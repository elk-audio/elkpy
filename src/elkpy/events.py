import asyncio
from .sushierrors import SushiUnkownError


class SushiCommandResponse(asyncio.Event):
    command_id: int
    error: bool = False

    def __init__(self, id: int, result=None) -> None:
        self.id = id
        self.result = result
        super().__init__()

    async def wait(self):
        if self.error:
            raise SushiUnkownError
        return await super().wait()
