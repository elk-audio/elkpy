from typing_extensions import Callable
import asyncio


def add_wait_event(wait_manager):
    """This will add an asyncio.Event to the passed wait_manager and also add it as a return value to the decorated function."""
    def add_event(fun: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            fun(*args, **kwargs)
            e = asyncio.Event()
            wait_manager.event_list.append(e)
            return e
        return wrapper
    return add_event


class ElkpyEvent(asyncio.Event):
    def __init__(self, state) -> None:
        super().__init__()
        self.state = state
