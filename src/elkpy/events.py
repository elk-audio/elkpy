import asyncio


class ElkpyCreationEvent(asyncio.Event):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name: str = name
        self.action = 1
        self.sushi_id: int | None = None
        self.data: dict = {}


class ElkpyDeletionEvent(asyncio.Event):
    def __init__(self, name: str, sushi_id: int) -> None:
        super().__init__()
        self.name: str = name
        self.action = 2
        self.sushi_id: int = sushi_id
