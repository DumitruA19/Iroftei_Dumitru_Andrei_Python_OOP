import json
import sqlite3
import time
import os
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from dotenv import load_dotenv

load_dotenv()

TOPIC = os.environ.get("KAFKA_TOPIC", "logs")
BOOTSTRAP_SERVERS = [os.environ.get("KAFKA_BROKER", "zookeeper-kafka:9092")]
SQLITE_DB = os.environ.get("SQLITE_DB", "events.db")
GROUP_ID = os.environ.get("KAFKA_GROUP_ID", "event-logger")
RETRY_DELAY = 5
MAX_RETRIES = 10

conn = sqlite3.connect(SQLITE_DB)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS kafka_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        message TEXT
    )
''')
conn.commit()

print("📦 Initialized SQLite:", SQLITE_DB)

consumer = None
for attempt in range(1, MAX_RETRIES + 1):
    try:
        consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=BOOTSTRAP_SERVERS,
            group_id=GROUP_ID,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest'
        )
        print("✅ KafkaConsumer connected.")
        break
    except NoBrokersAvailable:
        print(f"❌ Kafka not available... retrying in {RETRY_DELAY}s ({attempt}/{MAX_RETRIES})")
        time.sleep(RETRY_DELAY)

if consumer is None:
    raise RuntimeError("❌ Could not connect to Kafka after multiple retries.")

print("🚀 Kafka consumer started and listening to topic:", TOPIC)

for message in consumer:
    print(f"📩 Received message from topic '{message.topic}': {message.value}")
    cursor.execute(
        "INSERT INTO kafka_logs (topic, message) VALUES (?, ?)",
        (message.topic, json.dumps(message.value))
    )
    conn.commit()