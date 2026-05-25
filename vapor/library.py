from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from vapor.enums import RefundStatus


@dataclass
class LibraryEntry:
    id: UUID
    user_id: UUID
    game_id: UUID
    acquired_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class Refund:
    id: UUID
    order_item_id: UUID
    reason: str
    status: RefundStatus
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def approve(self) -> None:
        self.status = RefundStatus.APPROVED

    def reject(self, reason: str) -> None:
        self.status = RefundStatus.REJECTED


class LibraryService:
    def __init__(self, library_repository):
        self._library_repository = library_repository

    def add_game(self, user_id: UUID, game_id: UUID) -> LibraryEntry:
        entry = LibraryEntry(id=uuid4(), user_id=user_id, game_id=game_id)
        return self._library_repository.save(entry)

    def has_game(self, user_id: UUID, game_id: UUID) -> bool:
        try:
            self._library_repository.find_entry(user_id, game_id)
            return True
        except LookupError:
            return False

    def remove_game(self, user_id: UUID, game_id: UUID) -> None:
        entry = self._library_repository.find_entry(user_id, game_id)
        self._library_repository.delete(entry.id)

    def list_games(self, user_id: UUID) -> list[LibraryEntry]:
        return self._library_repository.find_by_user(user_id)


class DownloadService:
    def __init__(self, library_service, catalog_repository):
        self._library_service = library_service
        self._catalog_repository = catalog_repository

    def generate_download_url(self, user_id: UUID, game_id: UUID, platform_id: UUID) -> str:
        if not self._library_service.has_game(user_id, game_id):
            raise PermissionError('Game not in library')
        game = self._catalog_repository.find_by_id(game_id)
        for asset in game.assets:
            if asset.platform_id == platform_id:
                return asset.generate_signed_url()
        raise LookupError('Asset not found for platform')


class RefundService:
    def __init__(self, refund_policy, payment_gateway, library_service):
        self._refund_policy = refund_policy
        self._payment_gateway = payment_gateway
        self._library_service = library_service

    def request(self, order_item_id: UUID, reason: str) -> Refund:
        if not self._refund_policy.is_eligible(order_item_id):
            msg = self._refund_policy.rejection_reason(order_item_id)
            raise ValueError(msg)
        return Refund(
            id=uuid4(),
            order_item_id=order_item_id,
            reason=reason,
            status=RefundStatus.REQUESTED,
        )

    def process(self, refund_id: UUID) -> None:
        pass
