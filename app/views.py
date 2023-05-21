
from flask import jsonify, request
from flask.views import MethodView

from mapping import ApiError
from validation import validation
from mongodb import flasc_send_file, flasc_put_file, mongo_put, mongo_send
from app_celery import get_task, start_upscale, tasks
from log import logger


class UpscaleView(MethodView):
    
    def post(self):
        logger.info(f"Start POST /upscale/")

        if not request.files.get("file"):
            raise ApiError(400, "File not found")

        image_file = validation(request.files.get("file"))
        image_file = flasc_put_file(image_file, mongo_put)
        logger.info(f"{image_file}")
        task = start_upscale.delay(image_file)

        return jsonify({"status": task.status, "task_id": task.id})


class TasksView(MethodView):
    
    def get(self, task_id):
        task = get_task(task_id)

        return jsonify({"status": task.status, "result": task.result})


class ProcessedView(MethodView):
    
    def get(self, filename):
        logger.info(f"Start GET /filename/")
        logger.info(f"filename - {filename}")
        return flasc_send_file(filename, mongo_send)