from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from vapor.enums import GameStatus


@dataclass
class Genre:
    id: UUID
    name: str


@dataclass
class Platform:
    id: UUID
    name: str


@dataclass
class GameAsset:
    id: UUID
    game_id: UUID
    platform_id: UUID
    file_size: int
    download_url: str = ''

    def generate_signed_url(self, ttl: int = 3600) -> str:
        return f'{self.download_url}?token={self.id}&ttl={ttl}'


@dataclass
class Game:
    id: UUID
    creator_id: UUID
    title: str
    description: str
    price: Decimal
    release_date: date
    status: GameStatus
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    genres: list[Genre] = field(default_factory=list)
    platforms: list[Platform] = field(default_factory=list)
    assets: list[GameAsset] = field(default_factory=list)

    def approve(self) -> None:
        self.status = GameStatus.APPROVED

    def reject(self, reason: str) -> None:
        self.status = GameStatus.REJECTED

    def update_price(self, price: Decimal) -> None:
        self.price = price


class CatalogService:
    def __init__(self, catalog_repository):
        self._catalog_repository = catalog_repository

    def get_game(self, game_id: UUID) -> Game:
        return self._catalog_repository.find_by_id(game_id)

    def search_games(self, query: str, filters: dict) -> list[Game]:
        return self._catalog_repository.search(query, filters)

    def list_games(self, cursor: str, limit: int) -> tuple[list[Game], str]:
        return self._catalog_repository.list_approved(cursor, limit)

    def register_game(self, creator_id: UUID, data: dict) -> Game:
        game = Game(
            id=uuid4(),
            creator_id=creator_id,
            title=data['title'],
            description=data.get('description', ''),
            price=Decimal(str(data.get('price', '0.00'))),
            release_date=data.get('release_date', date.today()),
            status=GameStatus.PENDING,
        )
        return self._catalog_repository.save(game)
