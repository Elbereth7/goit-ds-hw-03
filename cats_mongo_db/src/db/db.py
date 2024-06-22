from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi
from functools import wraps

client = MongoClient(
    "mongodb+srv://elbereth7:%23MakeDealWithTheGod7@cluster0.ij6jt6y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi("1"),
)

db = client.book

def handle_mongo_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except errors.PyMongoError as e:
            print(f"An error occurred: {e}")
            return None
    return wrapper

@handle_mongo_exceptions
def add_new_cat(name: str):
    result_one = db.cats.insert_one({"name": name})
    return result_one.inserted_id

@handle_mongo_exceptions
def read_by_name(name: str):
    return db.cats.find_one({"name": name})

@handle_mongo_exceptions
def read_all():
    return db.cats.find({})

@handle_mongo_exceptions
def update_age(name: str, age: int):
    db.cats.update_one({"name": name}, {"$set": {"age": age}})
    return db.cats.find_one({"name": name})

@handle_mongo_exceptions
def update_features(name: str, feature: str): 
    db.cats.update_one({"name": name}, {"$addToSet": {"features": feature}})
    return db.cats.find_one({"name": name})

@handle_mongo_exceptions
def delete_by_name(name: str):
    db.cats.delete_one({"name": name})
    return db.cats.find_one({"name": name})

@handle_mongo_exceptions
def delete_all():
    return db.cats.delete_many({})
