from kafka import KafkaProducer
import json

# Kafka sunucusunun adresini ayarlayın
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'  # Eğer Docker'dan çalışıyorsanız 'kafka:9092' kullanabilirsiniz

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Test mesajı gönderme
try:
    producer.send('book_events', {'type': 'TEST_EVENT', 'data': {'title': 'Test Book', 'author': 'Test Author'}})
    producer.flush()
    print("Test mesajı başarıyla gönderildi!")
except Exception as e:
    print(f"Mesaj gönderimi başarısız oldu: {e}")
