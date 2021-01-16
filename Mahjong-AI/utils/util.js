module.exports = {
  formatTime: formatTime,
  initCountDown: initCountDown,
  closeCountDown: closeCountDown,
}
const formatTime = date => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  return [year, month, day].map(formatNumber).join('/') + ' ' + [hour, minute, second].map(formatNumber).join(':')
}

const formatNumber = n => {
  n = n.toString()
  return n[1] ? n : '0' + n
}

/**
 * 倒计时函数
 * @param {Page} page 当前页面的`this`
 * @param {Number} countDownNum 倒计时的时间 单位`秒`
 * @param {Number} interval 时间间隔 单位`秒`
 * @description `disPlayTime` wxml 中实际显示的时间
 * @description `注意!` 需要在自己的页面中定义`timeout()`用于执行时间到了的操作
 */
function initCountDown(page, countDownNum, interval) {
  let that = page;
  let displayTime = countDownNum;
  that.setData({
    countDownNum: countDownNum,
    displayTime: countDownNum
  });
  that.setData({
    timer: setInterval(function () { 
      // 这里把setInterval赋值给变量名为timer的变量
      // 每隔一秒countDownNum就减一，实现同步
      // console.log(displayTime)
      countDownNum = (countDownNum - interval).toFixed(1)
      displayTime = Math.ceil(countDownNum)
      //然后把countDownNum存进data，好让用户知道时间在倒计着
      that.setData({
        countDownNum: countDownNum,
        displayTime: displayTime
      })
      //在倒计时还未到0时，这中间可以做其他的事情，按项目需求来
      if (page.data.displayTime == 0) {
        closeCountDown(page)
        page.timeout()
      }else if(page.data.displayTime> 0 && page.data.displayTime<=5){
        toggle(page,interval)
      }
    }, 1000 * interval)
  })

}
/**
 * @param {Page} page 页面的this
 */
function closeCountDown(page) {
  let that = page;
  clearInterval(that.data.timer);
  page.timer = null;
  page.time = 0;
}