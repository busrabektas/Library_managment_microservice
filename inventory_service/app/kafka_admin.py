from kafka.admin import KafkaAdminClient, NewTopic
import os

def create_kafka_topic(topic_name):
    admin_client = KafkaAdminClient(
        bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092'),
        client_id='inventory_service_admin'
    )

    topic_list = [NewTopic(name=topic_name, num_partitions=1, replication_factor=1)]
    try:
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
    except Exception as e:
        # Zaten mevcutsa hata verebilir, bunu göz ardı edebiliriz
        pass
    finally:
        admin_client.close()
