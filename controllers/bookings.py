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

    def _check_room(self, roomId):
        rc = RoomController()
        room = rc.get_room_by_id(roomId)
        return room

    def _check_client(self, clientId):
        cc = ClientController()
        client = cc.get_client_by_id(clientId)
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
        correctTiming = self._check_timing(booking["initHour"],booking["endHour"], room)
        if not client:
            raise NoClientException
        elif not correctTiming:
            raise InvalidTimingException
        else:
            booking["totalH"] = booking["endHour"]- booking["initHour"]
            new_booking = self.booking_db.insert_one(booking)
            return self.get_booking_by_id(new_booking.inserted_id)
        
    def list_bookings(self):
        filter = {}
        res = list(self.booking_db.find(filter, limit=500))
        for x in res:
            x.pop("_id")
        return res
    
    def list_bookings_by_client_id(self, clientId):
        client = self._check_client(clientId)
        if not client:
            raise NoClientException
        else:
            filter = {"idClient": clientId}
            res = list(self.booking_db.find(filter, limit=500))
            for x in res:
                x.pop("_id")
            return res
        
    def list_bookings_by_room_id(self, roomId):
        room = self._check_room(roomId)
        if not room:
            raise NoRoomException
        else:
            filter = {"idRoom": roomId}
            res = list(self.booking_db.find(filter, limit=500))
            for x in res:
                x.pop("_id")
            return res
    
    def get_bookings_by_clients(self):
        res = self.booking_db.aggregate([{'$group':{'_id':'$idClient','totalBookings':{'$count':{}}}}])
        return list(res)

    def list_overlapped_booking(self, roomId):
        filter = {"idRoom": roomId}
        all_bookings = list(self.booking_db.find(filter, limit=500))
        bookings= []
        uniques = []
        if not all_bookings:
            return False
        else:
            copy_bookings = all_bookings.copy()
            for x in all_bookings:
                x["_id"] = str(x.get('_id'))
                for y in copy_bookings: 
                    y["_id"] = str(y.get('_id'))
                    if  x["initHour"] in range(y["initHour"], y["endHour"]) or  x["endHour"] in range(y["initHour"],y["endHour"]+1):
                        bookings.append(x)
            [uniques.append(x) for x in bookings if x not in uniques]
            return uniques
