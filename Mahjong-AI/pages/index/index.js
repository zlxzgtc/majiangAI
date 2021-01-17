var tilesutil = require("../../utils/tilesutil")

const app = getApp()
Page({
  data: {
    whosturn: {},
    nowcard: {},
    huid: -1,
    pongid: -1,
    lastdiscard: [],
    finished: false,
    ponehand: [],
    ponecpk: [],
    ptwohand: [],
    ptwocpk: [],
    pthreehand: {},
    pthreecpk: [],
    pfourhand: {},
    pfourcpk: [],
    lastcount: {},
    score: [0, 0, 0, 0],
    desklist: [],
    recommandlist: {},
    eatchoice: 3,
    eatchoicelist: [],
    eatchoicetiles: [],
    mahjong: [
      {
        index: 0,
        address: "../../images/MJw1.png"
      }, {
        index: 1,
        address: "../../images/MJw2.png"
      }, {
        index: 2,
        address: "/images/MJw3.png"
      }, {
        index: 3,
        address: "/images/MJw4.png"
      }, {
        index: 4,
        address: "/images/MJw5.png"
      }, {
        index: 5,
        address: "/images/MJw6.png"
      }, {
        index: 6,
        address: "/images/MJw7.png"
      }, {
        index: 7,
        address: "/images/MJw8.png"
      }, {
        index: 8,
        address: "/images/MJw9.png"
      }, {
        index: 9,
        address: "/images/MJs1.png"
      }, {
        index: 10,
        address: "/images/MJs2.png"
      }, {
        index: 11,
        address: "/images/MJs3.png"
      }, {
        index: 12,
        address: "/images/MJs4.png"
      }, {
        index: 13,
        address: "/images/MJs5.png"
      }, {
        index: 14,
        address: "/images/MJs6.png"
      }, {
        index: 15,
        address: "/images/MJs7.png"
      }, {
        index: 16,
        address: "/images/MJs8.png"
      }, {
        index: 17,
        address: "/images/MJs9.png"
      }, {
        index: 18,
        address: "/images/MJt1.png"
      }, {
        index: 19,
        address: "/images/MJt2.png"
      }, {
        index: 20,
        address: "/images/MJt3.png"
      }, {
        index: 21,
        address: "/images/MJt4.png"
      }, {
        index: 22,
        address: "/images/MJt5.png"
      }, {
        index: 23,
        address: "/images/MJt6.png"
      }, {
        index: 24,
        address: "/images/MJt7.png"
      }, {
        index: 25,
        address: "/images/MJt8.png"
      }, {
        index: 26,
        address: "/images/MJt9.png"
      }, {
        index: 27,
        address: "/images/MJf1.png"
      }, {
        index: 28,
        address: "/images/MJf2.png"
      }, {
        index: 29,
        address: "/images/MJf3.png"
      }, {
        index: 30,
        address: "/images/MJf4.png"
      }, {
        index: 31,
        address: "/images/MJd3.png"
      }, {
        index: 32,
        address: "/images/MJd2.png"
      }, {
        index: 33,
        address: "/images/MJd1.png"
      },
    ]
  },
  onLoad() {
    var that = this
    wx.request({
      method: 'GET',
      dataType: 'json',
      url: 'http://127.0.0.1:5000/game_start',
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      success: res => {
        that.refreshall(that, res)
        that.setData({
          recommandlist: res.data["recommand"]
        })
      }
    })
    if (this.data.huid == 0) {
      this.end()
    }
  },
  end: function () {
    var that = this
    if (that.data.huid != -1) {
      var content = "此次游戏结束，赢家为：\n玩家" + that.data.huid + "\n最后得分为：\n玩家1：" + that.data.score[0] + "\n玩家2：" + that.data.score[1] + "\n玩家3：" + that.data.score[2] + "\n玩家4：" + that.data.score[3]
    } else {
      var content = "此次游戏结束，为流局。" + "\n最后得分为：\n玩家1：" + that.data.score[0] + "\n玩家2：" + that.data.score[1] + "\n玩家3：" + that.data.score[2] + "\n玩家4：" + that.data.score[3]
    }
    wx.showModal({
      title: '游戏结束',
      content: content,
      confirmText: '继续游戏',
      cancelText: '退出游戏',
      success: function (res) {
        if (res.confirm) {
          wx.redirectTo({
            url: '../index/index',
          })
        }
        else if (res.cancel) {
          wx.redirectTo({
            url: '../start/start',
          })
        }
      }
    })
  },
  pong: function (e) {
    var index = parseInt(e.currentTarget.dataset.index);
    var that = this
    console.log("111",index)
    var desklist = this.data.desklist
    tilesutil.pongTiles(index, (res) => {
      that.refreshall(that, res)
      console.log(res)
      if (index != -1) {
        this.remove(desklist, res.data["lastdiscard"])
        that.setData({
          desklist: desklist,
        })
      }
      console.log(desklist)
    })
  },
  eat: function (e) {
    var index = parseInt(e.currentTarget.dataset.index);
    var that = this
    tilesutil.eatTiles(index, (res) => {
      that.refreshall(that, res)
      console.log(res)
      var desklist = that.data.desklist
      if (index != 3) {
        this.remove(desklist, res.data["lastdiscard"])
        that.setData({
          desklist: desklist,
        })
      }
      var eatchoice = that.data.eatchoicelist[index]
      that.setData({
        eatchoice: eatchoice,
      })
      console.log(desklist)
    })
  },
  remove: function (array, val) {
    for (var i = 0; i < array.length; i++) {
      if (array[i] == val) {
        array.splice(i, 1);
        break
      }
    }
    return -1;
  },

  discard: function (e) {
    var index = parseInt(e.currentTarget.dataset.index);
    if (this.data.whosturn == 0) {
      var that = this
      tilesutil.discardTiles(index, (res) => {
        that.refreshall(that, res)
        console.log("pongid:", res.data["pong_id"])
        if (res.data["lastdiscard"] > -1) {
          var desklist = that.data.desklist.concat(res.data["lastdiscard"])
          that.setData({
            desklist: desklist,
            pongid: res.data["pong_id"],
          })
        }
        console.log(that.data.desklist)
      })
      if (this.data.huid != -1) {
        this.end()
      } else {
        this.nextplayer()

      }
      var a = setInterval(function () {
        if (that.data.huid != -1) {
          that.end()
          clearInterval(a)
        }else if (that.data.huid == -1 && that.data.finished) {
          that.end()
          clearInterval(a)
        }
         else {
          if (that.data.whosturn != 0 && that.data.pongid != 0) {
            that.nextplayer()
          } else if (that.data.pongid == 0) {
            clearInterval(a)
          } else if (that.data.whosturn == 0 && that.data.pongid != 0) {
            that.mo()
            console.log("pongid:", that.data.pongid)
            clearInterval(a)
          }
        }
      }, 2000)
    }
  },
  finished: function () {
    if (this.data.finished) {
      if (this.data.huid == -1)
        return "流局"
      else
        return "胡了"
    }
  },
  mo: function (callback) {
    var that = this
    wx.request({
      method: 'GET',
      dataType: 'json',
      url: 'http://127.0.0.1:5000/mo',
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      success: function (res) {
        callback && callback(res);
        that.refreshall(that, res)
        console.log("ponehand:", res.data["ponehand"])
        that.setData({
          eatchoicelist: res.data["eatchoicelist"],
          eatchoicetiles: res.data["eatchoicetiles"],
          recommandlist: res.data["recommand"]
        })
      }
    })
  },
  nextplayer: function (callback) {
    if (this.data.whosturn != 0) {
      var that = this
      wx.request({
        method: 'GET',
        dataType: 'json',
        url: 'http://127.0.0.1:5000/nextplayer',
        header: {
          'content-type': 'application/x-www-form-urlencoded'
        },
        success: function (res) {
          callback && callback(res)
          that.refreshall(that, res)
          console.log(res)
          if (res.data["lastdiscard"] > -1) {
            var desklist = that.data.desklist.concat(res.data["lastdiscard"])
            that.setData({
              desklist: desklist,
            })
          }
          console.log(that.data.desklist)
        }
      })
    }
  },
  refreshall: function (that, res) {
    that.setData({
      ponehand: res.data["ponehand"],
      ptwohand: res.data["ptwohand"],
      pthreehand: res.data["pthreehand"],
      pfourhand: res.data["pfourhand"],
      ponecpk: res.data["ponecpk"],
      ptwocpk: res.data["ptwocpk"],
      pthreecpk: res.data["pthreecpk"],
      pfourcpk: res.data["pfourcpk"],
      recommand: res.data["recommand"],
      lastcount: res.data["lastcount"],
      whosturn: res.data["whosturn"],
      lastdiscard: res.data["lastdiscard"],
      score: res.data["score"],
      huid: res.data["huid"],
      finished: res.data["finished"],
      pongid :res.data["pong_id"]
    })
  },
})
