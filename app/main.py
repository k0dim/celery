from views import UpscaleView, TasksView, ProcessedView
from mapping import ApiError, error_handler
from app_celery import celery_app
from application import app

celery_app.conf.update(app.config)

app.add_url_rule("/upscale", view_func=UpscaleView.as_view("upscale"), methods=["POST"])
app.add_url_rule("/tasks/<string:task_id>", view_func=TasksView.as_view("tasks"), methods=["GET"])
app.add_url_rule("/processed/<string:filename>", view_func=ProcessedView.as_view("processed"), methods=["GET"])

app.errorhandler(ApiError)(error_handler)

# app.run(host='127.0.0.1', port=5000, debug=True)