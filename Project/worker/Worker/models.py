from gino import Gino
from enum import Enum


db = Gino()


class MessageStatus(Enum):
    NEW = 'new'
    PROCESSED = 'processed'
    ERRORPROCESS = 'errorprocess'


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer(), primary_key=True)
    recipient = db.Column(db.Unicode(), nullable=False)
    source = db.Column(db.Integer(), nullable=False)
    status = db.Column(db.Enum(MessageStatus), nullable=False)
    body = db.Column(db.Unicode(), nullable=False)