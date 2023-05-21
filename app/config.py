import os

from dotenv import load_dotenv

load_dotenv()

USERNAME_MONGO = os.getenv("USERNAME_MONGO")
PASSWORD_MONGO = os.getenv("PASSWORD_MONGO")

DSN_MONGODB = f"mongodb://{USERNAME_MONGO}:{PASSWORD_MONGO}@db-mongo:27017/"
DSN_REDIS = "redis://db-redis:6379/1"


# DSN_MONGODB = "mongodb://127.0.0.1:27017/"
# DSN_REDIS = "redis://127.0.0.1:6379/2"



# DSN_MONGODB = os.getenv("DSN_MONGODB")
# CELERY_BROKER = os.getenv("CELERY_BROKER")
