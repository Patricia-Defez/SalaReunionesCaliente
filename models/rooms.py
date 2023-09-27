from pydantic import BaseModel

class RoomModel(BaseModel):
    id: str
    openingH: int
    closingH: int
    capacity: int

class ListRoomModel(BaseModel):
    rooms: list[RoomModel]
    count: int