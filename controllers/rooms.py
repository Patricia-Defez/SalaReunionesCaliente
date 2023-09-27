from config.db import RoomDO

class InvalidTimingException(Exception):
    pass

class InvalidCapacityException(Exception):
    pass

class RoomController:
    def __init__(self):
        self.room_db = RoomDO

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

    def list_rooms(self):
        filter = {}
        res = list(self.room_db.find(filter,limit=500))
        for x in res:
           x["id"] = x["_id"]
           x.pop("totalH")
        return res
    
    def get_room_by_id(self, room_id):
        filter = {"_id": room_id}
        room = self.room_db.find_one(filter)
        if room:
            room["id"] = room["_id"]
            room.pop("totalH")
            return room
        else:
            return False

    def insert_room(self, room):
        if not self._check_timing(room["openingH"], room["closingH"]):
            raise InvalidTimingException
        if not self._check_capacity(room["capacity"]):
            raise InvalidCapacityException
        room["_id"] = room["id"]
        room.pop("id")
        room["totalH"]= room["closingH"]-room["openingH"]
        new_room = self.room_db.insert_one(room)
        return self.get_room_by_id(new_room.inserted_id)
