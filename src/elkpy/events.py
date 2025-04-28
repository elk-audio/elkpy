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
        r = await super().wait()
        if self.error:
            raise SushiUnkownError('Sushi returned an error')
        return r
