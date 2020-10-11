import asyncio
import aio_pika
from Worker.config import PG_URL, RABBITMQ_URL, RABBITMQ_EXCHANGE, SOURCE_ID
from Worker.models import db, Message, MessageStatus
import json


async def treatment_message(message: aio_pika.IncomingMessage):
    with message.process():
        data = json.loads(message.body.decode())
        print(data)
        obj_message = await Message.get(data['id'])
        if '9999' in data['body']:
            await obj_message.update(status=MessageStatus.ERRORPROCESS).apply()
        else:
            await obj_message.update(status=MessageStatus.PROCESSED).apply()


async def main():
    await db.set_bind(PG_URL)
    await db.gino.create_all()

    connection = await aio_pika.connect(RABBITMQ_URL)
    channel = await connection.channel()
    exchange = await channel.declare_exchange(
        RABBITMQ_EXCHANGE,
        aio_pika.ExchangeType.DIRECT,
    )

    queue = await channel.declare_queue('{}-queue'.format(SOURCE_ID))

    await queue.bind(exchange, routing_key=SOURCE_ID)
    await queue.consume(treatment_message)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
