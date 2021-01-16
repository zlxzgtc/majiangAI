# m * AAA + n * BCD + EE
# 遍历EE，递归搜索ABC , 剩余是否均为AAA
# def think_hu(self,t=-1):
#     now_tile = deepcopy(self.tiles)
#     if t!=-1:
#         now_tile.append(t)
#     cnt = self.get_cnt(now_tile)
#     for i in range(34):
#         if cnt[i] > 0:
#             if cnt[i] >= 2:
#                 now_tile.remove(i)
#                 now_tile.remove(i)
#                 if self.search_BCD(now_tile):
#                     return True
#                 else:
#                     now_tile += [i, i]
#             else:
#                 # 如果没有顺子和三张剪枝
#                 if not self.is_AAA(i) and not self.is_BCD(i):
#                     return False
#     else:
#         return self.search_BCD(now_tile)


# 找顺子 ，递归的找，如果剩下的只有三张，则胡了
# 0-8:"万";9-17:"条";18-26:"筒"
# def search_BCD(self, now_tile):
#     if self.search_AAA(now_tile):
#         return True
#     else:
#         if len(now_tile) == 0:
#             return True
#         temp = deepcopy(now_tile)
#         cnt = self.get_cnt(temp)
#         for i in range(34):
#             if cnt[i] > 0:
#                 if 0 <= i <= 6 or 9 <= i <= 15 or 18 <= i <= 24:  # 1-7
#                     if cnt[i] > 0 and cnt[i + 1] > 0 and cnt[i + 2] > 0:
#                         temp.remove(i)
#                         temp.remove(i + 1)
#                         temp.remove(i + 2)
#                         if self.search_BCD(temp):
#                             return True
#                         temp += [i, i + 1, i + 2]
#     return False


# 剩余牌是否都是三张
# def search_AAA(self, now_tile):
#     cnt = set(self.get_cnt(now_tile))
#     return cnt <= {0, 3}
# 移除余牌中所有的刻子后的向听数

# def think_gang(self, tile):
#     if self.type == 'human':
#         if self.is_gang(tile):
#             print('是否要杠?(y/n)')
#             flag = input()
#             if flag == 'y':
#                 self.tiles.remove(tile)
#                 self.tiles.remove(tile)
#                 self.tiles.remove(tile)
#                 self.pong_tiles.append([tile] * 4)
#                 return True
#             else:
#                 return False
#     else:
#         if self.is_gang(tile):
#             self.tiles.remove(tile)
#             self.tiles.remove(tile)
#             self.tiles.remove(tile)
#             self.pong_tiles.append([tile] * 4)
#             return True
#         else:
#             return False


# 判断能不能杠
# def is_gang(self, tile):
#     return self.tiles.count(tile) == 3