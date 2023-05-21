from pymongo.mongo_client import MongoClient
from gridfs import GridFS
from PIL import Image
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from application import app
import config

from werkzeug.datastructures import FileStorage


mongo_put = PyMongo(app, uri=config.DSN_MONGODB + "put")
mongo_send = PyMongo(app, uri=config.DSN_MONGODB + "send")


def get_fs(DSN: str) -> GridFS:
    mongo = MongoClient(DSN)
    return GridFS(mongo["put"])


def get_file_put(fileid):
    files = get_fs(config.DSN_MONGODB)
    return files.get(ObjectId(fileid))


def flasc_put_file(file: FileStorage, mongo: PyMongo, filename = None):
    if not filename:
        filename = file.filename
    fileid = mongo.save_file(filename=filename, fileobj=file)
    return {
        "id": str(fileid),
        "filename": filename
    }


def flasc_send_file(filename, mongo: PyMongo):
    return mongo.send_file(filename)