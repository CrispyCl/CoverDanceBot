from typing import Any, Dict

from aiogram.types import TelegramObject
from aiogram.utils.i18n import SimpleI18nMiddleware

from models import User


class CustomI18nMiddleware(SimpleI18nMiddleware):
    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        user: User = data.get("current_user")
        if not user:
            return self.i18n.default_locale

        return user.language.value or self.i18n.default_locale


__all__ = ["CustomI18nMiddleware"]
