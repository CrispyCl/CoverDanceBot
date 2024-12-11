from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, Update

from service import DefaultUserService


class ACLMiddleware(BaseMiddleware):
    def __init__(self, user_service: DefaultUserService):
        self.service = user_service
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ):

        if event.message:
            user_id = event.message.from_user.id
        elif event.callback_query:
            user_id = event.callback_query.from_user.id
        current_user = await self.service.get_or_create(user_id)

        data["current_user"] = current_user
        return await handler(event, data)


__all__ = ["ACLMiddleware"]
