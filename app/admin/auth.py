from typing import Optional

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.config import settings
from app.exceptions import IncorrectEmailOrPassword, UserIsNotAdminException
from app.users.auth import authenticate_user, create_access_token
from app.users.dependencies import  get_admin


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        # Validate username/password credentials
        # And update session
        user = await authenticate_user(email, password)
        if not user:
            raise IncorrectEmailOrPassword
        if user.role.name != 'admin':
            raise UserIsNotAdminException
        access_token = create_access_token({"sub": str(user.id)})
        request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        user = await get_admin(token=token)

        # Check the token in depth


authentication_backend = AdminAuth(secret_key=settings.KEY)
