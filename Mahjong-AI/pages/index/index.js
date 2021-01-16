var tilesutil = require("../../utils/tilesutil")

const app = getApp()
Page({
  data: {
    whosturn: {},
    nowcard: {},
    liuid:{},
    huid: -1,
    pongid:-1,
    chiid:{},
    lastdiscard:{},
    finished: false,
    ponehand: {},
    ponecpk: [],
    ptwohand: {},
    ptwocpk: [],
    pthreehand: {},
    pthreecpk: [],
    pfourhand: {},
    pfourcpk: [],
    lastcount: {},
    score: {},
    desklist: [],
    recommandlist:{},
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
        that.refreshall(that,res)
        console.log(res)
        // while(!that.data.finished){
          // setTimeout(function () {
          //   console.log(111)
          // }, 1000)
        // }
      }
    })

  },
  end: function () {
    var that = this
    wx.showModal({
      title: '游戏结束',
      content: '此次游戏结束，最后得分为：玩家一：' + this.data.score[0] + "，玩家二：" + this.data.score[1] + "，玩家三：" + this.data.score[2] + "，玩家四：" + this.data.score[3],
      confirmText: '继续游戏',
      cancelText: '退出游戏',
      success: function (res) {
        if (res.confirm) {
          this.setData({
            score: [0, 0, 0, 0],
            recommandlist: {}
          })
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
  discard: function (e) {
    var index = parseInt(e.currentTarget.dataset.index);
    if (this.data.whosturn == 0) {
      this.setData({
        nowcard: index
      })
      console.log(this.data.nowcard)
      var that = this
      tilesutil.discardTiles(index, (res) => {
        console.log(res)
        that.refreshall(that,res)
        console.log(res)
        var desklist = that.data.desklist.concat(res.data["lastdiscard"])
        that.setData({
          desklist:desklist
        })
          // console.log(res.data["huid"])
      })
    }
  },
  finished: function () { //用来修改页面显示
    if(this.data.finished){
      if(this.data.huid==-1)
        console.log("流局")
      else
        console.log(this.data.huid,"hule")
    }
  },
  nextplayer:function () {
    wx.request({
      method: 'GET',
      dataType: 'json',
      url: 'http://127.0.0.1:5000/nextplayer',
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      success: function (res) {
        callback && callback(res);
      }
    })
  },
  refreshall:function (that,res) {
    that.setData({
      ponehand:res.data["ponehand"],
      ptwohand:res.data["ptwohand"],
      pthreehand:res.data["pthreehand"],
      pfourhand:res.data["pfourhand"],
      ponecpk:res.data["ponecpk"],
      ptwocpk:res.data["ptwocpk"],
      pthreecpk:res.data["pthreecpk"],
      pfourcpk:res.data["pfourcpk"],
      recommand:res.data["recommand"],
      lastcount:res.data["lastcount"],
      whosturn:res.data["whosturn"],
      lastdiscard:res.data["lastdiscard"],
      score:res.data["score"],
      huid:res.data["huid"],
      finished:res.data["finished"],
    })
  }
})
