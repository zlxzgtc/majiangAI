import game_table


# 麻将牌的名称
def get_tile_name(t):
    if t >= 0:
        if t <= 26:
            return str(t % 9 + 1) + game_table.Gametable.type[t // 9]
        elif t <= 33:
            return game_table.Gametable.s_type[t - 27]
    return ''


# 一次性输出一堆牌的名称
def get_Tiles_names(tiles):
    names = ''
    for t in tiles:
        names += get_tile_name(t) + ' '
    return names


# 输出已经打出的牌
def get_Cnt_names(cnt):
    names = ''
    for i in range(len(cnt)):
        e = cnt[i]
        while (e > 0):
            names += get_tile_name(i) + ' '
            e -= 1
    return names


# 返回每一种牌的数目
def get_cnt(tiles):
    cnt = [0] * 34
    for i in range(34):
        cnt[i] = tiles.count(i)
    return cnt


def get_eat_cnt(choice):
    cnt = [0] * 4
    for c in choice:
        cnt[c] += 1
    return cnt

def get_pong_cnt(choice):
    cnt = [0] * 2
    for c in choice:
        cnt[c] += 1
    return cnt