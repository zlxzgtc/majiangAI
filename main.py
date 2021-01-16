from flask import Flask, request
import game_main,json
import game_table,utils

app = Flask(__name__)
game = {}
def creatres():
    res = {
        #手牌
        "ponehand":game.players[0].tiles,
        "ptwohand":game.players[1].tiles,
        "pthreehand":game.players[2].tiles,
        "pfourhand":game.players[3].tiles,
        #吃碰的牌
        "ponecpk":list(game.players[0].eat_tiles) + list(game.players[0].pong_tiles),
        "ptwocpk":list(game.players[1].eat_tiles )+ list(game.players[1].pong_tiles),
        "pthreecpk":list(game.players[2].eat_tiles) +list (game.players[2].pong_tiles),
        "pfourcpk":list(game.players[3].eat_tiles )+list (game.players[3].pong_tiles),
        #推荐的牌
        "recommand":[6],
        #剩余的牌数
        "lastcount":len(game.game_table.Tiles),
        #当前出牌者id
        "whosturn":game.now_turn,
        #上一个人出的牌
        "lastdiscard":game.last_tile,
        #玩家得分
        "score":[game.players[0].score,game.players[1].score,game.players[2].score,game.players[3].score],
        #胡碰的玩家的id
        "huid":game.hu_id,
        #是否流局
        "finished":game.finished,
    }
    return res 

@app.route('/game_start')
def game_start():
    players=['human', 'computer', 'computer', 'computer']
    global game 
    game = game_main.Game(players=players,round=1)
    game.game_table = game_table.Gametable(True)  # 创建牌堆
    game.now_turn = 0
    game.no_hu = False
    for k in range(4):  # 玩家上局手牌清空
        game.players[k].game_init()
    for k in range(0, 16):
        for j in range(4):
            game.players[j].add_tiles(game.game_table.give_pile())

    game.mo(player_id = game.now_turn)
    res = creatres()
    res["recommand"]=[game.players[0].computer_choose()]
    return res

@app.route('/mo')
def mo(): #如果能吃，就返回eatchoice 
    game.players[0].sort_tiles()
    if len(game.game_table.Tiles)==71:
        # game.mo(player_id = game.now_turn)
        game.player_think_hu()
        res = creatres()
    else:
        choice = game.players[0].is_eat(game.last_tile) #关于吃的选项
        # choice.append(3)
        print("choice",choice)
        print(game.now_turn)
        if len(choice) == 0:
            game.mo(player_id = game.now_turn)
            game.player_think_hu()
            res = creatres()
            res["eatchoicelist"] = choice
        else :
            res = creatres()
            res["eatchoicelist"] = choice
            eatchoicetiles = []
            for i in range(len(choice)):
                if choice[i] == 0:
                    eatchoicetiles.append([game.last_tile, game.last_tile + 1, game.last_tile + 2])
                elif choice[i] == 1:
                    eatchoicetiles.append([game.last_tile - 1, game.last_tile, game.last_tile + 1])
                else:
                    eatchoicetiles.append([game.last_tile - 2, game.last_tile - 1, game.last_tile])
            print("eatchoicetiles",eatchoicetiles)
            res["eatchoicetiles"] = eatchoicetiles
        res["recommand"]=[game.players[0].computer_choose()]
        print(res["recommand"])
    return res

@app.route('/eat',methods=['POST'])
def eat():
    c = int(request.form['eatchoice'])
    print("吃"+str(c))
    player = game.players[0]
    print(utils.get_Tiles_names(player.tiles))
    print(utils.get_tile_name(game.last_tile))
    if c==3:# buchi
        game.mo(player_id = game.now_turn)
        game.player_think_hu()
    else:
        if c == 0:  # 吃左边
            player.tiles.remove(game.last_tile + 1)
            player.tiles.remove(game.last_tile + 2)
            player.eat_tiles = player.eat_tiles + [game.last_tile, game.last_tile + 1, game.last_tile + 2]
        elif c == 1:  # 吃中间
            player.tiles.remove(game.last_tile - 1)
            player.tiles.remove(game.last_tile + 1)
            player.eat_tiles = player.eat_tiles + [game.last_tile - 1, game.last_tile, game.last_tile + 1]
        else:  # 吃右边
            player.tiles.remove(game.last_tile - 1)
            player.tiles.remove(game.last_tile - 2)
            player.eat_tiles = player.eat_tiles + [game.last_tile - 2, game.last_tile - 1, game.last_tile]       
    res = creatres()
    return res

@app.route('/discard', methods=["POST"])
def discard():
    print(game.players[0].tiles)
    t=int(request.form['nowcard'])
    game.last_tile=t
    game.players[0].out_tiles(t=t)
    game.game_table.put_pile(t)
    game.others_think_hu(game.last_tile)
    res = creatres()
    if game.hu_id == -1:
        pong_id = game.others_think_pong(game.last_tile)
        if pong_id != -1:
            game.next_player(pong_id % 4)
            game.last_tile = game.player_think_out()
            game.next_player()
        else:
            game.next_player()
        res = creatres()
        res["pong_id"] = pong_id
    
    return res

@app.route('/pong', methods=["POST"])
def pong():
    print(game.players[0].tiles)
    pong_id=int(request.form['ifpong'])
    if pong_id == -1:
        game.tiles.remove(game.last_tile)
        game.tiles.remove(game.last_tile)
        game.pong_tiles+=[game.last_tile] * 3
    else:
        game.next_player()
    res = creatres()
    return res


@app.route('/nextplayer', methods=["GET"])
def nextplayer():
    now_turn = game.now_turn
    c = game.player_think_eat(game.last_tile)
    print("c",c)
    pong_id=-1
    if c != 3: 
        game.last_tile = game.player_think_out()
        game.next_player()
    else:
        if game.mo(game.now_turn) == -1:  # 摸牌
            game.finished = True
        else:
            game.player_think_hu()
            game.last_tile = game.player_think_out()
            game.game_table.put_pile(game.last_tile)
            game.next_player()
            game.others_think_hu(game.last_tile)
            pong_id = game.others_think_pong(game.last_tile)
            
            if pong_id != -1 :
                if pong_id !=0:
                    game.next_player(pong_id % 4)
                    game.last_tile = game.player_think_out()
                    game.next_player()
                    res = creatres()
                    res["pong_id"] = game.now_turn
                else:
                    game.next_player(pong_id % 4)
                    res = creatres()
                    res["pong_id"] = game.now_turn
    print("pong_id",pong_id)
    res = creatres()
    # res["pong_id"] = game.now_turn
    return res




if __name__ == '__main__':
    app.run()



    