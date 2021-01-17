import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, optimizers, Sequential
import numpy as np
from tensorflow.keras.optimizers import Adam


class BasicBlock(layers.Layer):
    def __init__(self, filter_num, stride=1):
        super(BasicBlock, self).__init__()
        self.conv1 = layers.Conv2D(filter_num, (3, 3), strides=stride, padding='same')
        self.bn1 = layers.BatchNormalization()
        self.relu = layers.Activation('relu')
        self.conv2 = layers.Conv2D(filter_num, (3, 3), strides=1, padding='same')
        self.bn2 = layers.BatchNormalization()
        if stride != 1:

            self.downsample = Sequential()
            self.downsample.add(layers.Conv2D(filter_num, (1, 1), strides=stride))
            # self.downsample = layers.Conv2D(filter_num, (1,1), strides = stride)
        else:
            self.downsample = lambda x: x

    def call(self, inputs, training=None):
        # [b, h, w, c]
        out = self.conv1(inputs)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)

        identity = self.downsample(inputs)

        output = layers.add([out, identity])
        output = tf.nn.relu(output)
        return output


class ResNet(keras.Model):
    def __init__(self, output_size=10):
        super(ResNet, self).__init__()
        # 预处理层
        self.stem = Sequential([
            layers.Conv2D(256, (3, 3), strides=(1, 1)),
            layers.BatchNormalization(),
            layers.Activation('relu'),
            # layers.MaxPool2D(pool_size=(2, 2), strides=(1, 1), padding='same')
        ])
        # resblock
        self.resblock = self.build_resblock(256, 19)
        # 自适应
        self.avgpool = layers.GlobalAveragePooling2D()
        self.fc = layers.Dense(output_size, activation='softmax')

    def build_resblock(self, filter_num, blocks, stride=1):
        res_blocks = Sequential()
        # may down sample
        res_blocks.add(BasicBlock(filter_num, stride))
        # just down sample one time
        for pre in range(1, blocks):
            res_blocks.add(BasicBlock(filter_num, stride=1))
        return res_blocks

    def call(self, inputs, training=None):
        x = self.stem(inputs)
        x = self.resblock(x)
        x = self.avgpool(x)
        x = self.fc(x)
        return x


# model = ResNet(output_size=34)
# model.compile(optimizer=Adam(lr=0.0001))
# model.build(input_shape=(None, 32, 3, 3))
# model.summary()
# from tensorflow.keras.utils import plot_model
#
# plot_model(model, to_file='DResLayer_model.png', show_shapes=True)
# x = tf.random.uniform(shape=(1, 32, 3, 3))
# print(x)
# print(model.predict(x))
