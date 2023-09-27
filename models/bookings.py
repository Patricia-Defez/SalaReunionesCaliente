from pydantic import BaseModel

class BookingModel(BaseModel):
    idRoom: str
    idClient: str
    initHour: int
    endHour: int

class ListBookingModel(BaseModel):
    bookings: list[BookingModel]
    count: int
