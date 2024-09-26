
from kafka import KafkaProducer
import json
import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_book_event(event_type, book_data):
    producer.send('book_events', {'type': event_type, 'data': book_data})
    producer.flush()
