// pages/login/login.js
const utilcookie = require('../../utils/cookie.js')
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  getCookie:function(){
    wx.request({
      url: 'http://127.0.0.1:8000/api/v1.0/cookietest/',
      success:function(res){
        var cookie = utilcookie.getSessionIDFromResponse(res)
        console.log(cookie)
        //保存cookie
        utilcookie.setCookieToStorage(cookie)
      }
    })
  },
  sendCookie:function(){
    var newcookie = utilcookie.getCookieFromStorage()
    var header = {}
    header.Cookie = newcookie
    wx.request({
      url: 'http://127.0.0.1:8000/api/v1.0/cookietest2/',
      header:header,
      success:function(res){
        console.log(res)
      }
    })
  },

  // authorize:function(){
  //   wx.login({
  //     success:function(res){
  //       var code = res.code
  //       var appId = app.globarData.appId
  //       var nickname = app.globarData.userInfo.nickname
  //       wx.request({
  //         url: 'http://127.0.0.1:8000/api/v1.0/userview/',
  //         method:'post',
  //         data:{
  //           code:code,
  //           appId:appId,
  //           nickname:nickname
  //         },
  //         header:{
  //           'content-type':'application/json'
  //         },
  //         success:function(res){
  //           wx.showToast({
  //             title: '授权成功'
  //           })
  //           var cookie = utilcookie.getSessionIDFromResponse(res)
  //           utilcookie.setCookieToStorage(cookie)
  //           console.log(cookie)
  //         }
  //       })
  //     }
  //   })
  // },

  authorize: function () {
    console.log(app.globalData.userInfo)
    wx.login({
      success: function (res) {
        var code = res.code
        // var appId = app.globalData.appId
        var nickname = app.globalData.userInfo.nickName
        wx.request({
          url: 'http://127.0.0.1:8000/api/v1.0/userview/',
          method: 'POST',
          data: {
            code: code,
            // appId: appId,
            nickname: nickname
          },
          success: function (res) {
            wx.showToast({
              title: '授权成功'
            })
            var cookie = utilcookie.getSessionIDFromResponse(res)
            utilcookie.setCookieToStorage(cookie)
            console.log(cookie)
          }
        })
      }
    })
  },


  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

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