import asyncio


class ElkpyEvent(asyncio.Event):
    def __init__(self, state) -> None:
        super().__init__()
        self.state = state


