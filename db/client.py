from pymongo import AsyncMongoClient

class Client:
    def __init__(self, uri, db_name):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        if self.client is None:
            self.client = AsyncMongoClient(self.uri)
            self.db = self.client.get_database(self.db_name)
        return self.db
    
    async def close(self):
        if self.client:
            await self.client.close()
            self.client = None
            self.db = None
    
    
    
