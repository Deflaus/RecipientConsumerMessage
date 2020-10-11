from aiohttp import web
from .views import get_list_messages, get_message, add_message


urlspatterns = [
    web.get('/messages/', get_list_messages),
    web.get('/messages/{id}', get_message),
    web.post('/messages/', add_message),
]