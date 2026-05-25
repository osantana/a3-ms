from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from vapor.catalog import Game
from vapor.enums import OrderStatus, PaymentMethod


@dataclass
class CartItem:
    id: UUID
    game_id: UUID
    unit_price: Decimal
    added_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class Cart:
    id: UUID
    user_id: UUID
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    items: list[CartItem] = field(default_factory=list)

    def add_item(self, game: Game) -> CartItem:
        for item in self.items:
            if item.game_id == game.id:
                raise ValueError('Game already in cart')
        cart_item = CartItem(id=uuid4(), game_id=game.id, unit_price=game.price)
        self.items.append(cart_item)
        return cart_item

    def remove_item(self, game_id: UUID) -> None:
        self.items = [item for item in self.items if item.game_id != game_id]

    def clear(self) -> None:
        self.items.clear()

    def total(self) -> Decimal:
        return sum((item.unit_price for item in self.items), Decimal('0.00'))


@dataclass
class OrderItem:
    id: UUID
    game_id: UUID
    price_paid: Decimal


@dataclass
class Order:
    id: UUID
    user_id: UUID
    total: Decimal
    payment_method: PaymentMethod
    status: OrderStatus
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    items: list[OrderItem] = field(default_factory=list)

    def cancel(self) -> None:
        self.status = OrderStatus.CANCELLED


class CheckoutService:
    def __init__(self, cart_repository, order_repository, payment_gateway, library_service):
        self._cart_repository = cart_repository
        self._order_repository = order_repository
        self._payment_gateway = payment_gateway
        self._library_service = library_service

    def checkout(self, user_id: UUID, method: PaymentMethod, payment_data: dict) -> Order:
        cart = self._cart_repository.find_by_user(user_id)
        if not cart.items:
            raise ValueError('Cart is empty')

        order_items = [OrderItem(id=uuid4(), game_id=item.game_id, price_paid=item.unit_price) for item in cart.items]
        order = Order(
            id=uuid4(),
            user_id=user_id,
            total=cart.total(),
            payment_method=method,
            status=OrderStatus.PENDING,
            items=order_items,
        )

        self._payment_gateway.charge(order, payment_data)
        order.status = OrderStatus.PAID
        self._order_repository.save(order)

        for item in order.items:
            self._library_service.add_game(user_id, item.game_id)

        self._cart_repository.clear(user_id)
        return order
