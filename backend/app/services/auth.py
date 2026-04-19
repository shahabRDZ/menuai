from sqlalchemy.exc import IntegrityError

from app.exceptions import Conflict, Unauthorized
from app.models import User
from app.repositories import UserRepository
from app.schemas.auth import RegisterRequest
from app.services.security import PasswordHasher, TokenService


class AuthService:
    def __init__(
        self,
        users: UserRepository,
        password_hasher: PasswordHasher,
        token_service: TokenService,
    ) -> None:
        self.users = users
        self.password_hasher = password_hasher
        self.token_service = token_service

    async def register(self, payload: RegisterRequest) -> tuple[User, str]:
        user = User(
            email=payload.email.lower(),
            password_hash=self.password_hasher.hash(payload.password),
            name=payload.name,
            native_language=payload.native_language,
            target_language=payload.target_language,
        )
        try:
            await self.users.add(user)
            await self.users.session.commit()
        except IntegrityError as exc:
            await self.users.session.rollback()
            raise Conflict("Email already registered") from exc

        await self.users.session.refresh(user)
        return user, self.token_service.issue(user.id)

    async def login(self, email: str, password: str) -> tuple[User, str]:
        user = await self.users.get_by_email(email)
        if user is None or not self.password_hasher.verify(password, user.password_hash):
            raise Unauthorized("Invalid email or password")
        return user, self.token_service.issue(user.id)
