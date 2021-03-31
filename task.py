import os

from time import sleep

from app_config import celery_app, logger, redis_connection


@celery_app.task(name="push_data")
def push_data(phone, message):
    sleep(1)
    logger.info(f"Pushed {phone} - {message}")


if __name__ == "__main__":
    push_data.delay("11111111", "xxxxxxxxxx")