from copy import deepcopy


def get_hu_dis(tiles):
    x, y = 0, 0  # x表示需替换1张，y表示需替换两张
    tiles_copy = deepcopy(tiles)
    cnt = get_cnt(tiles)
    for i in range(3):
        for j in range(9):
            t = i * 9 + j
            if cnt[t] > 0:
                if cnt[t] == 2:
                    tiles.remove(t)
                    tiles.remove(t)
                    cnt[t] -= 2
                    x += 1
                else:
                    if j < 7:
                        if cnt[t + 1] > 0:
                            tiles.remove(t)
                            tiles.remove(t + 1)
                            cnt[t] -= 1
                            cnt[t + 1] -= 1
                            x += 1
                        elif cnt[t + 2] > 0:
                            tiles.remove(t)
                            tiles.remove(t + 2)
                            cnt[t] -= 1
                            cnt[t + 2] -= 1
                            x += 1
                    elif j == 8:
                        if cnt[t + 1] > 0:
                            tiles.remove(t)
                            tiles.remove(t + 1)
                            cnt[t] -= 1
                            cnt[t + 1] -= 1
                            x += 1
    for i in range(27, 34):
        if cnt[i] == 2:
            tiles.remove(i)
            tiles.remove(i)
            x += 1
    y = len(tiles)
    #  计算向听量
    if x * 3 >= len(tiles_copy):
        count = len(tiles_copy) / 3
    else:
        count = x + (y - x) / 3 * 2
    if len(tiles_copy) % 3 != 0:
        count += 1
    return int(count)


def get_cnt(tiles):
    cnt = [0] * 34
    for i in range(34):
        cnt[i] = tiles.count(i)
    return cnt


# 返回胡牌距离 now_dis=0，则胡了
def hu_distance(tiles, t=-1):
    now_tile = deepcopy(tiles)
    if t != -1:
        now_tile.append(t)
    cnt = get_cnt(now_tile)
    tile_copy = deepcopy(now_tile)
    now_dis = 11
    has_DD = False
    for i in range(34):
        if cnt[i] >= 2:
            has_DD = True
            tile_copy.remove(i)
            tile_copy.remove(i)
            k = search_AAA(tile_copy)
            if k < now_dis:
                now_dis = k
            if now_dis == 0:
                break
            tile_copy += [i, i]
    if not has_DD:
        k = search_AAA(tile_copy)
        if k < now_dis:
            now_dis = k
    return now_dis


def search_AAA(now_tile):
    cnt = get_cnt(now_tile)
    tile_copy = deepcopy(now_tile)
    for i in range(34):
        if cnt[i] >= 3:
            tile_copy.remove(i)
            tile_copy.remove(i)
            tile_copy.remove(i)
    return search_BCD(tile_copy)


def search_BCD(now_tile):
    if len(now_tile) == 0:
        return 0
    else:
        tile_copy = deepcopy(now_tile)
        cnt = get_cnt(tile_copy)
        for i in range(3):
            for j in range(7):
                t = i * 9 + j
                if cnt[t] >= 1 and cnt[t + 1] >= 1 and cnt[t + 2] >= 1:
                    tile_copy.remove(t)
                    tile_copy.remove(t + 1)
                    tile_copy.remove(t + 2)
                    cnt[t] -= 1
                    cnt[t + 1] -= 1
                    cnt[t + 2] -= 1
        return get_hu_dis(tile_copy)


# t = [1, 1, 1, 3, 3, 4, 4, 4, 5, 5, 8, 9, 11, 12]
# print(hu_distance(t))
