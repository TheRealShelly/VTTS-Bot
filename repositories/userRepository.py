from pymongo import ReturnDocument
from pymongo.database import Database

class UserRepository:
    def __init__(self, db: Database):
        self.collection = db.get_collection("Users")

    async def getUser(self, id: int): # create and read
        try:
            user = await self.collection.find_one_and_update(
                {"id": id},
                {"$setOnInsert": {"id": id, "daily": 0, "atm": 0}},
                return_document=ReturnDocument.AFTER,
                upsert=True
            )
            return user
        except Exception as e:
            print(f"error fetching/adding user to database. \
                  \n{e.__class__.__name__}: {e}")
            return None

    async def updateUser(self, id: int, fields): # update
        try:
            user = await self.collection.update_one(
                {"id": id},
                {"$set": fields}
            )
            return user
        except Exception as e:
            print(f"error updating user on database. \
                  \n{e.__class__.__name__}: {e}")
            return None

    async def deleteUser(self, id: int): # delete
        try:
            user = await self.collection.delete_one({"id": id})
            return user
        except Exception as e:
            print(f"error deleting user on database. \
                  \n{e.__class__.__name__}: {e}")
            return None