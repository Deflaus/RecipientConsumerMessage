import aiohttp
from .models import db, Message, MessageStatus
from .config import SOURCE_ID
import json
import aio_pika


async def get_list_messages(request):
    all_messages = await Message.query.gino.all()
    json_response = {}
    for message in all_messages:
        wordlist = {
            'id': message.id,
            'recipient': message.recipient,
            'source': message.source,
            'status': message.status.value,
            'body': message.body,
        }
        json_response[message.id] = wordlist
    return aiohttp.web.json_response(
        json_response
    )


async def get_message(request):
    try:
        id = int(request.match_info['id'])
    except ValueError:
        return aiohttp.web.json_response(
            {
                'error': 'Message id is not valid'
            },
            status=400
        )

    # BD
    message = await Message.query.where(Message.id == id).gino.first()
    if message is None:
        json_response = {
                            'error': 'Message not founded'
                        }
    else:
        json_response = {
            'id': id,
            'recipient': message.recipient,
            'source': message.source,
            'status': message.status.value,
            'body': message.body,
        }

    return aiohttp.web.json_response(
        json_response
    )


async def add_message(request):
    try:
        data = await request.json()
    except json.decoder.JSONDecodeError:
        return aiohttp.web.json_response(
            {
                'error': 'Error of message',
            },
            status=400,
        )

    # BD
    message_recipient = data['recipient']
    message_body = data['body']

    message = await Message.create(
        recipient = message_recipient,
        source = int(SOURCE_ID),
        status = MessageStatus.NEW,
        body = message_body,
    )

    # RabbitMQ
    json_response = {
        'id': message.id,
        'recipient': message_recipient,
        'source': int(SOURCE_ID),
        'status': message.status.value,
        'body': message_body,
    }
    json_response = json.dumps(json_response).encode()
    exchange = request.app['exchange']
    mes = aio_pika.Message(json_response)
    await exchange.publish(mes, routing_key=SOURCE_ID)

    return aiohttp.web.json_response(
        {
            'id' : message.id,
        },
        status=200,
    )