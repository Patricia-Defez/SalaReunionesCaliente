from pydantic import BaseModel

class UserModel(BaseModel):
    id: str
    name: str

class ListUserModel(BaseModel):
    users: list[UserModel]
    count: int