from pymongo import MongoClient

conn = MongoClient("your url")
db = conn.baobad
ClientDO = db.clients
RoomDO = db.rooms
BookingDO = db.bookings

cliente1 = {"_id": "c1", "name": "Tomas"}
#x = ClientDO.insert_one(cliente1)
#print(x.inserted_id)
clients= [
    {"_id": "c2", "name": "Patri"},
    {"_id": "c3", "name": "Luis"},
    {"_id": "c4", "name": "Frank"},
    {"_id": "c5", "name": "Mira"},
    {"_id": "c6", "name": "Leon"},
    {"_id": "c7", "name": "Monica"},
    {"_id": "c8", "name": "Michelle"},
    {"_id": "c9", "name": "Daniel"},
    {"_id": "c10", "name": "Luz"}
]
#x = ClientDO.insert_many(clients)
"""""
res = ClientDO.find().sort("name")
for x in res:
    print(x)

rooms = [
    {"_id": "r1", "openigH": 8, "closingH": 22, "capacity": 20, "totalH": 14},
    {"_id": "r2", "openigH": 7, "closingH": 24, "capacity": 10, "totalH": 17},
    {"_id": "r3", "openigH": 8, "closingH": 22, "capacity": 30, "totalH": 14},
    {"_id": "r4", "openigH": 9, "closingH": 20, "capacity": 50, "totalH": 11},
    {"_id": "r5", "openigH": 8, "closingH": 22, "capacity": 25, "totalH": 14},
]
#x = RoomDO.insert_many(rooms)

res = RoomDO.find()
for x in res:
    print(x)
    """""