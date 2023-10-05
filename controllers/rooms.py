from config.db import RoomDO, BookingDO

class InvalidTimingException(Exception):
    pass

class InvalidCapacityException(Exception):
    pass

class RoomController:
    def __init__(self):
        self.room_db = RoomDO
        self.booking_db = BookingDO

    def _check_timing(self, initHour, endHour):
        if initHour not in range(1,24):
            return False
        elif endHour not in range(2,25):
            return False
        elif initHour >= endHour:
            return False
        else:
            return True
        
    def _check_capacity(self, capacity):
        if capacity not in range(1,501):
            return False
        else:
            return True

    async def list_rooms(self):
        filter = {}
        data = self.room_db.find(filter,limit=500)
        res = await data.to_list(length=500)
        for x in res:
           x["id"] = x["_id"]
           x.pop("totalH")
        return res
    
    async def get_room_by_id(self, room_id):
        filter = {"_id": room_id}
        room = await self.room_db.find_one(filter)
        if room:
            room["id"] = room["_id"]
            room.pop("totalH")
            return room
        else:
            return False

    async def insert_room(self, room):
        if not self._check_timing(room["openingH"], room["closingH"]):
            raise InvalidTimingException
        if not self._check_capacity(room["capacity"]):
            raise InvalidCapacityException
        room["_id"] = room["id"]
        room.pop("id")
        room["totalH"]= room["closingH"]-room["openingH"]
        new_room = await self.room_db.insert_one(room)
        return await self.get_room_by_id(new_room.inserted_id)
    
    async def get_rooms_usage(self):
        filter = {}
        project = {"_id":1,"totalH":1}
        data_r = self.room_db.find(filter,project,limit=500)
        all_rooms = await data_r.to_list(length=500)
        data_br = self.booking_db.aggregate([{'$group':{'_id':'$idRoom','totalUsage':{'$sum':'$totalH'}}}])
        booked_rooms = await data_br.to_list(length=500)
        dicBR = {x["_id"]:x["totalUsage"]for x in booked_rooms}
        usages = []
        room = {}
        for x in all_rooms:
            if x["_id"] not in dicBR.keys():
                room = {
                    "id":x["_id"],
                    "usage": "0%",
                }
            else:
                room = {
                    "id":x["_id"],
                    "usage": str(round((100/x["totalH"])*dicBR[x["_id"]], 2))+"%",
                }
            usages.append(room)
        return usages
    
    async def get_room_status(self,roomId, hour):
        filter = {"idRoom": roomId}
        data = self.booking_db.find(filter, limit=500)
        all_bookings = await data.to_list(length=500)
        bookings= []
        if not all_bookings:
            return False
        else:
            for  x in all_bookings:
                if hour in range(x["initHour"], x["endHour"]):
                    bookings.append(x)
            return bookings
        
   


