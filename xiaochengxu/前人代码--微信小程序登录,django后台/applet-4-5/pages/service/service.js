// pages/service/service.js

const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    isConstellationView: false,
    isJokeView: false,
    constellationData: null,
    jokeData: null
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    console.log(options)
    var isConstellationViewTmp = false
    var isJokeViewTmp = false
    if (options.type == 'joke'){
      isJokeViewTmp = true
      this.updateJokeData()
    }else{
      isConstellationViewTmp = true
      this.updateConstellationData()
    }
    this.setData({
      isConstellationView: isConstellationViewTmp,
      isJokeView: isJokeViewTmp
    })
  },

  updateConstellationData: function() {
    wx.showLoading({
      title: '加载中',
    })
    var that = this; {
      var header = {}
      if (this.data.isAuthorized) {
        const cookie = cookieUtil.getCookieFromStorage()
        header.Cookie = cookie
      }
      wx.request({
        url: app.globalData.serverUrl + app.globalData.apiVersion + '/service/constellation',
        header: header,
        success(res) {
          that.setData({
            constellationData: res.data.data
          })
          wx.hideLoading()
        }
      })
    }
  },

  updateJokeData: function () {
    wx.showLoading({
      title: '加载中',
    })
    var that = this; {
      var header = {}
      if (this.data.isAuthorized) {
        const cookie = cookieUtil.getCookieFromStorage()
        header.Cookie = cookie
      }
      wx.request({
        url: app.globalData.serverUrl + app.globalData.apiVersion + '/service/joke',
        header: header,
        success(res) {
          console.log(res.data)
          that.setData({
            jokeData: res.data.data
          })
          wx.hideLoading()
        }
      })
    }
  },
})