from config.db import ClientDO


class ClientController:
    def __init__(self):
        self.client_db = ClientDO

    def list_clients(self):
        filter ={}
        res = list(self.client_db.find(filter,limit=500))
        for x in res:
           x["id"] = x["_id"]
        return res

    def get_client_by_id(self, client_id):
        filter = {"_id":client_id}
        client = self.client_db.find_one(filter)
        if client:
            return client
        else:
            return False    
