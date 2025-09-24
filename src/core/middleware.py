import inspect
from functools import wraps

from dependency_injector.wiring import inject as di_inject
from loguru import logger

from src.services.base_service import BaseService


def inject(func):
    # Support both async and sync callables
    if inspect.iscoroutinefunction(func):

        @di_inject
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            injected_services = [arg for arg in kwargs.values() if isinstance(arg, BaseService)]
            if len(injected_services) == 0:
                return result
            try:
                injected_services[-1].close_scoped_session()
            except Exception as e:
                logger.error(e)
            return result

        return async_wrapper

    @di_inject
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        injected_services = [arg for arg in kwargs.values() if isinstance(arg, BaseService)]
        if len(injected_services) == 0:
            return result
        try:
            injected_services[-1].close_scoped_session()
        except Exception as e:
            logger.error(e)
        return result

    return wrapper
