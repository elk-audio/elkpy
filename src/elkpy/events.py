import asyncio
from .sushierrors import SushiUnkownError
from .sushi_info_types import TrackInfo, ProcessorInfo


class ElkpyEvent(asyncio.Event):
    error: bool = False
    action: int
    name: str = ''
    sushi_id: int = 0 
    command_response_id: int = 0
    command_response_status: int = 0
    data: TrackInfo | ProcessorInfo

    async def wait(self):
        if self.error:
            raise SushiUnkownError
        return await super().wait()


class TrackCreationEvent(ElkpyEvent):
    def __init__(self, name: str, command_response_id: int, command_response_status: int) -> None:
        super().__init__()
        self.name: str = name
        self.command_response_id = command_response_id
        self.command_response_status = command_response_status
        self.action = 1


class TrackDeletionEvent(ElkpyEvent):
    def __init__(self, sushi_id: int, command_response_id: int, command_response_status: int) -> None:
        super().__init__()
        self.action = 2
        self.command_response_id = command_response_id
        self.command_response_status = command_response_status
        self.sushi_id: int = sushi_id


class ProcessorCreationEvent(ElkpyEvent):
    def __init__(self, name: str, command_response_id: int, command_response_status: int) -> None:
        super().__init__()
        self.name: str = name
        self.command_response_id = command_response_id
        self.command_response_status = command_response_status
        self.action = 1


class ProcessorDeletionEvent(ElkpyEvent):
    def __init__(self, sushi_id: int, command_response_id: int, command_response_status: int) -> None:
        super().__init__()
        self.command_response_id = command_response_id
        self.command_response_status = command_response_status
        self.action = 2
        self.sushi_id: int = sushi_id
