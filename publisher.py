import json
import os
import random
from time import sleep

from app_config import fake, redis_connection, logger, sqs_queue


for i in range(100):
    phone_number = fake.phone_number()
    message = fake.sentence()

    if os.getenv("QUEUE") == "REDIS":
        redis_connection.rpush(os.getenv("CHANNEL_NAME"), json.dumps(dict(p=phone_number, m=message, i=i)))
        logger.info(f"PUBLICACAO ID: {i} FILA REDIS {redis_connection.llen(os.getenv('CHANNEL_NAME'))}")

    elif os.getenv("QUEUE") == "SQS" and sqs_queue:
        response = sqs_queue.send_message(
            MessageBody=json.dumps(dict(p=phone_number, m=message, i=i)),
            MessageGroupId=f"Group_{os.getenv('QUEUE')}"
        )
        logger.info(f"PUBLICACAO ID: {i} FILA SQS")
    else:
        raise NotImplemented()

    if os.getenv("PUBLISHER_DELAY"):
        sleep(random.uniform(0, float(os.getenv("DELAY"))))

