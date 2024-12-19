import asyncio
from .sushierrors import SushiUnkownError
from .sushi_info_types import TrackInfo, ProcessorInfo


class ElkpyEvent(asyncio.Event):
    error: bool = False
    action: int
    name: str = ''
    sushi_id: int = 0 
    data: TrackInfo | ProcessorInfo

    async def wait(self):
        if self.error:
            raise SushiUnkownError
        return await super().wait()


class TrackCreationEvent(ElkpyEvent):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name: str = name
        self.action = 1


class TrackDeletionEvent(ElkpyEvent):
    def __init__(self, sushi_id: int) -> None:
        super().__init__()
        self.action = 2
        self.sushi_id: int = sushi_id


class ProcessorCreationEvent(ElkpyEvent):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name: str = name
        self.action = 1


class ProcessorDeletionEvent(ElkpyEvent):
    def __init__(self, sushi_id: int) -> None:
        super().__init__()
        self.action = 2
        self.sushi_id: int = sushi_id
