import os


PG_URL = os.getenv('PG_URL', 'postgresql://postgres:admin@localhost/postgres')
RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost/')
RABBITMQ_EXCHANGE = os.getenv('RABBITMQ_EXCHANGE', 'messages')
SOURCE_ID = os.getenv('KEY', '1')
