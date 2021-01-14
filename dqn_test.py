# Deep-Q learning Agent
import tensorflow as tf
import gym.envs as envs
# 需要安装这个来获取游戏环境
import gym
import numpy as np
import copy
# import io
import os
import tensorflow.keras as keras

# 查看所有游戏列表
# print(envs.registry.all())
# env = gym.make('CartPole-v0')
# env.reset()
#
# while True:
#     env.render()
#     env.action_space(1)


class DQNAgent(object):
    def __init__(self, _env):
        self.env = _env
        # 经验池
        self.memory = []
        self.gamma = 0.9  # decay rate 奖励衰减

        # 控制训练的随机干涉
        self.epsilon = 1  # 随机干涉阈值 该值会随着训练减少
        self.epsilon_decay = .995  # 每次随机衰减0.005
        self.epsilon_min = 0.1  # 随机值干涉的最小值

        self.learning_rate = 0.0001  # 学习率
        self._build_model()

    # 创建模型  输入4种状态，预测0/1两种行为分别带来到 奖励值
    def _build_model(self):
        model = tf.keras.Sequential()
        # 输入为4，3层128券链接，输出为2线性  2是因为控制为左右
        model.add(tf.keras.layers.Dense(128, input_dim=4, activation='tanh'))
        model.add(tf.keras.layers.Dense(128, activation='tanh'))
        model.add(tf.keras.layers.Dense(128, activation='tanh'))
        model.add(tf.keras.layers.Dense(2, activation='linear'))
        # 这里虽然输出2，但第二个完全没用上
        model.compile(loss='mse', optimizer=tf.keras.optimizers.RMSprop(lr=self.learning_rate))
        self.model = model

    # 记录经验 推进memory中
    def save_exp(self, _state, _action, _reward, _next_state, _done):
        # 将各种状态 存进memory中
        self.memory.append((_state, _action, _reward, _next_state, _done))

    # 经验池重放  根据尺寸获取  #  这里是训练数据的地方
    def train_exp(self, batch_size):
        # 这句的目的：确保每批返回的数量不会超出memory实际的存量，防止错误
        batches = min(batch_size, len(self.memory))  # 返回不大于实际memory.len 的数
        # 从len(self.memory）中随机选出batches个数
        batches = np.random.choice(len(self.memory), batches)

        for i in batches:
            # 从经验数组中 取出相对的参数 状态，行为，奖励，即将发生的状态，结束状态
            _state, _action, _reward, _next_state, _done = self.memory[i]

            # 获取当前 奖励
            y_reward = _reward
            # 如果不是结束的状态，取得未来的折扣奖励
            if not _done:
                # _target = 经验池.奖励 + gamma衰退值 * (model根据_next_state预测的结果)[0]中最大（对比所有操作中，最大值）
                # 根据_next_state  预测取得  当前的回报 + 未来的回报 * 折扣因子（gama）
                y_reward = _reward + self.gamma * np.amax(self.model.predict(_next_state)[0])
                # print('y_action', y_action)  # 1.5389154434204102

            # 获取，根据当前状态推断的 行为 input 4,output 2
            _y = self.model.predict(_state)
            # print(_action, y_reward, _y[0][_action], '_y', _y)  # [[0.08838317 0.16991007]]
            # 更新 将 某行为预测的 回报，分配到相应到 行为中  （_action = 1/0）
            _y[0][_action] = y_reward
            # 训练  x： 4 当前状态  _y[0]：2
            self.model.fit(_state, _y, epochs=1, verbose=0)

        # 随着训练的继续，每次被随机值干涉的几率减少 * epsilon_decay倍数(0.001)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    # 输入状态，返回应该采取的动作。随机干涉会随着时间的推进，越来越少。
    def act(self, _state):  # 返回回报最大的奖励值，或 随机数
        # 随机返回0-1的数，
        # 随着训练的增加，渐渐减少随机
        if np.random.rand() <= self.epsilon:
            # print('000000000',self.env.action_space.sample())
            return self.env.action_space.sample()
        else:
            # 使用预测值    返回，回报最大到最大的那个
            act_values = self.model.predict(_state)
            return np.argmax(act_values[0])  # returns action


if __name__ == "__main__":
    # 为agent初始化gym环境参数
    env = gym.make('CartPole-v0')
    # 游戏结束规则：杆子角度为±12， car移动距离为±2.4，分数限制为最高200分
    agent = DQNAgent(env)
    #保存模型到脚本所在目录，如果已有模型就加载，继续训练
    folder = os.getcwd()
    imageList = os.listdir(folder)
    for item in imageList:
        if os.path.isfile(os.path.join(folder, item)):
            if item == 'dqn.h5':
                tf.keras.models.load_model('dqn.h5')
    # 训练主循环
    episodes = 1000  # 循环次数
    for e in range(episodes):
        # 游戏复位  并获取状态4:
        # 0	Cart Position	-2.4	2.4
        # 1	Cart Velocity	-Inf	Inf
        # 2	Pole Angle	~ -41.8°	~ 41.8°
        # 3	Pole Velocity At Tip
        state = env.reset()
        # 获取当前状态  每局的初始值为 state【0】的值±0.05
        state = np.reshape(state, [1, 4])

        # time_t 代表游戏的每一帧 由于每次的分数是+1 或-100所以这个时间坚持的越长分数越高
        for time_t in range(5000):
            # 如果想看游戏就开这个
            env.render()
            # 选择行为 传入当前的游戏状态，获取行为 state 是在这里更新
            # 从模型 获取行为的随机值 或 预测值
            _action = agent.act(state)
            # 输入行为，并获取结果，包括状态、奖励和游戏是否结束  返回游戏下一针的数据 done：是否游戏结束，reward：分数  nextstate，新状态
            _next_state, _reward, _done, _ = env.step(_action)
            _next_state = np.reshape(_next_state, [1, 4])

            # 在每一个agent完成了目标的帧agent都会得到回报值1  如果失败得到-100
            _reward = -100 if _done else _reward

            # 记忆先前的状态，行为，回报与下一个状态   #  将当前状态，于执行动作后的状态，存入经验池
            agent.save_exp(state, _action, _reward, _next_state, _done)

            # 训练
            # 使下一个状态成为下一帧的新状态 #使下一状态/新状态，成为下一针的 当前状态
            state = copy.deepcopy(_next_state)

            # 如果游戏结束 done 被置为 ture
            if _done:
                # 打印分数并且跳出游戏循环
                print("episode: {}/{}, score: {}"
                      .format(e, episodes, time_t))
                break
        # 通过之前的经验训练模型
        agent.train_exp(100)
        # 保存模型
        if (e + 1) % 10 == 0:  # 每20次迭代保存一次训练数据 注销该行每次都保存
            print("saving model")
            agent.model.save('dqn.h5')