import tensorflow as tf
from keras.preprocessing import image
import numpy as np


model = tf.keras.models.load_model('./models/my_model.keras')


mapper = {
    0: 'anger',
    1: 'disgust',
    2: 'fear',
    3: 'happiness',
    4: 'sadness',
    5: 'surprise',
    6: 'neutral'
}


def pred_emotion():
    image = tf.keras.utils.load_img('/kaggle/input/inputs/test.jpg')
    mood = mapper[np.argmax(model.predict(image.reshape(1, 48, 48, 3))[0])]

    return mood
