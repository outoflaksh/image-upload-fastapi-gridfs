from pymongo import MongoClient
from gridfs import GridFS

import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get("MONGODB_URI")


def get_fs():
    client = MongoClient(MONGO_URI)

    try:
        client.admin.command("ping")
        print("Database connected successfully...")
    except Exception as e:
        print(e)

    db = client["images"]
    fs = GridFS(db)

    return fs
