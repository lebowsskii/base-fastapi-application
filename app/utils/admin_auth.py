import base64
from datetime import UTC, datetime, timedelta

import argon2
import jwt
from loguru import logger
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

ph = argon2.PasswordHasher()


# ── SQLAdmin authentication ───────────────────────────────────────────────────
JWT_EXPIRATION_DELTA = timedelta(hours=12)
JWT_ALGORITHM = "HS256"


class AdminAuth(AuthenticationBackend):
    def __init__(self, jwt_secret: str, admin_password_hash: str):
        super().__init__(jwt_secret)
        self.admin_password_hash = admin_password_hash
        self.jwt_secret = jwt_secret

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        if not self.admin_password_hash:
            return False

        hs = base64.b64decode(self.admin_password_hash).decode("utf-8")

        try:
            if not ph.verify(hs, password):
                return False
        except Exception as e:
            logger.error(e)
            return False

        token = jwt.encode(
            {"username": username, "exp": datetime.now(UTC) + JWT_EXPIRATION_DELTA},
            self.jwt_secret,
            algorithm=JWT_ALGORITHM,
        )
        request.session.update({"token": token})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        try:
            jwt.decode(token, self.jwt_secret, algorithms=[JWT_ALGORITHM])
            return True
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return False
