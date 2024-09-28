from kafka import KafkaConsumer
import json
import os
from .database import SessionLocal
from app import crud, schemas

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')

consumer = KafkaConsumer(
    'book_events',
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    event = message.value
    event_type = event['type']
    book_data = event['data']

    db = SessionLocal()
    if event_type == 'created':
        book = schemas.BookCreate(**book_data)
        crud.create_book(db, book)
    elif event_type == 'updated':
        # Güncelleme işlemi
        pass
    elif event_type == 'deleted':
        # Silme işlemi
        pass
    db.close()
