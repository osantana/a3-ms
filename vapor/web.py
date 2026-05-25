from datetime import date
from hashlib import sha256
from pathlib import Path
from uuid import UUID, uuid4

from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from vapor.catalog import CatalogService, Genre, Platform
from vapor.database import init_db
from vapor.enums import GameStatus, OrderStatus, PaymentMethod, Role
from vapor.library import LibraryService
from vapor.orders import Order, OrderItem
from vapor.repositories import (
    PgCartRepository,
    PgCatalogRepository,
    PgLibraryRepository,
    PgOrderRepository,
    PgUserRepository,
)
from vapor.seed import run as seed_db
from vapor.users import AuthService, User

TEMPLATES_DIR = Path(__file__).parent / 'templates'

app = FastAPI(title='Vapor', debug=True)
app.add_middleware(SessionMiddleware, secret_key='vapor-secret-key-change-in-production')
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

user_repo = PgUserRepository()
catalog_repo = PgCatalogRepository()
cart_repo = PgCartRepository()
order_repo = PgOrderRepository()
library_repo = PgLibraryRepository()
auth_service = AuthService(user_repo)
catalog_service = CatalogService(catalog_repo)
library_service = LibraryService(library_repo)


@app.on_event('startup')
def startup():
    conn = init_db()
    conn.close()
    seed_db()


def current_user(request: Request) -> User | None:
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    try:
        return user_repo.find_by_id(UUID(user_id))
    except LookupError:
        return None


def render(request: Request, template: str, **extra):
    context = {'user': current_user(request), **extra}
    return templates.TemplateResponse(request, template, context=context)


# -- Auth --------------------------------------------------------------------


@app.get('/')
def index(request: Request):
    games, _ = catalog_repo.list_approved('', 20)
    return render(request, 'catalog.html', games=games, query='', genre='')


@app.get('/register')
def register_form(request: Request):
    return render(request, 'register.html', error='')


@app.post('/register')
def register(
    request: Request,
    name: str = Form(),
    email: str = Form(),
    password: str = Form(),
):
    try:
        user_repo.find_by_email(email)
        return render(request, 'register.html', error='Email already registered.')
    except LookupError:
        pass
    password_hash = sha256(password.encode()).hexdigest()
    user = User(id=uuid4(), name=name, email=email, password_hash=password_hash, role=Role.USER)
    user_repo.save(user)
    request.session['user_id'] = str(user.id)
    return RedirectResponse('/', status_code=303)


@app.get('/login')
def login_form(request: Request):
    return render(request, 'login.html', error='')


@app.post('/login')
def login(request: Request, email: str = Form(), password: str = Form()):
    try:
        user = auth_service.login(email, password)
    except (LookupError, ValueError):
        return render(request, 'login.html', error='Invalid email or password.')
    request.session['user_id'] = str(user.id)
    return RedirectResponse('/', status_code=303)


@app.get('/logout')
def logout(request: Request):
    request.session.clear()
    return RedirectResponse('/', status_code=303)


# -- Catalog -----------------------------------------------------------------


@app.get('/catalog')
def catalog(request: Request, query: str = '', genre: str = ''):
    filters = {}
    if genre:
        filters['genre'] = genre
    if query or filters:
        games = catalog_repo.search(query, filters)
        games = [g for g in games if g.status == GameStatus.APPROVED]
    else:
        games, _ = catalog_repo.list_approved('', 50)
    return render(request, 'catalog.html', games=games, query=query, genre=genre)


@app.get('/games/{game_id}')
def game_detail(request: Request, game_id: str):
    game = catalog_repo.find_by_id(UUID(game_id))
    user = current_user(request)
    in_library = False
    if user:
        in_library = library_service.has_game(user.id, game.id)
    return render(request, 'game_detail.html', game=game, in_library=in_library)


# -- Cart --------------------------------------------------------------------


@app.get('/cart')
def view_cart(request: Request):
    user = current_user(request)
    if not user:
        return RedirectResponse('/login', status_code=303)
    cart = cart_repo.find_by_user(user.id)
    games = {}
    for item in cart.items:
        games[item.game_id] = catalog_repo.find_by_id(item.game_id)
    return render(request, 'cart.html', cart=cart, games=games)


@app.post('/cart/add/{game_id}')
def add_to_cart(request: Request, game_id: str):
    user = current_user(request)
    if not user:
        return RedirectResponse('/login', status_code=303)
    game = catalog_repo.find_by_id(UUID(game_id))
    cart = cart_repo.find_by_user(user.id)
    try:
        cart.add_item(game)
        cart_repo.save(cart)
    except ValueError:
        pass
    return RedirectResponse(f'/games/{game_id}', status_code=303)


