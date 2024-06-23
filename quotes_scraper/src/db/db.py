from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi
from functools import wraps

client = MongoClient(
    "mongodb+srv://elbereth7:%23MakeDealWithTheGod7@cluster0.ij6jt6y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi("1"),
)

db = client.quotes


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
def import_quotes(quotes: list):
    result = db.qoutes.insert_many(quotes)
    return result.inserted_ids


@handle_mongo_exceptions
def import_authors(authors: list):
    result = db.authors.insert_many(authors)
    return result.inserted_ids
