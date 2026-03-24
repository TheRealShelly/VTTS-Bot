from pymongo.database import Database

class TTSRepository:
    def __init__(self, db: Database):
        self.collection = db.get_collection("TTS")

        