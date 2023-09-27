from fastapi import FastAPI
from routes.rooms import room
from routes.clients import client
from routes.bookings import booking

app = FastAPI(
    title='La sala de reuniones caliente',
    description='Prueba técnica para Baobab Soluciones',
)

app.include_router(room)
app.include_router(client)
app.include_router(booking)