# Wildfire Prediction Application


<br>

### ___Summary___
This application will allow the user to enter two Longitude and Latitude coordinates and a date. The first pair of coordinates corresponds to the bottom left corner of the image, the second pair of points corresponds to the top right corner of the image. The application sends the user's input to Nasa's Worldview Snapshots which and will return a satellite image for the given location and date. This image will then be analyzed by an SVM model to detect if a wildfire is present in the satellite image. If there is a wildfire, a YOLO model with place a bounding box around the fire to identify it for the user. Finally, if the location and date of the fire is within the dataset of environmental measurements, an LSTM model will predict the spread of the fire over the next 5 days.  

### ___Application Flow___
![Application Flow](https://i.imgur.com/EbrrvAg.png)

<br>

### ___Output___
![LSTM_output](https://github.com/user-attachments/assets/9ce87bad-9eeb-4010-922d-b6103357b152)



 
<br>

### ___Developer Instructions___
The application requires Apache Tomcat 9 to be installed in order to host the frontend. The backend requires Python 3.10 and a number of python libraries to be installed including: <br>
* os
* requests
* matplotlib.pyplot
* numpy
* tensorflow.keras.utils
* tensorflow.keras.models


