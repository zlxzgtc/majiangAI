module.exports = {
  discardTiles: discardTiles,
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