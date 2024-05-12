import tensorflow as tf
from keras.preprocessing import image
import numpy as np
from PIL import Image


model = tf.keras.models.load_model('./Home/models/my_model.keras')


mapper = {
    0: 'angry',
    1: 'disgusted',
    2: 'feared',
    3: 'happy',
    4: 'sad',
    5: 'surprised',
    6: 'neutral'
}


def pred_emotion(img_array):

    if len(img_array.shape) == 2:
        img_array = np.stack((img_array,) * 3, axis=-1)
    elif img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]

    resized_img_array = tf.image.resize(img_array, [48, 48])

    resized_img_array = resized_img_array / 255.0

    reshaped_img_array = np.expand_dims(resized_img_array, axis=0)

    pred = mapper[np.argmax(model.predict(reshaped_img_array)[0])]

    return pred
