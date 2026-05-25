from decimal import Decimal
from uuid import UUID, uuid4

from vapor.catalog import Game, GameAsset, Genre, Platform
from vapor.database import get_connection
from vapor.enums import GameStatus, OrderStatus, PaymentMethod, RefundStatus, Role
from vapor.library import LibraryEntry, Refund
from vapor.orders import Cart, CartItem, Order, OrderItem
from vapor.users import User


class PgUserRepository:
    def __init__(self, dsn=None):
        self._dsn = dsn

    def find_by_id(self, user_id: UUID) -> User:
        conn = get_connection(self._dsn)
        row = conn.execute('SELECT * FROM users WHERE id = %s', (user_id,)).fetchone()
        conn.close()
        if not row:
            raise LookupError(f'User {user_id} not found')
        return self._row_to_user(row)

    def find_by_email(self, email: str) -> User:
        conn = get_connection(self._dsn)
        row = conn.execute('SELECT * FROM users WHERE email = %s', (email,)).fetchone()
        conn.close()
        if not row:
            raise LookupError(f'User with email {email} not found')
        return self._row_to_user(row)

    def save(self, user: User) -> User:
        conn = get_connection(self._dsn)
        conn.execute(
            'INSERT INTO users (id, name, email, password_hash, role, created_at)'
            ' VALUES (%s, %s, %s, %s, %s, %s)'
            ' ON CONFLICT (id) DO UPDATE SET name=EXCLUDED.name, email=EXCLUDED.email,'
            ' password_hash=EXCLUDED.password_hash, role=EXCLUDED.role',
            (user.id, user.name, user.email, user.password_hash, user.role.value, user.created_at),
        )
        conn.commit()
        conn.close()
        return user

    def delete(self, user_id: UUID) -> None:
        conn = get_connection(self._dsn)
        conn.execute('DELETE FROM users WHERE id = %s', (user_id,))
        conn.commit()
        conn.close()

    def _row_to_user(self, row) -> User:
        return User(
            id=row['id'],
            name=row['name'],
            email=row['email'],
            password_hash=row['password_hash'],
            role=Role(row['role']),
            created_at=row['created_at'],
        )


