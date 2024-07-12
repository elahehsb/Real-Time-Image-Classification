import pandas as pd
import matplotlib.pyplot as plt
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'image_classification_results',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

results = []

for message in consumer:
    results.append(message.value)

df = pd.DataFrame(results)

# Visualize the data
plt.figure(figsize=(10, 6))
df['label'].value_counts().plot(kind='bar')
plt.title('Image Classification Results')
plt.xlabel('Label')
plt.ylabel('Frequency')
plt.show()
