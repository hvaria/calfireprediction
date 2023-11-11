import os
import io
import requests
from tensorflow.keras.utils import load_img, img_to_array
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.models import load_model

model = load_model("svm_final.h5")


def isFireDetected(img_data):
    # print("inside SVM")
    retsultstr = "Fire"
    # test_image = load_img(img, target_size=(224,224))
    # plt.imshow(test_image)

    image = np.array(Image.open(io.BytesIO(img_data)))

    # Resize the image to 224x224 using PIL
    image = Image.fromarray(image).resize((224, 224))

    # Convert the resized image back to a NumPy array
    image = np.array(image)

    test_image = img_to_array(image)  # (converting to single dimen array)
    test_image = test_image / 255  # (to normalize by byte)
    test_image = np.expand_dims(test_image, axis=0)  # (to bring in matrix)
    result = model.predict(test_image)
    print(result)
    value = result[0]
    v = value[0]
    # print("Value is ",v)
    # if v>0.3 and v<1:
    if v > -2:
        retsultstr = "Fire Detected"
    else:
        retsultstr = "No Fire Detected"

    return retsultstr
