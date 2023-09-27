from config.db import BookingDO
from controllers.rooms import RoomController
from controllers.clients import ClientController

class NoRoomException(Exception):
    pass

class NoClientException(Exception):
    pass

class InvalidTimingException(Exception):
    pass

class BookingController:
    def __init__(self):
        self.booking_db = BookingDO
        self.rc = RoomController()
        self.cc = ClientController()

    def _check_room(self, roomId):
        room = self.rc.get_room_by_id(roomId)
        return room

    def _check_client(self, clientId):
        client = self.cc.get_client_by_id(clientId)
        return client
    
    def _check_timing(self, initHour, endHour, room):
        if initHour not in range(room["openingH"],room["closingH"]):
            return False
        elif endHour not in range(room["openingH"]+1,room["closingH"]+1):
            return False
        elif initHour >= endHour:
            return False
        else:
            return True
        
    def get_booking_by_id(self, booking_id):
        filter = {"_id": booking_id}
        booking = self.booking_db.find_one(filter)
        if booking:
            booking.pop("_id")
            booking.pop("totalH")
            return booking
        else:
            return False

    def insert_booking(self, booking):
        room = self._check_room(booking.get("idRoom"))
        if not room:
            raise NoRoomException
        client = self._check_client(booking.get("idClient"))
        if not client:
            raise NoClientException
        correctTiming = self._check_timing(booking["initHour"],booking["endHour"], room)
        if not correctTiming:
            raise InvalidTimingException
        booking["totalH"] = booking["endHour"]- booking["initHour"]
        new_booking = self.booking_db.insert_one(booking)
        return self.get_booking_by_id(new_booking.inserted_id)

