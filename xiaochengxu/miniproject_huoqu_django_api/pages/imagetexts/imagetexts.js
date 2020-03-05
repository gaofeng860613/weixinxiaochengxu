Page({
  data: {
    // 待上传的图片, 本地地址
    files: [],
    //下载的文件列表
    downloadedBackupedFiles: []

  },
  chooseImage: function (e) {
    var that = this;
    wx.chooseImage({
      sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
      success: function (res) {
        // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片
        that.setData({
          files: that.data.files.concat(res.tempFilePaths)
        });
      }
    })
  },
  previewImage: function (e) {
    wx.previewImage({
      current: e.currentTarget.id, // 当前显示图片的http链接
      urls: this.data.files // 需要预览的图片http链接列表
    })
  },
  // 上传图片文件
  uploadFiles: function () {
    for (var i = 0; i < this.data.files.length; i++) {
      var filePath = this.data.files[i]
      wx.uploadFile({
        url: 'http://127.0.0.1:8000/api/v1.0/loaderupdown/',
        filePath: filePath,
        name: 'test' + filePath,
        success: function (res) {
          console.log(res.data),
            console.log(typeof (res.data))
        }
      })
    }
  },
  // 下载图片
  downloadFile: function (imgItem) {
    var that = this
    wx.downloadFile({
      url: 'http://127.0.0.1:8000/api/v1.0/loaderupdown/',
      success: function (res) {
        console.log('成功了..')
        console.log(res.tempFilePath)
        console.log(res.filePath)
        var tmpPath = res.tempFilePath
        var newDownloadedBackupedFiles = that.data.downloadedBackupedFiles
        newDownloadedBackupedFiles.push(tmpPath)
        that.setData({
          downloadedBackupedFiles: newDownloadedBackupedFiles
        })
      }
    })
  },

  // 删除图片
  deleteBackup: function (imgItem) {
    wx.request({
      url: 'http://127.0.0.1:8000/api/v1.0/loaderupdown/?name=81f3.jpg',
      method: 'DELETE',
      success: function (res) {
        console.log(res.data)
        wx.showToast({
          title: '删除成功',
        })
      }
    })
  },

  // 长按确认删除函数
  longTapConfirm: function (e) {
    var that = this
    var confirmList = ["删除这个图片"]
    wx.showActionSheet({
      itemList: confirmList,
      success: function (res) {
        if (res.cancel) {
          return
        }
        var imageIndex = e.currentTarget.dataset.index
        var imageItem = that.data.downloadedBackupedFiles[imageIndex]
        var newList = that.data.downloadedBackupedFiles
        newList.splice(imageIndex, 1)
        that.setData({
          downloadedBackupedFiles: newList
        })
        that.deleteBackup(imageItem)
      }
    })
  },



});