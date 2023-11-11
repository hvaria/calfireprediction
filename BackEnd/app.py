from flask import Flask, request, jsonify
from flask import send_file
from flask_cors import CORS
from flask import send_from_directory
import subprocess
import requests
import ImageMapPulling
import svm_test
import base64
import YoloDetection
import time
import LSTMTEST_Init 
from os import path



app = Flask(__name__)
CORS(app)



@app.route('/get_classification', methods=['POST'])
def get_image():
    latitude1 = request.form.get('latitude1')
    longitude1 = request.form.get('longitude1')
    latitude2 = request.form.get('latitude2')
    longitude2 = request.form.get('longitude2')
    date = request.form.get('date')

    print(latitude1, longitude1, latitude2, longitude2, date)

    if None in [latitude1, longitude1, latitude2, longitude2, date]:
        return "Parameters are required", 400
    
    coordinates = f"{latitude1},{longitude1},{latitude2},{longitude2}"
    # response = ImageMapPulling.get_image_stream(date, coordinates)
    image = ImageMapPulling.get_image(date, coordinates)
    # gif = LSTMTEST_Init.run_lstm_prediction(date, coordinates)
    if image:
        
        temp_image_path = 'temp_image.jpg'
        with open(temp_image_path, "wb") as f:
            f.write(image)
            time.sleep(1)
            print(f"Image written to {temp_image_path}")

        classification = svm_test.isFireDetected(image)
        if classification == "Fire Detected":
            print("FIRE IS DETETED FOR THE GIVEN CO-ORDINATES and GIVEN DATES")
            # YoloDetection.startYolo(temp_image_path)
        else:
            print("FIRE IS NOT-DETETED FOR THE GIVEN CO-ORDINATES and GIVEN DATES")



    else:
        return 500


    encoded_image = base64.b64encode(image).decode('utf-8')
    response_json = {
        "classification": classification,
        "image": encoded_image
    }
    # print("JSON Response:\n" + response_json)
    return jsonify(response_json)


@app.route('/get_yolo_output', methods=['GET'])
def get_yolo_output():
    # Run YOLO right before serving the image
    temp_image_path = 'temp_image.jpg'
    YoloDetection.startYolo(temp_image_path)
    
    print('I am in yolo_output')
    return send_from_directory(".", "yolo_output.jpg", mimetype="image/jpeg")



@app.route('/your_lstm_endpoint', methods=['POST'])
def predict():
    # Call LSTM_INIT.py using subprocess

    latitude1 = request.form.get('latitude1')
    longitude1 = request.form.get('longitude1')
    latitude2 = request.form.get('latitude2')
    longitude2 = request.form.get('longitude2')
    date = request.form.get('date')
    coordinates = f"{latitude1},{longitude1},{latitude2},{longitude2}"
    print("LSTM===>",coordinates,  date)
    result = LSTMTEST_Init.predict(coordinates, date)
    path_to_gif = 'LSTM_output.gif'
    # LSTMTEST_Init.run_lstm_prediction(date, coordinates)


    # return jsonify({"message": "Prediction completed!", "output": result.stdout})
    # return send_from_directory(directory=path.dirname(path.realpath(__file__)), filename='LSTM_output.gif')
    # return send_from_directory(".", "LSTM_output.gif", mimetype="image/gif")
    return send_file(path_to_gif, mimetype='image/gif')


@app.route('/get_lstm_gif')
def get_lstm_gif():
    # Replace 'path_to_gif' with the actual path to the generated GIF
    path_to_gif = 'LSTM_output.gif'
    return send_file(path_to_gif, mimetype='image/gif')

if __name__ == '__main__':
    app.run(port=5000)