class PgCatalogRepository:
    def __init__(self, dsn=None):
        self._dsn = dsn

    def find_by_id(self, game_id: UUID) -> Game:
        conn = get_connection(self._dsn)
        row = conn.execute('SELECT * FROM games WHERE id = %s', (game_id,)).fetchone()
        if not row:
            conn.close()
            raise LookupError(f'Game {game_id} not found')
        game = self._row_to_game(conn, row)
        conn.close()
        return game

    def find_by_creator(self, creator_id: UUID) -> list[Game]:
        conn = get_connection(self._dsn)
        rows = conn.execute('SELECT * FROM games WHERE creator_id = %s', (creator_id,)).fetchall()
        games = [self._row_to_game(conn, row) for row in rows]
        conn.close()
        return games

    def search(self, query: str, filters: dict) -> list[Game]:
        conn = get_connection(self._dsn)
        sql = 'SELECT * FROM games WHERE true'
        params: list = []
        if query:
            sql += ' AND title ILIKE %s'
            params.append(f'%{query}%')
        if 'status' in filters:
            sql += ' AND status = %s'
            params.append(filters['status'])
        if 'genre' in filters:
            sql += (
                ' AND id IN (SELECT game_id FROM game_genres'
                ' JOIN genres ON genre_id = genres.id WHERE genres.name = %s)'
            )
            params.append(filters['genre'])
        rows = conn.execute(sql, params).fetchall()
        games = [self._row_to_game(conn, row) for row in rows]
        conn.close()
        return games

    def list_approved(self, cursor: str, limit: int) -> tuple[list[Game], str]:
        conn = get_connection(self._dsn)
        sql = "SELECT * FROM games WHERE status = 'approved'"
        params: list = []
        if cursor:
            sql += ' AND created_at > %s'
            params.append(cursor)
        sql += ' ORDER BY created_at ASC LIMIT %s'
        params.append(limit)
        rows = conn.execute(sql, params).fetchall()
        games = [self._row_to_game(conn, row) for row in rows]
        conn.close()
        next_cursor = games[-1].created_at.isoformat() if games else ''
        return games, next_cursor

    def save(self, game: Game) -> Game:
        conn = get_connection(self._dsn)
        conn.execute(
            'INSERT INTO games (id, creator_id, title, description, price, release_date, status, created_at)'
            ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
            ' ON CONFLICT (id) DO UPDATE SET title=EXCLUDED.title, description=EXCLUDED.description,'
            ' price=EXCLUDED.price, release_date=EXCLUDED.release_date, status=EXCLUDED.status',
            (
                game.id,
                game.creator_id,
                game.title,
                game.description,
                game.price,
                game.release_date,
                game.status.value,
                game.created_at,
            ),
        )
        conn.execute('DELETE FROM game_genres WHERE game_id = %s', (game.id,))
        for genre in game.genres:
            existing = conn.execute('SELECT id FROM genres WHERE name = %s', (genre.name,)).fetchone()
            if existing:
                genre_id = existing['id']
            else:
                genre_id = genre.id
                conn.execute('INSERT INTO genres (id, name) VALUES (%s, %s)', (genre_id, genre.name))
            conn.execute('INSERT INTO game_genres (game_id, genre_id) VALUES (%s, %s)', (game.id, genre_id))
        conn.execute('DELETE FROM game_platforms WHERE game_id = %s', (game.id,))
        for platform in game.platforms:
            existing = conn.execute('SELECT id FROM platforms WHERE name = %s', (platform.name,)).fetchone()
            if existing:
                platform_id = existing['id']
            else:
                platform_id = platform.id
                conn.execute('INSERT INTO platforms (id, name) VALUES (%s, %s)', (platform_id, platform.name))
            conn.execute(
                'INSERT INTO game_platforms (game_id, platform_id) VALUES (%s, %s)',
                (game.id, platform_id),
            )
        conn.commit()
        conn.close()
        return game

    def _row_to_game(self, conn, row) -> Game:
        game_id = row['id']
        genre_rows = conn.execute(
            'SELECT g.* FROM genres g JOIN game_genres gg ON g.id = gg.genre_id WHERE gg.game_id = %s', (game_id,)
        ).fetchall()
        platform_rows = conn.execute(
            'SELECT p.* FROM platforms p JOIN game_platforms gp ON p.id = gp.platform_id WHERE gp.game_id = %s',
            (game_id,),
        ).fetchall()
        asset_rows = conn.execute('SELECT * FROM game_assets WHERE game_id = %s', (game_id,)).fetchall()
        return Game(
            id=game_id,
            creator_id=row['creator_id'],
            title=row['title'],
            description=row['description'] or '',
            price=Decimal(row['price']),
            release_date=row['release_date'],
            status=GameStatus(row['status']),
            created_at=row['created_at'],
            genres=[Genre(id=r['id'], name=r['name']) for r in genre_rows],
            platforms=[Platform(id=r['id'], name=r['name']) for r in platform_rows],
            assets=[
                GameAsset(
                    id=r['id'],
                    game_id=r['game_id'],
                    platform_id=r['platform_id'],
                    file_size=r['file_size'],
                    download_url=r['download_url'] or '',
                )
                for r in asset_rows
            ],
        )


class PgCartRepository:
    def __init__(self, dsn=None):
        self._dsn = dsn

    def find_by_user(self, user_id: UUID) -> Cart:
        conn = get_connection(self._dsn)
        rows = conn.execute('SELECT * FROM cart_items WHERE user_id = %s ORDER BY added_at', (user_id,)).fetchall()
        conn.close()
        items = [
            CartItem(
                id=r['id'],
                game_id=r['game_id'],
                unit_price=Decimal(r['unit_price']),
                added_at=r['added_at'],
            )
            for r in rows
        ]
        return Cart(id=uuid4(), user_id=user_id, items=items)

    def save(self, cart: Cart) -> Cart:
        conn = get_connection(self._dsn)
        conn.execute('DELETE FROM cart_items WHERE user_id = %s', (cart.user_id,))
        for item in cart.items:
            conn.execute(
                'INSERT INTO cart_items (id, user_id, game_id, unit_price, added_at) VALUES (%s, %s, %s, %s, %s)',
                (item.id, cart.user_id, item.game_id, item.unit_price, item.added_at),
            )
        conn.commit()
        conn.close()
        return cart

    def clear(self, user_id: UUID) -> None:
        conn = get_connection(self._dsn)
        conn.execute('DELETE FROM cart_items WHERE user_id = %s', (user_id,))
        conn.commit()
        conn.close()


