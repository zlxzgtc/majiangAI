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
            self.eat_agent = ddqn.DDQNAgent(34 * 6 + 6, 3, 'eat')  # 吃牌模型 0,1,2
            self.pong_agent = ddqn.DDQNAgent(34 * 6 + 6, 2, 'pong')  # 碰牌模型 0,1
            self.old_env = []
            self.new_env = []
            self.last_act_out = -1
            self.last_act_eat = -1
            self.last_act_pong = -1

    def game_init(self):
        self.tiles = []  # 我的手牌
        self.pong_tiles = []
        self.eat_tiles = []
        self.gang_tiles = []
        self.hu_dis = 11  # 初始化向听数为最大向听数

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
    def out_tiles(self, t=-1, finish=False, is_eat=True):
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
            # 获得上一轮状态 上一轮出的牌
            if is_eat:  # 吃碰后暂时还是简易自动出牌
                if t != -1:
                    out_t = t
                else:
                    out_t = self.computer_choose()
            else:
                cnt = np.array(utils.get_cnt(self.tiles))
                cnt[cnt > 1] = 1
                if self.last_act_out == -1:  # 第一次初始化状态
                    self.old_env = t
                    self.last_act = self.out_agent.act(t, cnt)
                    out_t = self.last_act
                else:
                    self.new_env = t
                    out_t = self.out_agent.act(t, cnt)
                    self.out_agent.train(self.old_env, self.last_act, self.new_env, finish)
                    self.last_act_eat = out_t
                    self.old_env = self.new_env
        else:
            pass
        self.tiles.remove(out_t)
        print(str(self.id) + "打出" + utils.get_tile_name(out_t) + ",打出后：" + utils.get_Tiles_names(self.tiles))
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

    def think_pong(self, tile):
        if self.type == 'human':
            if self.is_pong(tile):
                print('是否要碰?(y/n)')
                flag = input()
                if flag == 'y':
                    self.tiles.remove(tile)
                    self.tiles.remove(tile)
                    self.pong_tiles.append([tile] * 3)
                    return self.out_tiles()
            return -1
        elif self.type == 'computer':
            if self.is_pong(tile):
                # print("如果碰了，推荐出牌：",Utils.get_tile_name(t))
                # print("当前手牌：",Utils.get_Tiles_names(self.tiles))
                self.tiles.remove(tile)
                self.tiles.remove(tile)
                t = self.computer_choose()
                self.tiles.remove(t)
                if hu_judge.hu_distance(self.tiles) < self.hu_dis:
                    print(str(self.id) + "碰" + utils.get_tile_name(tile))
                    self.pong_tiles.append([tile] * 3)
                    self.tiles += [t]
                    return self.out_tiles(t)
                else:
                    self.tiles += [tile, tile, t]
                    return -1
            else:
                return -1
        elif self.type == 'ai':  # 碰同computer
            if self.is_pong(tile):  # 能碰
                self.tiles.remove(tile)
                self.tiles.remove(tile)
                t = self.computer_choose()
                self.tiles.remove(t)
                if hu_judge.hu_distance(self.tiles) < self.hu_dis:
                    print(str(self.id) + "碰" + utils.get_tile_name(tile))
                    self.pong_tiles.append([tile] * 3)
                    self.tiles += [t]
                    return self.out_tiles(t)
                else:
                    self.tiles += [tile, tile, t]
                    return -1
            else:
                return -1
        else:
            return -1

    def think_eat(self, tile):
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
                    return self.out_tiles()
            return -1
        elif self.type == 'computer':
            if len(eat_choice) > 0:
                print(str(self.id) + "吃了" + utils.get_tile_name(tile))
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
                return self.out_tiles()
            return -1
        elif self.type == 'ai':  # 吃同computer

            if len(eat_choice) > 0:
                print(str(self.id) + "吃了" + utils.get_tile_name(tile))
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
                return self.out_tiles()
            return -1
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
