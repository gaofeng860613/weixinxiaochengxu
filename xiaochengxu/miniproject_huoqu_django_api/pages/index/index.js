//index.js
//获取应用实例
const app = getApp()
const cookieUtil = require('../../utils/cookie.js')

Page({
  data: {
    motto: 'Hello World',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),

    isAuthorized: false,
    constellationData: null,
    stockData: null,
    weatherData: null
  },
  // network_request: function () {
  //   wx.request({
  //     url: 'http://127.0.0.1:8000/api/v1.0/juhe/',

  //     header: {
  //       'content-type': 'application/json'
  //     },
  //     success(res) {
  //       console.log(res.data)
  //     }
  //   })
  // },
  updateData: function () {
    wx.showLoading({
      title: '加载中',
    })
    var that = this
    var cookie = cookieUtil.getCookieFromStorage()
    var header = {}
    header.Cookie = cookie
    console.log()
    wx.request({
      url: 'http://127.0.0.1:8000/api/v1.0/weather/',
      header: header,
      success: function (res) {
        console.log(res)
        that.setData({
          weatherData: res.data

        })
        wx.hideLoading()
      }
    })

  },

  onPullDownRefresh: function () {
    var that = this
    var cookie = cookieUtil.getCookieFromStorage()
    var header = {}
    header.Cookie = cookie
    wx.request({
      url: 'http://127.0.0.1:8000/api/v1.0/userstatus/',
      header: header,
      success: function (res) {
        var data = res.data
        if (data.is_authorized == 1) {
          that.setData({
            isAuthorized: true
          })
          that.updateData()
        } else {
          that.setData({
            isAuthorized: false
          })
          wx.showToast({
            title: '请先授权登录',
          })
        }
      }
    })
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onLoad: function () {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse){
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
  },
  getUserInfo: function(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  }
})
