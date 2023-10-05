from fastapi import APIRouter, HTTPException
from models.clients import UserModel, ListUserModel
from controllers.clients import ClientController

client = APIRouter(prefix="/clients", tags=['Clients'])

@client.get("", response_model=ListUserModel)
async def get_clients():
    cc= ClientController()
    clients = await cc.list_clients()
    if not clients:
        raise HTTPException(
             status_code= 404,
             detail= "No clients found"
        )
    else:
        return {"users": clients, "count": len(clients)}