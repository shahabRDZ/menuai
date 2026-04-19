from datetime import UTC, datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings


class PasswordHasher:
    """Thin wrapper around bcrypt so swapping algorithms is a one-liner."""

    def __init__(self) -> None:
        self._ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, password: str) -> str:
        return self._ctx.hash(password)

    def verify(self, password: str, password_hash: str) -> bool:
        return self._ctx.verify(password, password_hash)


class TokenService:
    """Issues and verifies short-lived access tokens."""

    def __init__(self, secret: str, algorithm: str, expire_minutes: int) -> None:
        self._secret = secret
        self._algorithm = algorithm
        self._expire = timedelta(minutes=expire_minutes)

    def issue(self, user_id: UUID) -> str:
        payload = {"sub": str(user_id), "exp": datetime.now(UTC) + self._expire}
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def verify(self, token: str) -> UUID | None:
        try:
            payload = jwt.decode(token, self._secret, algorithms=[self._algorithm])
            sub = payload.get("sub")
            if sub is None:
                return None
            return UUID(sub)
        except (JWTError, ValueError):
            return None


password_hasher = PasswordHasher()
token_service = TokenService(
    secret=settings.jwt_secret,
    algorithm=settings.jwt_algorithm,
    expire_minutes=settings.access_token_expire_minutes,
)
