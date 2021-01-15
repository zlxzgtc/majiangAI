from random import shuffle
from copy import deepcopy
import numpy as np
import utils
import player
import game_table
import hu_judge


class Game():

    def __init__(self, players=['ai', 'computer', 'computer', 'computer'], banker=0, round=1):
        self.finished = False
        self.players = []
        for i in range(4):
            self.players.append(player.Player(i, players[i]))
        self.banker = banker  # 庄家
        self.round = round  # 游戏轮数
        self.hu_score = 10  # 胡牌得分，庄家三倍
        self.hu_id = -1  # -1表示没人胡
        self.now_turn = banker
        self.no_hu = False

    def start(self):
        for i in range(self.round):
            print("--------------------第" + str(i + 1) + "局--------------------")
            self.game_table = game_table.Gametable(False)  # 创建牌堆
            self.now_turn = (self.banker + i) % 4
            self.banker = (self.banker + i) % 4
            self.no_hu = False
            for k in range(4):  # 玩家上局手牌清空
                self.players[k].game_init()
            for k in range(0, 16):
                for j in range(4):
                    self.players[j].add_tiles(self.game_table.give_pile())
            for k in range(4):
                print(k, ' 的牌：', utils.get_Tiles_names(self.players[k].tiles))
            self.play()
        print("--------------------游戏结束--------------------")
        self.print_score()

    def play(self, banker=0):
        k = 0
        last_tile = 0
        self.finished = False
        now_turn = banker  # 当前出牌的人
        while not self.finished:  # 游戏未结束，四名玩家轮流出牌
            k += 1
            # print("当前----第", k, "轮")
            if k != 1:  # 除了第一个人打出的牌，其余都要判断是否能吃
                if self.players[self.now_turn].type == 'ai':
                    t = self.players[self.now_turn].think_eat(last_tile, self.env(), self.finished)
                else:
                    t = self.players[self.now_turn].think_eat(last_tile)
                if t != -1:
                    last_tile = t
                    self.next_player()
                    continue
            # 摸牌
            if self.mo(self.now_turn) == -1:
                self.no_hu = True
                print("流局")
                break
            self.players[self.now_turn].hu_dis = hu_judge.hu_distance(self.players[self.now_turn].tiles)
            # if self.players[self.now_turn].type == 'ai':# ai在每次摸牌时要获取状态
            #     print(self.env(self.now_turn))
            if self.players[self.now_turn].hu_dis == 0:  # 判断是否胡
                print("玩家" + str(self.now_turn) + "自摸胡了:" + utils.get_Tiles_names(self.players[self.now_turn].tiles))
                self.hu_id = self.now_turn
                self.finished = True
                break
            if self.players[self.now_turn].type == 'ai':
                t = self.players[self.now_turn].out_tiles(self.env(self.now_turn), self.finished)
            else:
                t = self.players[self.now_turn].out_tiles()
            last_tile = t
            self.game_table.put_pile(t)
            self.next_player()
            for j in range(3):
                # 首先判断有没有人胡这张牌
                if hu_judge.hu_distance(self.players[(self.now_turn + j) % 4].tiles, last_tile) == 0:
                    print("玩家" + str((self.now_turn + j) % 4) + "胡了:" + utils.get_Tiles_names(
                        self.players[(self.now_turn + j) % 4].tiles) + utils.get_tile_name(last_tile))
                    self.finished = True
                    self.hu_id = (self.now_turn + j) % 4
                    break
                # 然后判断是否有人碰 ，有则将牌堆中的这张牌取出
                t = self.players[(self.now_turn + j) % 4].think_pong(last_tile)
                if t != -1:
                    last_tile = t
                    self.next_player(self.now_turn + j + 1)
                    break

            # print("当前打出的牌:", utils.get_Cnt_names(self.gametable.out_pile))
        # 游戏结束计算得分
        self.count_score()
        self.print_score()
        ai_player = self.players[0]
        ai_player.out_agent.train(ai_player.old_env, ai_player.last_act, self.env(0), self.finished)

    def env(self, id):
        my_tiles = utils.get_cnt(self.players[id].tiles)
        out_tiles = self.game_table.out_pile
        my_eat_pong = np.add(utils.get_cnt(self.players[id].eat_tiles), utils.get_cnt(self.players[id].pong_tiles))
        others_eat_pong = []
        other_info = []  # 所有玩家手牌数量 4 剩余牌数量 1 向听数 1
        for i in range(4):
            other_info.append(len(self.players[i].tiles))
            if i != id:
                others_eat_pong = np.hstack((others_eat_pong, np.add(utils.get_cnt(self.players[i].eat_tiles),
                                                                     utils.get_cnt(self.players[i].pong_tiles))))

        other_info.append(len(self.game_table.Tiles))
        other_info.append(self.players[id].hu_dis)
        return np.hstack((my_tiles, out_tiles, my_eat_pong, others_eat_pong, other_info))

    def count_score(self):
        if self.no_hu:  # 流局不计算得分
            return
        for player in self.players:
            if player.id == self.hu_id:
                player.score += self.hu_score * 3
            else:
                player.score -= self.hu_score

    def print_score(self):
        for player in self.players:
            print("玩家" + str(player.id) + "--当前得分：" + str(player.score))

    def next_player(self, next_id=-1):
        if next_id == -1:
            self.now_turn = (self.now_turn + 1) % 4
        else:
            self.now_turn = next_id % 4

    def mo(self, player_id):
        t = self.game_table.give_pile()
        if t == -1:  # 无牌可摸,流局
            self.finished = True
        else:
            self.players[player_id].add_tiles(t)
        return t


game = Game(round=4)
game.start()
