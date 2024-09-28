
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'loan_events',
    bootstrap_servers='kafka:9092',  # Docker dışından erişim için
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def consume_loan_events():
    for message in consumer:
        event_data = message.value
        print(f"Received event: {event_data}")
        
        if event_data['type'] == 'loan_created':
            loan_data = event_data['loan']
            print(f"Processing loan event for Book ID: {loan_data['book_id']}")
            # Burada kitapla ilgili işlem yapılabilir (örneğin, stok güncellemesi)

# Event tüketimi başlat
if __name__ == "__main__":
    consume_loan_events()
