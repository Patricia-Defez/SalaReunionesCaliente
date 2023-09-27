from fastapi import APIRouter
from models.clients import UserModel, ListUserModel
from controllers.clients import ClientController

client = APIRouter(prefix="/clients", tags=['Clients'])

@client.get("", response_model=ListUserModel)
def get_clients():
    cc= ClientController()
    users = cc.list_clients()
    return {"users": users, "count": len(users)}