
from typing import Union
from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from models.bookings import BookingModel, ListBookingModel
from controllers.bookings import BookingController,NoRoomException, NoClientException, InvalidTimingException
from samples.bookings import post_booking_example

booking = APIRouter(prefix="/booking", tags=['Bookings'])

@booking.get("", response_model= Union[ListBookingModel, None])
def list_all_bookings():
    bc = BookingController()
    bookings = []
    bookings = bc.list_bookings()
    if not bookings:
        raise HTTPException(
             status_code= 404,
             detail= "No booking found"
        )
    else:
        return {'bookings': bookings, 'count': len(bookings)}

@booking.post("")
def create_new_booking(booking: BookingModel = Body(post_booking_example)):
    bc = BookingController()
    new_booking = None
    try:
        new_booking = bc.insert_booking(jsonable_encoder(booking))
        new_booking.pop('_id', None)

    except NoRoomException:
            raise HTTPException(
                status_code = 400,
                detail = "No room found with that id"
            )
    except NoClientException:
            raise HTTPException(
                status_code = 400,
                detail = "No client found with that id"
            )
    except InvalidTimingException:
            raise HTTPException(
                status_code = 400,
                detail = "the timing does not match the room schedule"
            )
    if new_booking:
        return new_booking

@booking.get("/{clientId}/bookingsClient", response_model= Union[ListBookingModel, None])
def list_bookings_by_client_id(clientId: str):
    bc = BookingController()
    bookings = []
    try:
         bookings = bc.list_bookings_by_client_id(clientId)
    except NoClientException:
        raise HTTPException(
                status_code = 400,
                detail = "No client found with that id"
            )
    if not bookings:
        raise HTTPException(
             status_code= 404,
             detail= "No booking found"
        )
    else:  
        return {'bookings': bookings, 'count': len(bookings)}

@booking.get("/{roomId}/bookingsRoom", response_model= Union[ListBookingModel, None])
def list_bookings_by_room_id(roomId: str):
    bc = BookingController()
    bookings = []
    try:
         bookings = bc.list_bookings_by_room_id(roomId)
    except NoRoomException:
            raise HTTPException(
                status_code = 400,
                detail = "No room found with that id"
            )
    if not bookings:
        raise HTTPException(
             status_code= 404,
             detail= "No booking found"
        )
    else:
        return {'bookings': bookings, 'count': len(bookings)}

@booking.get("/bookingsByClients")
def get_bookings_by_clients():
    bc = BookingController()
    aggregate = []
    aggregate = bc.get_bookings_by_clients()
    if not aggregate:
         raise HTTPException(
             status_code= 404,
             detail= "No bookings found"
        )
    else:     
        return aggregate
    
@booking.get("/{roomId}/overlappedBookings")
def list_overlapped_bookings(roomId: str):
     bc = BookingController()
     overlapped = []
     return "overlapped"