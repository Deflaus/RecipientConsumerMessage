Инструкция по установке проекта:
-------------------------------

1)Установить docker и docker-compose:
docker https://docs.docker.com/engine/install/
docker-compose https://docs.docker.com/compose/install/;
2)Клонируем репозиторий с проектом;
3)Переходим в папку с проектом;
4)Открываем терминал в данной директории и прописываем команду "docker-compose up --build -d postgres rabbitmq" и затем команду "docker-compose up --build -d api worker".

После этих действий проект готов к работе.

API
-----------------

GET запросы:
1) url http://0.0.0.0:8080/messages/.
Возвращает список всех сообщений с их параметрами(id сообщения, получаетель, источник сообщения, статус сообщения, тело сообщения) в формате json;
2) url http://0.0.0.0:8080/messages/{id}, где id - id сообщения.
Возвращает информацию сообщения (id сообщения, получаетель, источник сообщения, статус сообщения, тело сообщения) по его id в формате json.

POST запрос:
url http://0.0.0.0:8080/webhooks/.
Принимает в теле запроса json. Формат сообщения:
{
    "recipient": "Deflaus",
    "body": "Привет, Deflaus",
}
Сохраняет сообщение в БД с принимаемыми параметрами, со статусом "new" и источником сообщения, который хранится в переменной окружения SOURCE_ID. Затем сообщение отправляется в rabbitmq в exchange messages с ключом равным источнику сообщения, добавив в тело сообщения его id. Ответ на запрос: id сообщения в БД (если успешно обработано), сообщение об ошибке (если возникла ошибка).

Worker
-------

При запуске создаёт очередь с именем '{source_id}-queue' и подписывает (bind) её на exchange 'messages' с заданным source-id.
Обрабатывает поступающие в эту очередь сообщения, а именно выводит на экран информацию о сообещнии(id сообщения, получаетель, источник сообщения, статус сообщения, тело сообщения) и устанавливает для обработанного сообщения  в БД статус "Обработано"("PROCESSED") и статус "Ошибка обработки"("ERRORPROCESS"), если сообщение содержит подстроку "9999".