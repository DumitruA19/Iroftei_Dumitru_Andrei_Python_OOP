import json
import os
import time
from dotenv import load_dotenv
from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError, NoBrokersAvailable

load_dotenv()  # Încarcă variabilele din .env

KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "zookeeper-kafka:9092")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "logs")

MAX_RETRIES = 10
for i in range(MAX_RETRIES):
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("✅ KafkaProducer connected.")
        break
    except NoBrokersAvailable:
        print(f"❌ Kafka not ready... retrying ({i+1}/{MAX_RETRIES})")
        time.sleep(5)
else:
    raise RuntimeError("❌ Could not connect to Kafka.")

def log_to_kafka(data: dict):
    try:
        producer.send(KAFKA_TOPIC, value=data)
        print("📤 Kafka message sent.")
    except KafkaTimeoutError as e:
        print(f"❌ KafkaTimeoutError: {e}")
