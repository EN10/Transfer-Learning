from tensorflow.keras import *

# download dataset
data_root = utils.get_file(
  'flower_photos','https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz',
   untar=True)

image_generator = preprocessing.image.ImageDataGenerator(rescale=1/255)

import tensorflow_hub as hub
# download model
feature_extractor_model = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4" 

IMAGE_SIZE = 224
feature_extractor_layer = hub.KerasLayer(
    feature_extractor_model, input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3), trainable=False)

# resize images for model
image_data = image_generator.flow_from_directory(str(data_root), target_size=(IMAGE_SIZE, IMAGE_SIZE))

# train head with new dataset
model = Sequential([
  feature_extractor_layer,
  layers.Dense(image_data.num_classes)
])

model.compile(
  optimizer=optimizers.Adam(),
  loss=losses.CategoricalCrossentropy(from_logits=True),
  metrics=['acc'])

epochs = 5
history = model.fit(image_data, epochs=epochs,
                    steps_per_epoch=len(image_data))

# test model with new image
!wget -O image.jpg https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/daisy-flower-1532449822.jpg

# process image for model
img = preprocessing.image.load_img('image.jpg',
                                   target_size=(IMAGE_SIZE, IMAGE_SIZE))
x = preprocessing.image.img_to_array(img)
x = backend.expand_dims(x, axis=0)

# display image
import matplotlib.pyplot as plt
plt.imshow(img)

# run prediction
pred = model.predict(x)
index = backend.argmax(pred)
labels = list(image_data.class_indices.keys())
print(labels[index[0]])
