import json
import os
from app_config import redis_connection, logger, celery_app, sqs_queue
from task import push_data


@celery_app.task("subscriber")
def subscriber():
    if os.getenv("QUEUE") == "REDIS":

        while True:
            message = redis_connection.lpop(os.getenv("CHANNEL_NAME"))
            if message:
                message = json.loads(message.decode("utf-8"))
                if 'p' in message and message['p'] and 'm' in message and message['m']:
                    logger.info(f"RECEBENDO REDIS({redis_connection.llen(os.getenv('CHANNEL_NAME'))}) {message['p']}, {message['m']}")
                    push_data.delay(message['p'], message['m'])
            else:
                logger.info(f"Waiting...")

    elif os.getenv("QUEUE") == "SQS":

        while True:
            for message in sqs_queue.receive_messages(MaxNumberOfMessages=10):
                message_dict = json.loads(message.body)
                if 'i' in message_dict:
                    logger.info(f"RECEBENDO SQS ID: {message_dict['i']}, {message_dict['p']}, {message_dict['m']}")
                else:
                    logger.info(f"RECEBENDO SQS {message_dict['p']}, {message_dict['m']}")
                push_data.delay(message_dict['p'], message_dict['m'])
                message.delete()