class PgOrderRepository:
    def __init__(self, dsn=None):
        self._dsn = dsn

    def find_by_id(self, order_id: UUID) -> Order:
        conn = get_connection(self._dsn)
        row = conn.execute('SELECT * FROM orders WHERE id = %s', (order_id,)).fetchone()
        if not row:
            conn.close()
            raise LookupError(f'Order {order_id} not found')
        order = self._row_to_order(conn, row)
        conn.close()
        return order

    def find_by_user(self, user_id: UUID) -> list[Order]:
        conn = get_connection(self._dsn)
        rows = conn.execute('SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC', (user_id,)).fetchall()
        orders = [self._row_to_order(conn, row) for row in rows]
        conn.close()
        return orders

    def save(self, order: Order) -> Order:
        conn = get_connection(self._dsn)
        conn.execute(
            'INSERT INTO orders (id, user_id, total, payment_method, status, created_at)'
            ' VALUES (%s, %s, %s, %s, %s, %s)'
            ' ON CONFLICT (id) DO UPDATE SET status=EXCLUDED.status',
            (order.id, order.user_id, order.total, order.payment_method.value, order.status.value, order.created_at),
        )
        for item in order.items:
            conn.execute(
                'INSERT INTO order_items (id, order_id, game_id, price_paid) VALUES (%s, %s, %s, %s)'
                ' ON CONFLICT (id) DO NOTHING',
                (item.id, order.id, item.game_id, item.price_paid),
            )
        conn.commit()
        conn.close()
        return order

    def _row_to_order(self, conn, row) -> Order:
        item_rows = conn.execute('SELECT * FROM order_items WHERE order_id = %s', (row['id'],)).fetchall()
        return Order(
            id=row['id'],
            user_id=row['user_id'],
            total=Decimal(row['total']),
            payment_method=PaymentMethod(row['payment_method']),
            status=OrderStatus(row['status']),
            created_at=row['created_at'],
            items=[OrderItem(id=r['id'], game_id=r['game_id'], price_paid=Decimal(r['price_paid'])) for r in item_rows],
        )


class PgLibraryRepository:
    def __init__(self, dsn=None):
        self._dsn = dsn

    def find_by_user(self, user_id: UUID) -> list[LibraryEntry]:
        conn = get_connection(self._dsn)
        rows = conn.execute(
            'SELECT * FROM library_entries WHERE user_id = %s ORDER BY acquired_at', (user_id,)
        ).fetchall()
        conn.close()
        return [self._row_to_entry(r) for r in rows]

    def find_entry(self, user_id: UUID, game_id: UUID) -> LibraryEntry:
        conn = get_connection(self._dsn)
        row = conn.execute(
            'SELECT * FROM library_entries WHERE user_id = %s AND game_id = %s', (user_id, game_id)
        ).fetchone()
        conn.close()
        if not row:
            raise LookupError(f'Library entry not found for user={user_id} game={game_id}')
        return self._row_to_entry(row)

    def save(self, entry: LibraryEntry) -> LibraryEntry:
        conn = get_connection(self._dsn)
        conn.execute(
            'INSERT INTO library_entries (id, user_id, game_id, acquired_at) VALUES (%s, %s, %s, %s)'
            ' ON CONFLICT (id) DO NOTHING',
            (entry.id, entry.user_id, entry.game_id, entry.acquired_at),
        )
        conn.commit()
        conn.close()
        return entry

    def delete(self, entry_id: UUID) -> None:
        conn = get_connection(self._dsn)
        conn.execute('DELETE FROM library_entries WHERE id = %s', (entry_id,))
        conn.commit()
        conn.close()

    def _row_to_entry(self, row) -> LibraryEntry:
        return LibraryEntry(
            id=row['id'],
            user_id=row['user_id'],
            game_id=row['game_id'],
            acquired_at=row['acquired_at'],
        )


class PgRefundRepository:
    def __init__(self, dsn=None):
        self._dsn = dsn

    def find_by_id(self, refund_id: UUID) -> Refund:
        conn = get_connection(self._dsn)
        row = conn.execute('SELECT * FROM refunds WHERE id = %s', (refund_id,)).fetchone()
        conn.close()
        if not row:
            raise LookupError(f'Refund {refund_id} not found')
        return self._row_to_refund(row)

    def save(self, refund: Refund) -> Refund:
        conn = get_connection(self._dsn)
        conn.execute(
            'INSERT INTO refunds (id, order_item_id, reason, status, created_at) VALUES (%s, %s, %s, %s, %s)'
            ' ON CONFLICT (id) DO UPDATE SET status=EXCLUDED.status',
            (refund.id, refund.order_item_id, refund.reason, refund.status.value, refund.created_at),
        )
        conn.commit()
        conn.close()
        return refund

    def _row_to_refund(self, row) -> Refund:
        return Refund(
            id=row['id'],
            order_item_id=row['order_item_id'],
            reason=row['reason'],
            status=RefundStatus(row['status']),
            created_at=row['created_at'],
        )
