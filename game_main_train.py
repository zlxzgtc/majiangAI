from random import shuffle
from copy import deepcopy
import numpy as np
import utils
import player
import game_table
import hu_judge
import tensorflow as tf
import os


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
            s = ""
            print("--------------------第" + str(i + 1) + "局--------------------\n")
            self.game_table = game_table.Gametable(False)  # 创建牌堆
            self.now_turn = (self.banker + i) % 4
            self.banker = (self.banker + i) % 4
            self.no_hu = False
            for k in range(4):  # 玩家上局手牌清空
                self.players[k].game_init()
            for k in range(0, 16):
                for j in range(4):
                    self.players[j].add_tiles(self.game_table.give_pile())
            # for k in range(4):
            #     print(k, ' 的牌：', utils.get_Tiles_names(self.players[k].tiles))
            self.play()
            print("ai手牌："+utils.get_Tiles_names(self.players[0].tiles) )
            print("--------------------游戏结束--------------------\n")
            print(self.print_score())
            #             print(s)
            # f = "train.txt"
            # with open(f, "a") as file:
            #     file.write(s)

    def play(self, banker=0):
        k = 0
        self.finished = False
        while not self.finished:  # 游戏未结束，四名玩家轮流出牌
            k += 1
            # print("当前----第", k, "轮")
            if k != 1:  # 除了第一个人打出的牌，其余都要判断是否能吃
                c = self.player_think_eat(last_tile)
                if c != 3:
                    last_tile = self.player_think_out()
                    self.next_player()
                    continue
            if self.mo(self.now_turn) == -1:  # 摸牌
                self.no_hu = True
                print("流局")
                break
            if self.player_think_hu():
                break
            last_tile = self.player_think_out()
            self.game_table.put_pile(last_tile)
            self.next_player()
            if self.others_think_hu(last_tile):
                break
            pong_id = self.others_think_pong(last_tile)
            if pong_id != -1:
                self.next_player(pong_id % 4)
                last_tile = self.player_think_out()
                self.next_player()
            # print("当前打出的牌:", utils.get_Cnt_names(self.gametable.out_pile))
        # 游戏结束计算得分
        self.count_score()
        self.print_score()
        ai_player = self.players[0]
        ai_player.train(ai_player.old_out_env, ai_player.last_act, self.env(0), True, 0)
        if ai_player.last_act_eat != -1:
            ai_player.train(ai_player.old_eat_env, ai_player.last_act_eat, self.env(0), True, 1)
            ai_player.last_act_eat = -1
        if ai_player.last_act_pong != -1:
            ai_player.train(ai_player.old_pong_env, ai_player.last_act_pong, self.env(0), True, 2)
            ai_player.last_act_pong = -1

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
        s = ""
        for player in self.players:
            s += "  玩家" + str(player.id) + "  " + str(player.score)
        return s

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
        if self.players[player_id].type == 'ai':
            self.players[player_id].last_act = 0
        return t

    def player_think_eat(self, last_tile):
        if self.players[self.now_turn].type == 'ai':
            t = self.players[self.now_turn].think_eat(last_tile, self.env(self.now_turn))
            if t != 3:
                self.players[self.now_turn].last_act = 1
        else:
            t = self.players[self.now_turn].think_eat(last_tile)
        return t

    def player_think_out(self):
        if self.players[self.now_turn].type == 'ai':
            t = self.players[self.now_turn].out_tiles(env=self.env(self.now_turn))
        else:
            t = self.players[self.now_turn].out_tiles()
        return t

    def player_think_hu(self):  # 玩家是否自摸胡
        self.players[self.now_turn].hu_dis = hu_judge.hu_distance(self.players[self.now_turn].tiles)
        if self.players[self.now_turn].hu_dis == 0:  # 判断是否胡
            print("玩家" + str(self.now_turn) + "自摸胡了:" + utils.get_Tiles_names(self.players[self.now_turn].tiles))
            self.hu_id = self.now_turn
            self.finished = True
        return self.finished

    def others_think_hu(self, last_tile):
        for j in range(3):
            # 首先判断有没有人胡这张牌
            if hu_judge.hu_distance(self.players[(self.now_turn + j) % 4].tiles, last_tile) == 0:
                print("玩家" + str((self.now_turn + j) % 4) + "胡了:" + utils.get_Tiles_names(
                    self.players[(self.now_turn + j) % 4].tiles) + utils.get_tile_name(last_tile))
                self.finished = True
                self.hu_id = (self.now_turn + j) % 4
                return True
        return False

    # 然后判断是否有人碰 ，返回碰的人的id,无则返回-1
    def others_think_pong(self, last_tile):
        pong_id = -1
        for j in range(3):
            player = self.players[(self.now_turn + j) % 4]
            if player.type == 'ai':
                c = player.think_pong(last_tile, env=self.env(self.now_turn))
                if c == 1:
                    self.players[self.now_turn].last_act = 2
            else:
                c = player.think_pong(last_tile)
            if c != 0:
                pong_id = (self.now_turn + j) % 4
        return pong_id


gpu = tf.config.experimental.list_physical_devices(device_type='GPU')[0]
tf.config.experimental.set_memory_growth(gpu, True)
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
game = Game(round=10000)
game.start()
