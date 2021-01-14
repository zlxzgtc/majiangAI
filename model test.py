import tensorflow as tf
import numpy as np

model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(128, input_dim=4, activation='tanh'))
model.add(tf.keras.layers.Dense(128, activation='tanh'))
model.add(tf.keras.layers.Dense(128, activation='tanh'))
model.add(tf.keras.layers.Dense(34, activation='softmax'))
model.compile(loss='mse', optimizer=tf.keras.optimizers.RMSprop(lr=0.1))

classes = model.predict(np.reshape([1,2,3,4], [1, 4]))
print(classes)
print(np.sum(classes))
print(np.argmax(classes))