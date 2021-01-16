module.exports = {
  discardTiles: discardTiles,
  pongTiles: pongTiles,
  eatTiles: eatTiles,
}
function discardTiles(index, callback) {
  wx.request({
    method: 'POST',
    dataType: 'json',
    url: 'http://127.0.0.1:5000/discard',
    header: {
      'content-type': 'application/x-www-form-urlencoded'
    },
    data: {
      nowcard:index,
    },
    success: function (res) {
      callback && callback(res);
    }
  })
}
function pongTiles(ifpong, callback) {
  wx.request({
    method: 'POST',
    dataType: 'json',
    url: 'http://127.0.0.1:5000/pong',
    header: {
      'content-type': 'application/x-www-form-urlencoded'
    },
    data: {
      ifpong:ifpong,
    },
    success: function (res) {
      callback && callback(res);
    }
  })
}
function eatTiles(eatchoice, callback) {
  wx.request({
    method: 'POST',
    dataType: 'json',
    url: 'http://127.0.0.1:5000/eat',
    header: {
      'content-type': 'application/x-www-form-urlencoded'
    },
    data: {
      eatchoice:eatchoice,
    },
    success: function (res) {
      callback && callback(res);
    }
  })
}