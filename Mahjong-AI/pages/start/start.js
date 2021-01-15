Page({

  data: {
    choosed:[false,false],
    degree: {},
  },
  start: function (res) {
      wx.redirectTo({
        url: '../index/index',
      })
  },
  choose: function (e) {
    var index = parseInt(e.currentTarget.dataset.index);
    var flag = this.data.choosed;
    var i;
    for (i = 0; i < 2; i++) {
      if (i != index)
        flag[i] = false;
      else
        flag[i] = true;
    }
    this.setData({
      choosed: flag,
      degree: index
    })
    console.log(this.data.degree)
  },
})