// pages/apps/apps.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    grids: ['应用名1','应用名2']
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // 调用一个方法来获取djiango后台的数据,并且将获取到的内容更新到九宫格
    this.updateMenuData()
  },

  updateMenuData:function(){
    var appnames = this
    //去后台获取数据
    wx.request({
      url:app.globalData.appurl,
      // url: app.globalData.appurl + app.globalData.appv + app.globalData.routeapp,
      success:function(res){
        //更新数据
        console.log('成功')
        console.log(res.data)
        appnames.setData({grids: res.data.publish})
      },
      fail:function(res){
        console.log(res.errMsg)
      }
    })
  },

  onNavigatorTap:function(e){
    var index = e.currentTarget.dataset.index
    // wx.showToast({
    //   title: 'index+',
    // })
    var item = this.data.grids[index]
    // wx.showToast({
    //   title: item.app.name,
    // })
    if (item.app.name == '微信'){
      wx.navigateTo({
        url: '/pages/weixin/weixin',
      })
    } else if (item.app.name == '支付宝'){
      wx.navigateTo({
        url: '/pages/zfb/zfb',
      })
    } else if (item.app.name == '笑话展现') {
      wx.navigateTo({
        url: '/pages/joke/joke',
      })
    }
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
    wx.updateShareMenu({
      withShareTicket:true,
      success(){}
    })
  }
})