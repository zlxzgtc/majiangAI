import random
import numpy as np
from collections import deque
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import backend as K
import os
import tensorflow as tf
import utils
import resnet

EPISODES = 5000


class DDQNAgent:
    def __init__(self, state_size, action_size, name):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.5  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.99
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()
        self.count = 0  # 统计训练次数
        self.batch_size = 32
        self.name = name
        if os.path.isfile("./{}.h5".format(name)):
            self.load("./{}.h5".format(name))

    def _huber_loss(self, y_true, y_pred, clip_delta=1.0):
        error = y_true - y_pred
        cond = K.abs(error) <= clip_delta

        squared_loss = 0.5 * K.square(error)
        quadratic_loss = 0.5 * K.square(clip_delta) + clip_delta * (K.abs(error) - clip_delta)

        return K.mean(tf.where(cond, squared_loss, quadratic_loss))

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        # model = Sequential()
        # model.add(Dense(128, input_dim=self.state_size, activation='relu'))
        # model.add(Dense(123, activation='relu'))
        # model.add(Dense(self.action_size, activation='softmax'))
        # model.compile(loss=self._huber_loss,
        #               optimizer=Adam(lr=self.learning_rate))
        model = resnet.resnet18()
        model.build(input_shape=(None, 32, 32, 3), num_class=self.action_size)

        return model

    def update_target_model(self):
        # copy weights from model to target_model
        self.target_model.set_weights(self.model.get_weights())

    def memorize(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state, cnt):
        # 首先获取所有可能的动作
        state = state.reshape((1, self.state_size))
        cnt = np.array(cnt)
        choice = np.argwhere(cnt == 1)
        print("可选出的牌：" + utils.get_Cnt_names(cnt))
        if np.random.rand() <= self.epsilon:
            return choice[random.randrange(len(choice))][0]  # 随机选择一个动作
        act_values = self.model.predict(state) + cnt  # 否则选择估值最大的 +(有牌可出的选项+1)
        print("建议出牌" + utils.get_tile_name(np.argmax(act_values)))
        return np.argmax(act_values)  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)  # 随机取样
        for state, action, reward, next_state, done in minibatch:
            target = self.model.predict(state)
            if done:
                target[0][action] = reward
            else:
                # a = self.model.predict(next_state)[0]
                t = self.target_model.predict(next_state)[0]
                target[0][action] = reward + self.gamma * np.amax(t)
                # target[0][action] = reward + self.gamma * t[np.argmax(a)]
            self.model.fit(state, target, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

    def train(self, state0, act0, state1, done, reward):
        self.count += 1
        state0 = self.reshape_input(state0)
        state1 = self.reshape_input(state1)
        # state0 = np.reshape(state0, [1, self.state_size])
        # state1 = np.reshape(state1, [1, self.state_size])
        self.memorize(state0, act0, reward, state1, done)
        if done:
            self.update_target_model()
            print("train_{}: {}, score: {}, e: {:.2}"
                  .format(self.count, self.name, reward, self.epsilon))
        if len(self.memory) > self.batch_size:
            self.replay(self.batch_size)
            # if self.count % self.batch_size == 0:
            self.save("./{}.h5".format(self.name))

    # 对输入进行格式化
    def reshape_input(self, x):
        x = x + [0] * (32 * 32 * 3 - len(x))
        x = np.asarray(x, dtype='float32')
        x = x.reshape((32, 32, 3))
        x = np.expand_dims(x, axis=0)
        return x
