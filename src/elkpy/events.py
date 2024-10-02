import asyncio


class TrackCreationEvent(asyncio.Event):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name: str = name
        self.action = 1
        self.sushi_id: int | None = None
        self.data: dict = {}


class TrackDeletionEvent(asyncio.Event):
    def __init__(self, sushi_id: int) -> None:
        super().__init__()
        self.action = 2
        self.sushi_id: int = sushi_id


class ProcessorCreationEvent(asyncio.Event):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name: str = name
        self.action = 1
        self.sushi_id: int | None = None
        self.data: dict = {}


class ProcessorDeletionEvent(asyncio.Event):
    def __init__(self, sushi_id: int) -> None:
        super().__init__()
        self.action = 2
        self.sushi_id: int = sushi_id
