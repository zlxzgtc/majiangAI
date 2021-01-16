import utils
from copy import deepcopy
import numpy as np
import hu_judge
import ddqn


class Player():
    # type : 'human' , 'computer' ,'ai'

    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.tiles = []  # 我的手牌
        self.pong_tiles = []
        self.eat_tiles = []
        self.gang_tiles = []
        self.hu_dis = 11  # 初始化向听数为最大向听数
        self.score = 0
        if type == 'ai':
            self.out_agent = ddqn.DDQNAgent(34 * 6 + 6, 34, 'out')  # 打牌模型 0-33
            self.eat_agent = ddqn.DDQNAgent(34 * 6 + 6, 4, 'eat')  # 吃牌模型 0,1,2,3(不吃)
            self.pong_agent = ddqn.DDQNAgent(34 * 6 + 6, 2, 'pong')  # 碰牌模型 0(不碰),1(碰)
            self.old_out_env = []
            self.new_out_env = []
            self.old_eat_env = []
            self.old_pong_env = []
            self.last_act_out = -1
            self.last_act_eat = -1
            self.last_act_pong = -1
            self.last_act = 0  # 记录上一次的操作,用来判断是否进行train 0:摸牌,1：吃，2：碰
            self.reward = 0

    def game_init(self):
        self.tiles = []  # 我的手牌
        self.pong_tiles = []
        self.eat_tiles = []
        self.gang_tiles = []
        self.hu_dis = 11  # 初始化向听数为最大向听数
        if self.type =='ai':
            self.old_out_env = []
            self.new_out_env = []
            self.old_eat_env = []
            self.old_pong_env = []
            self.last_act_out = -1
            self.last_act_eat = -1
            self.last_act_pong = -1
            self.last_act = 0  # 记录上一次的操作,用来判断是否进行train 0:摸牌,1：吃，2：碰
            self.reward = 0

    # 游戏开始后，发牌
    def set_tile(self, tiles):
        self.tiles = tiles

    # 摸牌
    def add_tiles(self, tile):
        self.tiles.append(tile)
        self.sort_tiles()

    # 理牌
    def sort_tiles(self):
        self.tiles.sort()

    # 玩家选择一张牌打出
    def out_tiles(self, t=-1, env=[]):
        if self.type == 'human':
            # 输出所有手牌
            for item in self.tiles:
                print(utils.get_tile_name(item), end='\t')
            print()
            print("\t".join(list(map(str, list(range(0, len(self.tiles)))))))
            t = int(input('请选择一张牌打出:'))
            out_t = self.tiles[t]
        elif self.type == 'computer':  # 简单自动出牌,优先出单张字牌，然后出单张的数牌
            if t != -1:
                out_t = t
            else:
                out_t = self.computer_choose()
        elif self.type == 'ai':
            cnt = np.array(utils.get_cnt(self.tiles))
            cnt[cnt > 1] = 1
