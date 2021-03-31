import logging
import os

import boto3
from celery import Celery
import redis
import faker
import dotenv

fake = faker.Faker()
dotenv.load_dotenv()

redis_connection = redis.Redis.from_url(os.getenv("REDIS_PUBSUB_URL"))
celery_app = Celery(broker=os.getenv("REDIS_CELERY_URL"))
logger = logging.getLogger("redis_queue")
logging.basicConfig(level="INFO")

if os.getenv("QUEUE") == "SQS":
    sqs = boto3.resource(
        'sqs',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION")
    )
    sqs_queue = sqs.get_queue_by_name(QueueName=os.getenv("QUEUE_NAME"))
else:
    sqs_queue = None
