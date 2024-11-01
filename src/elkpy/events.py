import asyncio
from .sushierrors import SushiUnkownError


class ElkpyEvent(asyncio.Event):
    error: bool = False

    async def wait(self):
        if self.error:
            raise SushiUnkownError
        return await super().wait()


class TrackCreationEvent(ElkpyEvent):
    sushi_id: int

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name: str = name
        self.action = 1
        self.data: dict = {}


class TrackDeletionEvent(ElkpyEvent):
    def __init__(self, sushi_id: int) -> None:
        super().__init__()
        self.action = 2
        self.sushi_id: int = sushi_id


class ProcessorCreationEvent(ElkpyEvent):
    sushi_id: int

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name: str = name
        self.action = 1
        self.data: dict = {}


class ProcessorDeletionEvent(ElkpyEvent):
    def __init__(self, sushi_id: int) -> None:
        super().__init__()
        self.action = 2
        self.sushi_id: int = sushi_id
