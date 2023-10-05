from config.db import ClientDO


class ClientController:
    def __init__(self):
        self.client_db = ClientDO

    async def list_clients(self):
        filter ={}
        data = self.client_db.find(filter,limit=500)
        res = await data.to_list(length=500)
        for x in res:
           x["id"] = x["_id"]
        return res

    async def get_client_by_id(self, client_id):
        filter = {"_id":client_id}
        client = await self.client_db.find_one(filter)
        if client:
            return client
        else:
            return False    
