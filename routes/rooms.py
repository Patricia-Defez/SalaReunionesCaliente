from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from models.rooms import RoomModel, ListRoomModel
from controllers.rooms import RoomController
from samples.rooms import post_room_example

room = APIRouter(prefix="/rooms", tags=["Rooms"])

@room.get("", response_model=ListRoomModel)
async def list_all_rooms():
    rc = RoomController()
    rooms = await rc.list_rooms()
    if not rooms:
        raise HTTPException(
             status_code= 404,
             detail= "No rooms found"
        )
    else:
        return {'rooms': rooms, "count": len(rooms)}

@room.get("/{id}/byId", response_model=RoomModel)
async def get_room_by_Id(id: str):
    rc = RoomController()
    room = await rc.get_room_by_id(id)
    if room:
        return room
    else:
        raise HTTPException (
            status_code = 404, 
            detail = "Room not found"
        )

@room.post("")
async def create_new_room(room: RoomModel = Body(post_room_example)):
    rc = RoomController()
    new_room = None
    try:
        new_room = await rc.insert_room(jsonable_encoder(room))
        new_room.pop('_id', None)
        
    except Exception as e:
        error = e.__class__.__name__
        if error == "DuplicateKeyError":
            raise HTTPException(
                status_code = 400,
                detail = "Duplicated room id"
            )
        if error == "InvalidTimingException":
            raise HTTPException(
                status_code = 400,
                detail = "Invalid timing"
            )
        if error == "InvalidCapacityException":
            raise HTTPException(
                status_code = 400,
                detail = "Invalid room capacity"
            )
    if new_room:
        return new_room

@room.get("/usage")
async def get_rooms_usage():
    rc = RoomController()
    usages = await rc.get_rooms_usage()
    return usages

@room.get("/{roomId}/room/{hour}/status")
async def get_room_status(roomId:str, hour:int):
    rc = RoomController()
    bookings = await rc.get_room_status(roomId, hour)
    if bookings:
        status = {
            "room": roomId,
            "hour": hour,
            "status": "booked"
        }
    else:
        status = {
            "room": roomId,
            "hour": hour,
            "status": "Not booked"
        }
    return status
