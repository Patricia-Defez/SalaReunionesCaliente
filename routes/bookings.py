from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from models.bookings import BookingModel
from controllers.bookings import BookingController
from samples.bookings import post_booking_example

booking = APIRouter(prefix="/booking", tags=['Bookings'])

@booking.get("")
def get_bookings():
    return "Bookings"

@booking.post("")
def create_new_booking(booking: BookingModel = Body(post_booking_example)):
    bc = BookingController()
    new_booking = None
    try:
        new_booking = bc.insert_booking(jsonable_encoder(booking))
        new_booking.pop('_id', None)

    except Exception as e:
        error = e.__class__.__name__
        if error == "NoRoomException":
            raise HTTPException(
                status_code = 400,
                detail = f"No room found with id {booking['idRoom']}"
            )
        if error == "NoClientException":
            raise HTTPException(
                status_code = 400,
                detail = f"No client found with id {booking['idClient']}"
            )
        if error == "InvalidTimingException":
            raise HTTPException(
                status_code = 400,
                detail = "the timing does not match the room schedule"
            )
    if new_booking:
        return new_booking

@booking.get("/{clientId}/bookings")
def get_bookings_by_client_id(clientId):
    return "Bookings"

@booking.get("/{roomId}/bookings")
def get_bookings_by_room_id(roomId):
    return "Bookings"

@booking.get("/bookingsByClients")
def get_bookings_by_clients():
    return "BookingsByClients"