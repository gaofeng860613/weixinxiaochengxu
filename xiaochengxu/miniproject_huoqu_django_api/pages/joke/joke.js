// pages/joke/joke.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    content:[]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var timestamp = Date.parse(new Date())/1000;
    var that = this
    wx.request({
      url: 'http://v.juhe.cn/joke/content/list.php?sort=desc&page=2&pagesize=5&time=' + timestamp+'&key=7641f4a34d4ac69073e22c227843f89f',
      success:function(res){
        console.log(res.data)
        that.setData({
          content:res.data.result.data
        })
      },
      fail:function(res){
        console.log('笑话段子请求失败')
      }
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})