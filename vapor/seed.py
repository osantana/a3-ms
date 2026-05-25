import logging
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from hashlib import sha256
from uuid import uuid4

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
from vapor.users import User

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger('vapor.seed')


def pw(plain: str) -> str:
    return sha256(plain.encode()).hexdigest()


def run():
    conn = init_db()
    row = conn.execute('SELECT count(*) AS n FROM users').fetchone()
    conn.close()
    if row['n'] > 0:
        logger.info('Database already seeded — skipping.')
        return

    user_repo = PgUserRepository()
    catalog_repo = PgCatalogRepository()
    cart_repo = PgCartRepository()
    order_repo = PgOrderRepository()
    library_repo = PgLibraryRepository()
    catalog_service = CatalogService(catalog_repo)
    library_service = LibraryService(library_repo)

    now = datetime.now(UTC)

    # -- Users ---------------------------------------------------------------
    admin = User(
        id=uuid4(), name='Admin', email='admin@vapor.gg', password_hash=pw('admin123'), role=Role.ADMINISTRATOR
    )
    alice = User(id=uuid4(), name='Alice Studio', email='alice@vapor.gg', password_hash=pw('alice123'), role=Role.USER)
    bob = User(id=uuid4(), name='Bob Indie', email='bob@vapor.gg', password_hash=pw('bob123'), role=Role.USER)
    carlos = User(id=uuid4(), name='Carlos', email='carlos@vapor.gg', password_hash=pw('carlos123'), role=Role.USER)
    diana = User(id=uuid4(), name='Diana', email='diana@vapor.gg', password_hash=pw('diana123'), role=Role.USER)

    for u in (admin, alice, bob, carlos, diana):
        user_repo.save(u)
    logger.info('Created %d users (admin/alice123/bob123/carlos123/diana123)', 5)

    # -- Genres & Platforms (reused across games) ----------------------------
    genre_names = ['RPG', 'Adventure', 'Action', 'Puzzle', 'Strategy', 'Shooter', 'Simulation', 'Horror']
    genres = {name: Genre(id=uuid4(), name=name) for name in genre_names}

    platform_names = ['Windows', 'macOS', 'Linux']
    platforms = {name: Platform(id=uuid4(), name=name) for name in platform_names}

    # -- Games ---------------------------------------------------------------
    games_data = [
        {
            'creator': alice,
            'title': 'Cyber Quest',
            'description': 'An open-world cyberpunk RPG set in Neo São Paulo, 2187. '
            'Hack, fight, and negotiate your way through corporate conspiracies.',
            'price': Decimal('59.90'),
            'release_date': date(2026, 3, 15),
            'genres': ['RPG', 'Action', 'Adventure'],
            'platforms': ['Windows', 'Linux'],
            'status': GameStatus.APPROVED,
        },
        {
            'creator': alice,
            'title': 'Puzzle Dimensions',
            'description': 'Bend space and time to solve mind-bending puzzles across 120 hand-crafted levels.',
            'price': Decimal('24.90'),
            'release_date': date(2026, 1, 10),
            'genres': ['Puzzle', 'Strategy'],
            'platforms': ['Windows', 'macOS', 'Linux'],
            'status': GameStatus.APPROVED,
        },
        {
            'creator': alice,
            'title': 'Neon Racer X',
            'description': 'High-speed anti-gravity racing through procedurally generated neon cities.',
            'price': Decimal('39.90'),
            'release_date': date(2026, 5, 1),
            'genres': ['Action', 'Simulation'],
            'platforms': ['Windows'],
            'status': GameStatus.APPROVED,
        },
        {
            'creator': bob,
            'title': 'The Last Signal',
            'description': 'A narrative horror experience. You are alone on a space station. The radio crackles.',
            'price': Decimal('19.90'),
            'release_date': date(2026, 4, 20),
            'genres': ['Horror', 'Adventure'],
            'platforms': ['Windows', 'macOS'],
            'status': GameStatus.APPROVED,
        },
        {
            'creator': bob,
            'title': 'Starfield Tactics',
            'description': 'Command your fleet in turn-based tactical battles across the galaxy.',
            'price': Decimal('44.90'),
            'release_date': date(2026, 2, 28),
            'genres': ['Strategy', 'Shooter'],
            'platforms': ['Windows', 'Linux'],
            'status': GameStatus.APPROVED,
        },
        {
            'creator': bob,
            'title': 'Farm & Chill',
            'description': 'Relax, plant, harvest, and build your dream countryside farm.',
            'price': Decimal('0.00'),
            'release_date': date(2025, 12, 1),
            'genres': ['Simulation'],
            'platforms': ['Windows', 'macOS', 'Linux'],
            'status': GameStatus.APPROVED,
        },
        {
            'creator': alice,
            'title': 'Shadow Protocol',
            'description': 'A stealth-action game where every choice reshapes the world.',
            'price': Decimal('49.90'),
            'genres': ['Action', 'RPG'],
            'platforms': ['Windows'],
            'status': GameStatus.PENDING,
        },
        {
            'creator': bob,
            'title': 'Dungeon Crawl Alpha',
            'description': 'Early access roguelike — still rough around the edges.',
            'price': Decimal('9.90'),
            'genres': ['RPG', 'Action'],
            'platforms': ['Windows'],
            'status': GameStatus.PENDING,
        },
    ]

    saved_games = []
    for gd in games_data:
        game = catalog_service.register_game(
            gd['creator'].id,
            {
                'title': gd['title'],
                'description': gd['description'],
                'price': gd['price'],
                'release_date': gd.get('release_date', date.today()),
            },
        )
        for gname in gd['genres']:
            game.genres.append(genres[gname])
        for pname in gd['platforms']:
            game.platforms.append(platforms[pname])
        if gd['status'] == GameStatus.APPROVED:
            game.approve()
        catalog_repo.save(game)
        saved_games.append(game)

    approved_games = [g for g in saved_games if g.status == GameStatus.APPROVED]
    pending_games = [g for g in saved_games if g.status == GameStatus.PENDING]
    logger.info('Created %d games (%d approved, %d pending)', len(saved_games), len(approved_games), len(pending_games))

    # -- Orders & Library for Carlos -----------------------------------------
    carlos_bought = approved_games[:4]
    order_items = [OrderItem(id=uuid4(), game_id=g.id, price_paid=g.price) for g in carlos_bought]
    order1 = Order(
        id=uuid4(),
        user_id=carlos.id,
        total=sum(g.price for g in carlos_bought),
        payment_method=PaymentMethod.PIX,
        status=OrderStatus.PAID,
        created_at=now - timedelta(days=3),
        items=order_items,
    )
    order_repo.save(order1)
    for g in carlos_bought:
        library_service.add_game(carlos.id, g.id)

    # -- Orders & Library for Diana ------------------------------------------
    diana_bought = [approved_games[1], approved_games[4], approved_games[5]]
    order_items2 = [OrderItem(id=uuid4(), game_id=g.id, price_paid=g.price) for g in diana_bought]
    order2 = Order(
        id=uuid4(),
        user_id=diana.id,
        total=sum(g.price for g in diana_bought),
        payment_method=PaymentMethod.CREDIT_CARD,
        status=OrderStatus.PAID,
        created_at=now - timedelta(days=1),
        items=order_items2,
    )
    order_repo.save(order2)
    for g in diana_bought:
        library_service.add_game(diana.id, g.id)

    logger.info('Created 2 orders (Carlos: %d games, Diana: %d games)', len(carlos_bought), len(diana_bought))

    # -- Cart for Diana (items waiting for checkout) -------------------------
    cart = cart_repo.find_by_user(diana.id)
    cart.add_item(approved_games[0])
    cart.add_item(approved_games[2])
    cart_repo.save(cart)
    logger.info("Added 2 items to Diana's cart")

    logger.info('')
    logger.info('=== Seed complete ===')
    logger.info('')
    logger.info('Demo accounts (password):')
    logger.info('  admin@vapor.gg    (admin123)   — Administrator')
    logger.info('  alice@vapor.gg    (alice123)   — Creator')
    logger.info('  bob@vapor.gg      (bob123)     — Creator')
    logger.info('  carlos@vapor.gg   (carlos123)  — Player (4 games in library)')
    logger.info('  diana@vapor.gg    (diana123)   — Player (3 games + 2 in cart)')


if __name__ == '__main__':
    run()
