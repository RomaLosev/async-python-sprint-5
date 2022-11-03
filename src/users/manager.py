import uuid

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    CookieTransport,
    JWTStrategy
)
from loguru import logger

from core.config import SECRET
from db.db import get_user_db
from models.models import User

bearer_transport = BearerTransport(tokenUrl="/auth/jwt/login")
cookie_transport = CookieTransport(cookie_max_age=3600, cookie_secure=False)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Request | None = None):
        logger.info(f"User {user.email} has registered.")

    async def on_after_login(
            self,
            user: User,
            request: Request | None = None,
    ):
        logger.info(f"User {user.username} logged in.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None,
    ):
        logger.info(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ):
        logger.info(f"Verification requested for user {user.id}. Verification token: {token}")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


async def get_enabled_backends(request: Request) -> list[AuthenticationBackend]:
    """Return the enabled dependencies following custom logic."""
    if request.url.path == "/protected-route-only-jwt":
        return [jwt_backend]
    else:
        return [cookie_backend, jwt_backend]


async def get_user_manager(user_db=Depends(get_user_db)) -> UserManager:
    yield UserManager(user_db)

cookie_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

jwt_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [jwt_backend],
)

current_user = fastapi_users.current_user(verified=False, get_enabled_backends=get_enabled_backends)
