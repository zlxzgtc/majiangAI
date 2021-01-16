from random import shuffle
import utils


class Gametable():
    type = ["万", "条", "筒"]
    s_type = ["东", "南", "西", "北", "白", "发", "中"]
    out_pile = [0] * 34  # 桌上已经打出的牌

    def __init__(self, debug=False):
        # 创建一副牌
        self.Tiles = list(range(0, 34)) * 4
        # 数字对应牌型0-8:"万";9-17:"条";18-26:"桶";27-33:"东","南","西","北","白","发","中"
        self.debug = debug
        self.shuffle()

    def shuffle(self):
        # self.draw_loc = 0
        # self.receive_cnt = [0] * 34
        # self.receive_tiles = []
        if self.debug:
            self.Tiles = [25, 26, 22, 28, 24, 14, 12, 16, 12, 13, 20, 2, 26, 30, 17, 33, 9, 22, 31, 33, 27, 19, 25, 20,
                          11, 2, 22, 20, 25, 4, 32, 4, 16, 28, 19, 5, 24, 29, 26, 7, 20, 15, 0, 24, 9, 11, 25, 15, 2,
                          27, 30, 22, 31, 18, 6, 4, 29, 16, 14, 3, 9, 21, 3, 21, 8, 17, 1, 13, 29, 11, 18, 2, 23, 32,
                          10, 31, 1, 7, 12, 15, 19, 6, 14, 17, 4, 28, 32, 23, 1, 17, 14, 33, 27, 5, 8, 10, 18, 13, 21,
                          8, 30, 1, 26, 28, 0, 7, 3, 5, 21, 30, 12, 8, 5, 7, 10, 15, 9, 10, 13, 31, 19, 6, 23, 29, 18,
                          23, 32, 27, 0, 6, 3, 24, 33, 11, 0, 16]
        else:
            shuffle(self.Tiles)

    # 将打出的牌放到牌堆中
    def put_pile(self, tile):
        self.out_pile[tile] += 1

    def give_pile(self):
        if len(self.Tiles) == 8:  # 流局
            return -1
        else:
            tile = self.Tiles[0]
            # print("给出一张牌-------------" + str(utils.get_tile_name(tile)) + ",--------当前余牌量：" + str(len(self.Tiles)))
            del self.Tiles[0]
            return tile

    # def draw(self):
    #     if self.draw_loc >= 136:
    #         return "End"
    #     t = self.Tiles[self.draw_loc]
    #     self.draw_loc += 1
    #
    #     return t
