from random import shuffle
from copy import deepcopy
import numpy as np
import utils
import Player
import Gametable
import hu_judge


class Game():

    def __init__(self, players=['computer', 'computer', 'computer', 'computer'], banker=0, round=1):
        self.finished = False
        self.players = []
        for i in range(4):
            self.players.append(Player.Player(i, players[i]))
        self.banker = banker  # 庄家
        self.round = round  # 游戏轮数
        self.score = 10  # 胡牌得分，庄家三倍
        self.hu_id = -1  # -1表示没人胡
        self.now_turn = banker

    def start(self):
        for i in range(self.round):
            print("--------------------第" + str(i + 1) + "局--------------------")
            self.game_table = Gametable.Gametable(True)  # 创建牌堆
            self.now_turn = (self.banker + i) % 4
            self.banker = (self.banker + i) % 4
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
            if k!=1:  # 除了第一个人打出的牌，其余都要判断是否能吃
                t = self.players[now_turn].think_eat(last_tile)
                first_draw = False
                if t != -1:
                    last_tile = t
                    self.next_player()
                    print("有人吃-----------------------------------------------------------------------")
                    continue

            # 摸牌
            if self.mo(self.now_turn) == -1:
                print("流局")
                break
            self.players[self.now_turn].hu_dis = hu_judge.hu_distance(self.players[self.now_turn].tiles)
            if self.players[self.now_turn].hu_dis == 0:  # 判断是否胡
                print("玩家" + str(self.now_turn) + "自摸胡了:" + utils.get_Tiles_names(self.players[self.now_turn].tiles))
                self.hu_id = self.now_turn
                self.finished = True
                break
            t = self.players[self.now_turn].out_tiles()
            last_tile = t
            self.game_table.put_pile(t)
            self.next_player()
            for j in range(3):
                # 首先判断有没有人胡这张牌
                if hu_judge.hu_distance(self.players[(self.now_turn + j ) % 4].tiles, last_tile) == 0:
                    print("玩家" + str((self.now_turn + j ) % 4) + "胡了:" + utils.get_Tiles_names(
                        self.players[(self.now_turn + j ) % 4].tiles) + utils.get_tile_name(last_tile))
                    self.finished = True
                    self.hu_id = self.now_turn + j
                    break
                # 然后判断是否有人碰 ，有则将牌堆中的这张牌取出
                t = self.players[(self.now_turn + j ) % 4].think_pong(last_tile)
                if t != -1:
                    last_tile = t
                    self.next_player(self.now_turn + j +1)
                    break

            # print("当前打出的牌:", utils.get_Cnt_names(self.gametable.out_pile))
        # 游戏结束计算得分

    def get_evn(self, id):
        print(utils.get_cnt(self.players[id].tiles))

    def count_score(self):
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

    # def player_judge_hu(self):

    # def get_score(self, hu_id):
    #     for i in range(4):
    #
    #         if i == hu_id:
    #             if self.banker == i:
    #                 self.players[i].score+=self.score*3
    #             else:
    #                 self.players[i].score-=self.score
    #         else:
    #             if self.banker == i:
    #                 self.players[i].score-=self.score
    #             else:
    #                 self.players[i].score-=self.score


game = Game(round=4)
game.start()
