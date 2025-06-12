from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI"))
db = client["split_app"]
expenses_collection = db["expenses"]
