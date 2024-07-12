import json
import time
from kafka import KafkaProducer
import requests

producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def send_image(image_path):
    with open(image_path, 'rb') as f:
        response = requests.post('http://localhost:5000/classify', files={'image': f})

    producer.send('image_requests', value=response.json())

if __name__ == '__main__':
    while True:
        send_image('path/to/image.jpg')
        time.sleep(5)
