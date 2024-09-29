import os
import json
from kafka import KafkaConsumer
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, schemas
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')


user_cache = {}

def consume_user_events():
    TOPIC = 'user_events'
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='loan-service-user-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    logger.info("Loan Service: User Events Consumer started")
    for message in consumer:
        event = message.value
        event_type = event.get('type')
        data = event.get('data')

        logger.info(f"Loan Service: Received event {event_type} with data {data}")

        if event_type == 'USER_CREATED':
            user_cache[data['id']] = data
            logger.info(f"Loan Service: User created - {data['id']}")
        elif event_type == 'USER_UPDATED':
            user_cache[data['id']] = data
            logger.info(f"Loan Service: User updated - {data['id']}")
        elif event_type == 'USER_DELETED':
            if data['id'] in user_cache:
                del user_cache[data['id']]
                logger.info(f"Loan Service: User deleted - {data['id']}")

def consume_loan_events():
    TOPIC = 'loan_events'
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='loan-service-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    logger.info("Loan Service: Loan Events Consumer started")
    for message in consumer:
        event = message.value
        event_type = event.get('type')
        data = event.get('loan')

        logger.info(f"Loan Service: Received event {event_type} with data {data}")

        db: Session = SessionLocal()
        try:
            if event_type == 'LOAN_CREATED':
                book_id = data.get('book_id')
                if book_id:
                    crud.decrement_inventory(db, book_id=book_id)
                    logger.info(f"Loan Service: Decreased inventory for book ID {book_id}")
            elif event_type == 'LOAN_RETURNED':
                book_id = data.get('book_id')
                if book_id:
                    crud.increment_inventory(db, book_id=book_id)
                    logger.info(f"Loan Service: Increased inventory for book ID {book_id}")
        except Exception as e:
            logger.error(f"Loan Service: Error processing loan event {event_type}: {e}")
        finally:
            db.close()
