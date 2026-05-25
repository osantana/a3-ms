from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID

from vapor.catalog import Game


@dataclass
class SalesMetrics:
    game_id: UUID
    game_title: str
    units_sold: int
    gross_revenue: Decimal
    net_revenue: Decimal
    period_start: date
    period_end: date


class ModerationService:
    def __init__(self, catalog_repository, notification_service):
        self._catalog_repository = catalog_repository
        self._notification_service = notification_service

    def list_pending(self) -> list[Game]:
        results, _ = self._catalog_repository.search('', {'status': 'pending'})
        return results

    def approve(self, game_id: UUID, admin_id: UUID) -> None:
        game = self._catalog_repository.find_by_id(game_id)
        game.approve()
        self._catalog_repository.save(game)
        self._notification_service.send(
            game.creator_id,
            'Game approved',
            f'Your game "{game.title}" has been approved and is now available in the catalog.',
        )

    def reject(self, game_id: UUID, admin_id: UUID, reason: str) -> None:
        game = self._catalog_repository.find_by_id(game_id)
        game.reject(reason)
        self._catalog_repository.save(game)
        self._notification_service.send(
            game.creator_id,
            'Game rejected',
            f'Your game "{game.title}" has been rejected. Reason: {reason}',
        )

    def request_changes(self, game_id: UUID, admin_id: UUID, notes: str) -> None:
        game = self._catalog_repository.find_by_id(game_id)
        self._notification_service.send(
            game.creator_id,
            'Changes requested',
            f'Your game "{game.title}" needs changes: {notes}',
        )


class SalesDashboardService:
    def __init__(self, order_repository):
        self._order_repository = order_repository

    def get_metrics(self, creator_id: UUID, game_id: UUID, start: date, end: date) -> list[SalesMetrics]:
        return []

    def export_csv(self, creator_id: UUID, start: date, end: date) -> bytes:
        return b''
