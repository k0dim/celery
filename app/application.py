from flask import Flask
from celery import Celery

import config
from log import logger


app_name = "app"

app = Flask(app_name)