from logging import Logger

from aiogram import Dispatcher
from aiogram.utils.i18n import I18n

from middleware.i18n import CustomI18nMiddleware
from middleware.logging import LoggingMiddleware
from middleware.user import ACLMiddleware
from service import DefaultUserService


def setup(dispatcher: Dispatcher, logger: Logger, user_service: DefaultUserService, i18n: I18n):
    dispatcher.update.middleware(ACLMiddleware(user_service=user_service))
    dispatcher.update.middleware(LoggingMiddleware(logger))
    dispatcher.update.middleware(CustomI18nMiddleware(i18n=i18n))


__all__ = ["setup"]
