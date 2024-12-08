from typing import Any

from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject

from models import User
from service import DefaultUserService


class IsAdminFilter(BaseFilter):
    """Is admin filter."""

    async def __call__(self, obj: TelegramObject, **data: Any) -> bool:
        user: User = data.get("current_user")
        if not user:
            return False

        user_service: DefaultUserService = data.get("user_service")
        if not user_service:
            return False

        return await user_service.is_admin(user.id)


class IsSuperAdminFilter(BaseFilter):
    """Is super admin filter."""

    async def __call__(self, obj: TelegramObject, **data: Any) -> bool:
        user: User = data.get("current_user")
        if not user:
            return False

        user_service: DefaultUserService = data.get("user_service")
        if not user_service:
            return False

        return await user_service.is_super_admin(user.id)


__all__ = ["IsAdminFilter", "IsSuperAdminFilter"]
