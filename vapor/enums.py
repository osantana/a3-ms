from enum import Enum


class Role(Enum):
    USER = 'user'
    ADMINISTRATOR = 'administrator'


class GameStatus(Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'


class PaymentMethod(Enum):
    CREDIT_CARD = 'credit_card'
    PIX = 'pix'


class OrderStatus(Enum):
    PENDING = 'pending'
    PAID = 'paid'
    CANCELLED = 'cancelled'


class RefundStatus(Enum):
    REQUESTED = 'requested'
    APPROVED = 'approved'
    REJECTED = 'rejected'
