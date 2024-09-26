# from confluent_kafka import Producer
# import os

# KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "kafka:9092")
# KAFKA_TOPIC = "book_updates"

# p = Producer({'bootstrap.servers': KAFKA_BROKER_URL})

# def delivery_report(err, msg):
#     """ Mesaj gönderim durumu. """
#     if err is not None:
#         print(f"Message delivery failed: {err}")
#     else:
#         print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# def send_book_update(book_data):
#     p.produce(KAFKA_TOPIC, key="book_update", value=str(book_data), callback=delivery_report)
#     p.flush()  # Tüm mesajların gönderilmesini bekler

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
