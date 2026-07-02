from enum import Enum


class Role(str, Enum):
    VISITOR = "visitor"
    LOCAL = "local"
    GUIDE = "guide"
    ADMIN = "admin"
    MINISTRY = "ministry"


ROLE_HIERARCHY: dict[str, int] = {
    Role.VISITOR: 0,
    Role.LOCAL: 1,
    Role.GUIDE: 2,
    Role.ADMIN: 3,
    Role.MINISTRY: 4,
}


def role_gte(user_role: str, required_role: str) -> bool:
    return ROLE_HIERARCHY.get(user_role, -1) >= ROLE_HIERARCHY.get(required_role, 999)
