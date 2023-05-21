from celery import Celery
from celery.result import AsyncResult
from mongodb import get_file_put, flasc_send_file, mongo_put
from application import app, app_name
from upscale.upscale import Upscale
import config
from log import logger


celery_app = Celery(app_name, backend=config.DSN_MONGODB, broker=config.DSN_REDIS)
celery_app.conf.update(app.config)


class ContextTask(celery_app.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


celery_app.Task = ContextTask


def get_task(task_id: str) -> AsyncResult:
    logger.info(f"{task_id}")
    return AsyncResult(task_id, app=celery_app)


@celery_app.task
def start_upscale(data: dict):
    try:
        logger.info(f"Start task upscale - {data['filename']}")
        img = get_file_put(data["id"])
        
        logger.info(f"{img}")
        return Upscale.get_instance().upscale(img, data['filename'])
    except Exception as exc:
        logger.error(f"{exc}")


def tasks():
    tasks = celery_app.tasks.keys()