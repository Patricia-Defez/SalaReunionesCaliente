from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from models.rooms import RoomModel, ListRoomModel
from controllers.rooms import RoomController
from samples.rooms import post_room_example

room = APIRouter(prefix="/rooms", tags=["Rooms"])

@room.get("", response_model=ListRoomModel)
def list_all_rooms():
    rc = RoomController()
    rooms = rc.list_rooms()
    return {'rooms': rooms, "count": len(rooms)}

@room.get("/{id}", response_model=RoomModel)
def get_room_by_Id(id):
    rc = RoomController()
    room = rc.get_room_by_id(id)
    if room:
        return room
    else:
        raise HTTPException (
            status_code = 404, 
            detail = "Room not found"
        )

@room.post("")
def create_new_room(room: RoomModel = Body(post_room_example)):
    rc = RoomController()
    new_room = None
    try:
        new_room = rc.insert_room(jsonable_encoder(room))
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
def get_rooms_usage():
    return "usage"