#             print("当前手牌:"+utils.get_Tiles_names(self.tiles))
            self.new_out_env = env
            if self.last_act_out != -1:
                self.train(self.old_out_env, self.last_act_out, env, False, 0)  # 还在进行决策，所以done肯定为false
            out_t = self.last_act_out = self.out_agent.act(env, cnt)
            self.old_out_env = env
            if self.last_act == 0:
                if self.last_act_eat != -1:
                    self.train(self.old_eat_env, self.last_act_eat, env, False, 1)
                    self.last_act_eat = -1
                if self.last_act_pong != -1:
                    self.train(self.old_pong_env, self.last_act_pong, env, False, 2)
                    self.last_act_pong = -1
        else:
            pass
        self.tiles.remove(out_t)
        # print(str(self.id) + "打出" + utils.get_tile_name(out_t) + ",打出后：" + utils.get_Tiles_names(self.tiles))
        return out_t

    # 判断能不能碰
    def is_pong(self, tile):
        return self.tiles.count(tile) == 2

    # 判断能不能吃 , 0:吃左边，1：吃中间，2：吃右边
    def is_eat(self, tile):
        eat_choice = []
        if tile > 26:
            pass
        elif tile in [0, 9, 18]:
            if self.tiles.count(tile + 1) >= 1 and self.tiles.count(tile + 2) >= 1:
                eat_choice.append(0)
        elif tile in [8, 17, 26]:
            if self.tiles.count(tile - 1) >= 1 and self.tiles.count(tile - 2) >= 1:
                eat_choice.append(2)
        elif tile in [1, 10, 19]:
            if self.tiles.count(tile + 1) >= 1 and self.tiles.count(tile + 2) >= 1:
                eat_choice.append(0)
            if self.tiles.count(tile + 1) >= 1 and self.tiles.count(tile - 1) >= 1:
                eat_choice.append(1)
        elif tile in [7, 16, 25]:
            if self.tiles.count(tile - 1) >= 1 and self.tiles.count(tile - 2) >= 1:
                eat_choice.append(2)
            if self.tiles.count(tile + 1) >= 1 and self.tiles.count(tile - 1) >= 1:
                eat_choice.append(1)
        else:
            if self.tiles.count(tile - 1) >= 1 and self.tiles.count(tile - 2) >= 1:
                eat_choice.append(2)
            if self.tiles.count(tile + 1) >= 1 and self.tiles.count(tile + 2) >= 1:
                eat_choice.append(0)
            if self.tiles.count(tile + 1) >= 1 and self.tiles.count(tile - 1) >= 1:
                eat_choice.append(1)
        return eat_choice

    def think_pong(self, tile, env=[]):
        if self.type == 'human':  # 待完善
            if self.is_pong(tile):
                print('是否要碰?(y/n)')
                flag = input()
                if flag == 'y':
                    self.tiles.remove(tile)
                    self.tiles.remove(tile)
                    self.pong_tiles.append([tile] * 3)
                    return 1
            return 0
        elif self.type == 'computer':  # 返回是否碰
            if self.is_pong(tile):
                # print("如果碰了，推荐出牌：",Utils.get_tile_name(t))
                # print("当前手牌：",Utils.get_Tiles_names(self.tiles))
                self.tiles.remove(tile)
                self.tiles.remove(tile)
                t = self.computer_choose()
                self.tiles.remove(t)
                if hu_judge.hu_distance(self.tiles) < self.hu_dis:
                    # print(str(self.id) + "碰" + utils.get_tile_name(tile))
                    self.pong_tiles.append([tile] * 3)
                    self.tiles += [t]
                    c = 1
                else:
                    self.tiles += [tile, tile, t]
                    c = 0
            else:
                c = 0
            return c
        elif self.type == 'ai':  # 返回是否碰
            pong_choice = [0]
            if self.is_pong(tile):  # 能碰
                self.old_pong_env = env
                pong_choice.append(1)
                c = self.pong_agent.act(env, utils.get_pong_cnt(pong_choice))
                if c == 1:  # 选择碰
                    self.tiles.remove(tile)
                    self.tiles.remove(tile)
                    self.pong_tiles += [tile] * 3
                self.last_act = 2
                self.old_pong_env = env
                self.last_act_pong = c
            else:
                c = 0
            return c
        else:
            return -1

    def think_eat(self, tile, env=[]):  # 返回为吃的选择
        add_tiles = np.asarray([[0, 1, 2], [-1, 0, 1], [-1, -2, 0]])
        # print(utils.get_Tiles_names(self.tiles)+"能不能吃？"+utils.get_tile_name(tile))
        eat_choice = self.is_eat(tile)
        if self.type == 'human':
            if len(eat_choice) > 0:
                print('是否要吃?(y/n)')
                flag = input()
                if flag == 'y':
                    eat_all = ""
                    for choice in eat_choice:
                        eat_all += '[' + str(choice) + ']' + utils.get_Tiles_names(add_tiles[choice] + tile)
                    c = int(input("请选择你要怎么吃" + eat_all + ":"))
                    if c == 0:  # 吃左边
                        self.tiles.remove(tile + 1)
                        self.tiles.remove(tile + 2)
                        self.eat_tiles = self.eat_tiles + [tile, tile + 1, tile + 2]
                    elif c == 1:  # 吃中间
                        self.tiles.remove(tile - 1)
                        self.tiles.remove(tile + 1)
                        self.eat_tiles = self.eat_tiles + [tile - 1, tile, tile + 1]
                    else:  # 吃右边
                        self.tiles.remove(tile - 1)
                        self.tiles.remove(tile - 2)
                        self.eat_tiles = self.eat_tiles + [tile - 2, tile - 1, tile]
                    return c
            return 3
        elif self.type == 'computer':
            if len(eat_choice) > 0:
                # print(str(self.id) + "吃了" + utils.get_tile_name(tile))
                c = eat_choice[0]
                if c == 0:  # 吃左边
                    self.tiles.remove(tile + 1)
                    self.tiles.remove(tile + 2)
                    self.eat_tiles = self.eat_tiles + [tile, tile + 1, tile + 2]
                elif c == 1:  # 吃中间
                    self.tiles.remove(tile - 1)
                    self.tiles.remove(tile + 1)
                    self.eat_tiles = self.eat_tiles + [tile - 1, tile, tile + 1]
                else:  # 吃右边
                    self.tiles.remove(tile - 1)
                    self.tiles.remove(tile - 2)
                    self.eat_tiles = self.eat_tiles + [tile - 2, tile - 1, tile]
            else:
                c = 3
            return c
        elif self.type == 'ai':
            if len(eat_choice) > 0:
                eat_choice.append(3)
                c = self.eat_agent.act(env, utils.get_eat_cnt(eat_choice))
                if c == 0:  # 吃左边
                    self.tiles.remove(tile + 1)
                    self.tiles.remove(tile + 2)
                    self.eat_tiles = self.eat_tiles + [tile, tile + 1, tile + 2]
                elif c == 1:  # 吃中间
                    self.tiles.remove(tile - 1)
                    self.tiles.remove(tile + 1)
                    self.eat_tiles = self.eat_tiles + [tile - 1, tile, tile + 1]
                elif c == 2:  # 吃右边
                    self.tiles.remove(tile - 1)
                    self.tiles.remove(tile - 2)
                    self.eat_tiles = self.eat_tiles + [tile - 2, tile - 1, tile]
                else:  # 没吃
                    pass
                self.last_act = 1
                self.old_eat_env = env
                self.last_act_eat = c
            else:
                c = 3
            # if c != 3:
                # print(str(self.id) + "吃了" + utils.get_tile_name(tile))
            return c
        else:
            pass

    def get_cnt(self, tiles):
        cnt = [0] * 34
        for i in range(34):
            cnt[i] = tiles.count(i)
        return cnt

    # 判断tile在手牌中是否能组成顺子
    def is_BCD(self, tile):
        if tile > 24:
            return False
        else:
            flag = False
            if tile in [0, 9, 18]:
                if self.tiles.count(tile + 1) > 0 and self.tiles.count(tile + 2) > 0:
                    flag = True
            elif tile in [8, 17, 26]:
                if self.tiles.count(tile - 1) > 0 and self.tiles.count(tile - 2) > 0:
                    flag = True
            else:
                if (self.tiles.count(tile - 1) > 0 and self.tiles.count(tile - 2) > 0) \
                        or (self.tiles.count(tile + 1) > 0 and self.tiles.count(tile + 2) > 0) \
                        or (self.tiles.count(tile + 1) > 0 and self.tiles.count(tile - 1) > 0):
                    flag = True
            return flag

    def is_AAA(self, tile):
        return self.tiles.count(tile) >= 3

    # 简易的出牌选择器,选择移除一张牌后会使向听量减小的牌
    def computer_choose(self):
        now_dis = hu_judge.hu_distance(self.tiles)
        cnt = self.get_cnt(self.tiles)
        list_dis = []
        for i in range(34):
            if cnt[i] == 1:
                self.tiles.remove(i)
                k = hu_judge.hu_distance(self.tiles)
                self.tiles.append(i)
                if k < now_dis:
                    return i
                elif k == now_dis:
                    list_dis.append(i)
        if len(list_dis) == 0:
            ran = int(np.floor(np.random.rand() * len(self.tiles)))
            t = self.tiles[ran]
        else:
            ran = int(np.floor(np.random.rand() * len(list_dis)))
            t = list_dis[ran]
        return t

    # def train_eat(self, env, done):  # 之前做过关于吃的决策,env表示当前状态
    #     if self.last_act_eat != -1:
    #         self.new_env = env
    #         reward = self.get_reward(done)
    #         self.eat_agent.train(self.old_env, self.last_act_eat, self.new_env, done, reward)
    #         self.old_env = self.new_env
    #         self.last_act_eat = -1
    #     else:
    #         self.old_env = env

    def get_reward(self, old_env, new_env, done):
        if not done:
            reward = old_env[-1] -new_env[-1]
        else:
            if new_env[-1] == 0:  # 我胡了
                reward = 30
            else:
                reward = -10  # 别人胡了
        return reward

    # 每次决策过后都把状态放到训练池， type表示要训练哪一个模型 0：out,1:eat,2:pong
    def train(self, old_env, act, new_env, done, cls):
        reward = self.reward + self.get_reward(old_env, new_env, done)
#         print("reward:"+str(reward))
        if cls == 0:
            self.out_agent.train(old_env, act, new_env, done, reward)
        elif cls == 1:
            self.eat_agent.train(old_env, act, new_env, done, reward)
            self.last_act_eat = -1
        else:
            self.pong_agent.train(old_env, act, new_env, done, reward)
            self.last_act_pong = -1
