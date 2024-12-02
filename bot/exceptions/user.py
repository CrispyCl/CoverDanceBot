class TokenNegativeError(Exception):
    """Exception raised when token count is negative."""

    pass


class TokenDailyError(Exception):
    """Exception raised when user has already received tokens today."""

    pass


__all__ = ["TokenNegativeError", "TokenDailyError"]
