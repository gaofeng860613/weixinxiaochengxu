//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    motto: 'Hello World',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    name:'我是邢总',
    array: [{ msg: '列表第一页' }, { msg: '列表第二页' }],
    array1:[{msg:app.globalDataabc}]
  },
  //事件处理函数
  dianji:function(){
    console.log('点击我')
    this.setData({name:'我是邢总啊'})
  },
  changan:function(){
    console.log('长按我')
  },
  testNetwork:function(event){
    wx.request({
      // url: 'http://www.imooc.com',
      url: 'http://apis.juhe.cn/ip/ipNew?ip=111.111.111.111&key=89b459c29d47c5f9f3de77ae80bcd21d',
      // url: 'http://127.0.0.1:8000/api/v1.0/image/',
      method:'GET',
      header:{},
      success:function(res){
        console.log(res.data)
      },
      fail:function(res){
        conlose.log('request failed.')
      }
    })
  },
  testStorage:function(){
    wx.setStorage({
      key: 'test',
      data: 'data',
    })
    wx.getStorage({
      key: 'test',
      success: function(res) {
        var data = res.data
        console.log('data from storage1:',data)
      },
    })
    var data = wx.getStorageSync('test')
    console.log('data from storage2:',data)
  },
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
