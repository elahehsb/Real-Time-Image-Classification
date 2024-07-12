from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'image_classification_results',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    print(f"Received message: {message.value}")
