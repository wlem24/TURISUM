from fastapi import Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_access_token
from app.core.security.permissions import Role, role_gte
from app.core.exceptions import InvalidToken, UnauthorizedRole, UserNotFound
from app.db.session import get_db
from app.models.user import User
from app.repositories.user_repo import UserRepository

_bearer = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(_bearer),
    session: AsyncSession = Depends(get_db),
) -> User:
    payload = verify_access_token(credentials.credentials)
    if not payload:
        raise InvalidToken()

    user_id = payload.get("sub")
    repo = UserRepository(session)
    user = await repo.get_active_by_id(user_id)
    if not user:
        raise UserNotFound(user_id)
    return user


def require_role(minimum_role: Role):
    async def _guard(current_user: User = Depends(get_current_user)) -> User:
        if not role_gte(current_user.role, minimum_role):
            raise UnauthorizedRole(minimum_role)
        return current_user
    return _guard


require_visitor = require_role(Role.VISITOR)
require_local = require_role(Role.LOCAL)
require_guide = require_role(Role.GUIDE)
require_admin = require_role(Role.ADMIN)
require_ministry = require_role(Role.MINISTRY)
