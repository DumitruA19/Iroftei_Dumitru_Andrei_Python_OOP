import time
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

for i in range(10):
    try:
        producer = KafkaProducer(bootstrap_servers="zookeeper-kafka:9092")
        print("✅ Kafka is available!")
        break
    except NoBrokersAvailable:
        print(f"❌ Kafka not ready... retrying ({i+1}/10)")
        time.sleep(5)
else:
    raise RuntimeError("❌ Could not connect to Kafka.")