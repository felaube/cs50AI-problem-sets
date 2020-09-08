import sys
import tensorflow as tf
from traffic import IMG_WIDTH, IMG_HEIGHT
import cv2
import numpy as np

# Check command-line arguments
if len(sys.argv) != 3:
    sys.exit("Usage: python recognition.py model image")
model = tf.keras.models.load_model(sys.argv[1])
image = sys.argv[2]

image = cv2.resize(cv2.imread(image), (IMG_WIDTH, IMG_HEIGHT))

classification = model.predict(np.array(image).reshape(1, 30, 30, 3)).argmax()

print(f"The CNN classified this image as {str(classification)}")
