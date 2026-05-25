from dataclasses import dataclass, field
from datetime import UTC, datetime
from hashlib import sha256
from uuid import UUID, uuid4

from vapor.enums import Role


@dataclass
class User:
    id: UUID
    name: str
    email: str
    password_hash: str
    role: Role
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def authenticate(self, password: str) -> bool:
        return self.password_hash == sha256(password.encode()).hexdigest()

    def change_password(self, new_password: str) -> None:
        self.password_hash = sha256(new_password.encode()).hexdigest()


class AuthService:
    def __init__(self, user_repository):
        self._user_repository = user_repository

    def register(self, name: str, email: str, password: str) -> User:
        password_hash = sha256(password.encode()).hexdigest()
        user = User(
            id=uuid4(),
            name=name,
            email=email,
            password_hash=password_hash,
            role=Role.USER,
        )
        return self._user_repository.save(user)

    def login(self, email: str, password: str) -> User:
        user = self._user_repository.find_by_email(email)
        if not user.authenticate(password):
            raise ValueError('Invalid credentials')
        return user

    def logout(self, user_id: UUID) -> None:
        pass

    def request_password_reset(self, email: str) -> None:
        pass
