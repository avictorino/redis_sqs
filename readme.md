#### Summary
The goal is to improve performance by decreasing the microservice resources usage and performs integrations in the shortest time.
The company expects to expand and it will not be possible to reach a demand of approximately 1 million shipments, currently in the range of 100,000 and hundreds of workers running in a matter of hours.

#### Emergency solution
After the DevOps team increase vertically the number of workers instances within the process peak period, my suggestion to not rewrite the full application in a week is to multiply the number of SQSs queues, once the problem is the read operation from a unique queue. Each consumer added to the cluster would have the capacity multiplied by the number of queues to pull messages in parallel. Anyway the read improvement brings performance problems to the executor since the CPU usage will increase requiring a multitread solution to spread the processing load.

#### Definitive solution
Redis offers a great FIFO queue solution (rpush/lpop) from which it achieves a high IOPS level and its performance is recognized and widely used for real-time systems. A consumer was implemented in Python, already foreseeing multiple workers scalability. After each message read the consumer starts a delayed celery task to be executed in another cluster, which is also horizontally scalable.

#### Repository architecture
Some microservices were developed to spread the load into each local block.  Two queues server implementations comparison the performance, that could be switched by the feature-flag QUEUE = SQS | REDIS in the .env config file.

**publisher.py** - script that simulates sending messages, batches of 100, 1000, 10000, 500000, basically a "for" without sleep() to fill the queue server with many messages as possible.

    if os.getenv ("QUEUE") == "REDIS":
        redis.rpush (os.getenv ("CHANNEL_NAME"), json.dumps (dict (p = phone_number, m = message, i = i)))
    elif os.getenv ("QUEUE") == "SQS":
        response = sqs_queue.send_message (MessageBody = json.dumps (dict (p = phone_number, m = message, i = i)))

**subscriber.py** - scalable message receiver, that reads from the queue server and starts Celery tasks for later execution.
    
    if os.getenv("QUEUE") == "REDIS":
        message = redis.lpop(os.getenv("CHANNEL_NAME"))
        message_dict = json.loads(message.decode("utf-8"))
    elif os.getenv("QUEUE") == "SQS":
        for message in sqs_queue.receive_messages(MaxNumberOfMessages=10):
            message_dict = json.loads(message.body)
            
    push_data.delay(message_dict['p'], message_dict['m'])

**task.py** - celery task executor, that simulates a request.post, that takes 1 second to finish the execution (even though this communication should be async)

Today, this queue publication is sent by many legacy systems, including in different languages, letting all write operations centralized in REDIS.  Redis can store 4,294,967,295, making the storage size enough if an outage happens. Using LPOP to get the first item on the list and safely remove, since this operation is a single thread within the REDIS context.

To execute this program you will need:

    * Docker
    * Redis Server
    * SQS queue - if you will connect there 
    * Edit .env with your variables
    * Execute the following command line:
    
    docker-compose up