@app.post('/cart/remove/{game_id}')
def remove_from_cart(request: Request, game_id: str):
    user = current_user(request)
    if not user:
        return RedirectResponse('/login', status_code=303)
    cart = cart_repo.find_by_user(user.id)
    cart.remove_item(UUID(game_id))
    cart_repo.save(cart)
    return RedirectResponse('/cart', status_code=303)


# -- Checkout ----------------------------------------------------------------


@app.post('/checkout')
def checkout(request: Request, payment_method: str = Form()):
    user = current_user(request)
    if not user:
        return RedirectResponse('/login', status_code=303)
    method = PaymentMethod(payment_method)
    cart = cart_repo.find_by_user(user.id)
    if not cart.items:
        return RedirectResponse('/cart', status_code=303)

    order_items = [OrderItem(id=uuid4(), game_id=item.game_id, price_paid=item.unit_price) for item in cart.items]
    order = Order(
        id=uuid4(),
        user_id=user.id,
        total=cart.total(),
        payment_method=method,
        status=OrderStatus.PAID,
        items=order_items,
    )
    order_repo.save(order)
    for item in order.items:
        library_service.add_game(user.id, item.game_id)
    cart_repo.clear(user.id)
    return RedirectResponse(f'/orders/{order.id}', status_code=303)


# -- Library & Orders --------------------------------------------------------


@app.get('/library')
def library(request: Request):
    user = current_user(request)
    if not user:
        return RedirectResponse('/login', status_code=303)
    entries = library_repo.find_by_user(user.id)
    games = {}
    for entry in entries:
        games[entry.game_id] = catalog_repo.find_by_id(entry.game_id)
    return render(request, 'library.html', entries=entries, games=games)


@app.get('/orders')
def orders(request: Request):
    user = current_user(request)
    if not user:
        return RedirectResponse('/login', status_code=303)
    user_orders = order_repo.find_by_user(user.id)
    return render(request, 'orders.html', orders=user_orders)


@app.get('/orders/{order_id}')
def order_detail(request: Request, order_id: str):
    user = current_user(request)
    if not user:
        return RedirectResponse('/login', status_code=303)
    order = order_repo.find_by_id(UUID(order_id))
    games = {}
    for item in order.items:
        games[item.game_id] = catalog_repo.find_by_id(item.game_id)
    return render(request, 'order_detail.html', order=order, games=games)


# -- Creator -----------------------------------------------------------------


@app.get('/creator/games')
def creator_games(request: Request):
    user = current_user(request)
    if not user:
        return RedirectResponse('/login', status_code=303)
    games = catalog_repo.find_by_creator(user.id)
    return render(request, 'creator_games.html', games=games)


@app.get('/creator/games/new')
def creator_new_game_form(request: Request):
    user = current_user(request)
    if not user:
        return RedirectResponse('/login', status_code=303)
    return render(request, 'creator_new_game.html', error='')


@app.post('/creator/games/new')
def creator_new_game(
    request: Request,
    title: str = Form(),
    description: str = Form(default=''),
    price: str = Form(default='0.00'),
    release_date: str = Form(default=''),
    genres: str = Form(default=''),
    platforms: str = Form(default=''),
):
    user = current_user(request)
    if not user:
        return RedirectResponse('/login', status_code=303)
    data = {
        'title': title,
        'description': description,
        'price': price,
        'release_date': date.fromisoformat(release_date) if release_date else date.today(),
    }
    game = catalog_service.register_game(user.id, data)
    if genres.strip():
        for name in genres.split(','):
            game.genres.append(Genre(id=uuid4(), name=name.strip()))
    if platforms.strip():
        for name in platforms.split(','):
            game.platforms.append(Platform(id=uuid4(), name=name.strip()))
    catalog_repo.save(game)
    return RedirectResponse('/creator/games', status_code=303)


# -- Admin / Moderation ------------------------------------------------------


@app.get('/admin/moderation')
def moderation(request: Request):
    user = current_user(request)
    if not user or user.role != Role.ADMINISTRATOR:
        return RedirectResponse('/login', status_code=303)
    pending = catalog_repo.search('', {'status': 'pending'})
    return render(request, 'moderation.html', games=pending)


@app.post('/admin/approve/{game_id}')
def approve_game(request: Request, game_id: str):
    user = current_user(request)
    if not user or user.role != Role.ADMINISTRATOR:
        return RedirectResponse('/login', status_code=303)
    game = catalog_repo.find_by_id(UUID(game_id))
    game.approve()
    catalog_repo.save(game)
    return RedirectResponse('/admin/moderation', status_code=303)


@app.post('/admin/reject/{game_id}')
def reject_game(request: Request, game_id: str, reason: str = Form(default='')):
    user = current_user(request)
    if not user or user.role != Role.ADMINISTRATOR:
        return RedirectResponse('/login', status_code=303)
    game = catalog_repo.find_by_id(UUID(game_id))
    game.reject(reason)
    catalog_repo.save(game)
    return RedirectResponse('/admin/moderation', status_code=303)
