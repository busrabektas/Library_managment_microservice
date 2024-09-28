# # inventory_service/kafka_admin.py

# from kafka.admin import KafkaAdminClient, NewTopic
# import os
# import logging

# logger = logging.getLogger(__name__)

# KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')

# def create_kafka_topic(topic_name: str, num_partitions: int = 1, replication_factor: int = 1):
#     admin_client = KafkaAdminClient(
#         bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
#         client_id='inventory-service'
#     )
#     topic_list = [NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)]
#     try:
#         admin_client.create_topics(new_topics=topic_list, validate_only=False)
#         logger.info(f"Kafka topic '{topic_name}' created successfully.")
#     except Exception as e:
#         if 'TopicAlreadyExistsError' in str(e):
#             logger.info(f"Kafka topic '{topic_name}' already exists.")
#         else:
#             logger.error(f"Failed to create Kafka topic '{topic_name}': {e}")
#     finally:
#         admin_client.close()
