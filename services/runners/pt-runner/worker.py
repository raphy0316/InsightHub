from celery import Celery
import os

app = Celery("runner",
             broker=os.environ["CELERY_BROKER_URL"],
             backend=os.environ["CELERY_BACKEND_URL"])
