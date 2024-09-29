# inventory_service/consumer.py

import os
import json
from kafka import KafkaConsumer
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, schemas
import logging

# Logging ayarları
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')

def consume_book_events():
    TOPIC = 'book_events'
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='inventory-service-book-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    logger.info("Inventory Service: Book Events Consumer started")
    for message in consumer:
        event = message.value
        event_type = event.get('type')
        data = event.get('data')
        
        logger.info(f"Inventory Service: Received event {event_type} with data {data}")
        
        db: Session = SessionLocal()
        try:
            if event_type == 'BOOK_CREATED':
                # Yeni kitap için stok oluştur
                inventory_create = schemas.InventoryCreate(book_id=data['id'], quantity=10)  # Varsayılan miktar
                crud.create_inventory(db, inventory_create)
                logger.info(f"Inventory Service: Created inventory for book ID {data['id']}")
            elif event_type == 'BOOK_DELETED':
                book_id = data.get('id')
                if book_id:
                    try:
                        updated_inventory = crud.update_inventory_quantity(db, book_id=book_id, quantity_change=-1)
                        if updated_inventory:
                            logger.info(f"Inventory Service: Decreased stock for book ID {book_id}. New quantity: {updated_inventory.quantity}")
                        else:
                            logger.info(f"Inventory Service: Inventory for book ID {book_id} deleted as quantity reached zero.")
                    except ValueError as ve:
                        logger.error(f"Inventory Service: {ve}")
        except Exception as e:
            logger.error(f"Inventory Service: Error processing book event {event_type}: {e}")
        finally:
            db.close()

def consume_loan_events():
    TOPIC = 'loan_events'
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='inventory-service-loan-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    logger.info("Inventory Service: Loan Events Consumer started")
    for message in consumer:
        event = message.value
        event_type = event.get('type')
        data = event.get('loan')
        
        logger.info(f"Inventory Service: Received event {event_type} with data {data}")
        
        db: Session = SessionLocal()
        try:
            if event_type == 'BOOK_LOANED':
                book_id = data.get('book_id')
                if book_id:
                    try:
                        updated_inventory = crud.update_inventory_quantity(db, book_id=book_id, quantity_change=-1)
                        if updated_inventory:
                            logger.info(f"Inventory Service: Decreased stock for book ID {book_id}. New quantity: {updated_inventory.quantity}")
                        else:
                            logger.info(f"Inventory Service: Inventory for book ID {book_id} deleted as quantity reached zero.")
                    except ValueError as ve:
                        logger.error(f"Inventory Service: {ve}")
            elif event_type == 'BOOK_RETURNED':
                book_id = data.get('book_id')
                if book_id:
                    try:
                        updated_inventory = crud.update_inventory_quantity(db, book_id=book_id, quantity_change=1)
                        logger.info(f"Inventory Service: Increased stock for book ID {book_id}. New quantity: {updated_inventory.quantity if updated_inventory else 'N/A'}")
                    except ValueError as ve:
                        logger.error(f"Inventory Service: {ve}")
        except Exception as e:
            logger.error(f"Inventory Service: Error processing loan event {event_type}: {e}")
        finally:
            db.close()
