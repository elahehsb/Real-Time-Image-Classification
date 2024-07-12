from flask import Flask, request, jsonify
from kafka import KafkaProducer, KafkaConsumer
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import json
import io

app = Flask(__name__)

producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

model = ResNet50(weights='imagenet')

@app.route('/classify', methods=['POST'])
def classify_image():
    img = image.load_img(io.BytesIO(request.files['image'].read()), target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    predictions = model.predict(img_array)
    decoded_predictions = decode_predictions(predictions, top=3)[0]

    result = [{"label": label, "description": description, "score": float(score)} for label, description, score in decoded_predictions]

    producer.send('image_classification_results', value=result)

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
