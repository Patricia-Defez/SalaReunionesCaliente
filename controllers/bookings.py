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

    async def _check_room(self, roomId):
        rc = RoomController()
        room = await rc.get_room_by_id(roomId)
        return room

    async def _check_client(self, clientId):
        cc = ClientController()
        client = await cc.get_client_by_id(clientId)
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
        
    async def get_booking_by_id(self, booking_id):
        filter = {"_id": booking_id}
        booking = await self.booking_db.find_one(filter)
        if booking:
            booking.pop("_id")
            booking.pop("totalH")
            return booking
        else:
            return False

    async def insert_booking(self, booking):
        room = await self._check_room(booking.get("idRoom"))
        if not room:
            raise NoRoomException
        client = await self._check_client(booking.get("idClient"))
        correctTiming = self._check_timing(booking["initHour"],booking["endHour"], room)
        if not client:
            raise NoClientException
        elif not correctTiming:
            raise InvalidTimingException
        else:
            booking["totalH"] = booking["endHour"]- booking["initHour"]
            new_booking = await self.booking_db.insert_one(booking)
            return await self.get_booking_by_id(new_booking.inserted_id)
        
    async def list_bookings(self):
        filter = {}
        data = self.booking_db.find(filter, limit=500)
        res = await data.to_list(length=500)
        for x in res:   
            x.pop("_id")
        return res
    
    async def list_bookings_by_client_id(self, clientId):
        client = await self._check_client(clientId)
        if not client:
            raise NoClientException
        else:
            filter = {"idClient": clientId}
            data = self.booking_db.find(filter, limit=500)
            res = await data.to_list(length=500)
            for x in res:
                x.pop("_id")
            return res
        
    async def list_bookings_by_room_id(self, roomId):
        room = self._check_room(roomId)
        if not room:
            raise NoRoomException
        else:
            filter = {"idRoom": roomId}
            data = self.booking_db.find(filter, limit=500)
            res = await data.to_list(length=500)
            for x in res:
                x.pop("_id")
            return res
    
    async def get_bookings_by_clients(self):
        data = self.booking_db.aggregate([{'$group':{'_id':'$idClient','totalBookings':{'$count':{}}}}])
        res = await data.to_list(length=500)
        return res

    async def list_overlapped_booking(self, roomId):
        filter = {"idRoom": roomId}
        data = self.booking_db.find(filter, limit=500)
        all_bookings = await data.to_list(length=500)
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
