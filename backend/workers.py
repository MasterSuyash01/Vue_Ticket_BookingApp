from celery import Celery, Task
from flask import Flask
def celery_init_app(app: Flask) -> Celery:
    class ContextTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=ContextTask)
    celery_app.conf.broker_url = 'redis://localhost:6379/1'
    celery_app.conf.result_backend='redis://localhost:6379/2'
    celery_app.conf.timezone="Asia/Kolkata"
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app