# inventory_service/consumer.py

from kafka import KafkaConsumer
import json
import os
from sqlalchemy.orm import Session
from . import crud, schemas, database
import asyncio
import logging

logger = logging.getLogger(__name__)

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
TOPIC = 'book_events'

async def consume_events():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='inventory-service-group'
    )

    logger.info(f"Kafka consumer started for topic: {TOPIC}")

    loop = asyncio.get_event_loop()

    try:
        for message in consumer:
            event = message.value
            event_type = event.get('type')
            book_data = event.get('data')

            if not event_type or not book_data:
                logger.warning("Invalid event format received.")
                continue

            await handle_event(event_type, book_data)
    except asyncio.CancelledError:
        logger.info("Kafka consumer task cancelled.")
    except Exception as e:
        logger.error(f"Error in Kafka consumer: {e}")
    finally:
        consumer.close()

async def handle_event(event_type: str, book_data: dict):
    db_gen = database.get_db()
    db: Session = next(db_gen)
    try:
        if event_type == 'BOOK_CREATED':
            book_id = book_data.get('id')
            if book_id:
                # Initialize inventory with default quantity, e.g., 0
                existing_inventory = crud.get_inventory(db, book_id=book_id)
                if not existing_inventory:
                    inventory_create = schemas.InventoryCreate(book_id=book_id, quantity=0)
                    crud.create_inventory(db, inventory_create)
                    logger.info(f"Inventory created for book_id: {book_id}")
        elif event_type == 'BOOK_DELETED':
            book_id = book_data.get('id')
            if book_id:
                crud.delete_inventory(db, book_id=book_id)
                logger.info(f"Inventory deleted for book_id: {book_id}")
        # Handle other event types like 'BOOK_UPDATED' if necessary
    except Exception as e:
        logger.error(f"Error handling event {event_type}: {e}")
    finally:
        db.close()
