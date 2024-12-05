from logging import Logger

from aiogram import Dispatcher

from middleware.logging import LoggingMiddleware
from middleware.user import ACLMiddleware
from service import DefaultUserService


def setup(dispatcher: Dispatcher, logger: Logger, user_service: DefaultUserService):
    dispatcher.update.middleware(ACLMiddleware(user_service=user_service))
    dispatcher.update.middleware(LoggingMiddleware(logger))


__all__ = ["setup"]
