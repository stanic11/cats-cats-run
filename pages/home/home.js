import Dialog from '../../dist/dialog/dialog';
const uploadApiUrl = 'http://localhost:5000/upload';

Page({
  data: {
    swiperMaps: [
      "/resource/banner/1.png",
      "/resource/banner/2.png",
      "/resource/banner/3.png"
    ]
  },
  takePhoto: function () {
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      sourceType: ['album', 'camera'],
      success: (res) => {
        const filePath = res.tempFiles[0].tempFilePath;
        this.uploadImage(filePath);
      },
      fail: (err) => {
        if (err.errMsg.includes('auth deny')) {
          wx.showModal({
            title: '权限请求',
            content: '为了使用拍照或从相册选择图片的功能，我们需要您开启相应的权限。',
            showCancel: false,
            success: (res) => {
              if (res.confirm) {
                wx.openSetting({
                  success: (settingdata) => {
                    if (settingdata.authSetting['scope.camera'] && settingdata.authSetting['scope.album']) {
                      this.takePhoto();
                    } else {
                      wx.showToast({
                        title: '需要开启权限才能使用',
                        icon: 'none'
                      });
                    }
                  }
                });
              }
            }
          });
        }
      }
    });
  },
  uploadImage: function (filePath) {
    wx.uploadFile({
      url: uploadApiUrl,
      filePath: filePath,
      name: 'image',
      success: (res) => {
        console.log('后端响应:', res);
        try {
          const data = JSON.parse(res.data);
          if (data.error) {
            this.showFailDialog();
          } else {
            if (data.predicted_class !== undefined && data.confidence !== undefined) {
              if (data.confidence > 0.6) {
                console.log('预测结果:', data.predicted_class);
                this.showSuccessDialog(data.predicted_class)
              } else {
                console.log('发现新物种');
                this.newSpeciesSolution(filePath);
              }
            }
          }
        } catch (e) {
          console.error('处理服务器响应时出错:', e, '服务器返回:', res.data);
          wx.showToast({
            title: '处理响应出错',
            icon: 'none'
          });
        }
      },
      fail: (err) => {
        this.showFailDialog();
      }
    });
  },
  newSpeciesSolution: function (filePath) {
    // 获取token
    wx.request({
      url: `https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Rwfaf0S2F8h62fazH1eTZyLc&client_secret=OnZNvgUxUTeYHkFeB8r6hASnaJ2UNnup`,
      method: 'POST',
      success: (res) => {
        const token = res.data.access_token;
        this.recognizeImage(filePath, token);
      },
      fail: (err) => {
        console.error('获取token失败', err);
        wx.showToast({
          title: '获取token失败',
          icon: 'none'
        });
      }
    });
  },
  recognizeImage: function (filePath, token) {
    wx.getFileSystemManager().readFile({
      filePath: filePath,
      encoding: 'base64',
      success: (res) => {
        const base64Img = res.data;
        wx.request({
          url: `https://aip.baidubce.com/rest/2.0/image-classify/v1/animal?access_token=${token}`,
          method: 'POST',
          header: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          data: {
            image: base64Img
          },
          success: (res) => {
            if (res.data.result && res.data.result.length > 0) {
              const maxResult = res.data.result.reduce((prev, current) => (prev.score > current.score) ? prev : current);
              console.log('识别结果', maxResult);
              this.showNewDialog(maxResult.name);
            }
          },
          fail: (err) => {
            console.error('图像识别失败', err);
            this.showFailDialog();
          }
        });
      },
      fail: (err) => {
        console.error('读取文件失败', err);
        this.showFailDialog();
      }
    });
  },
  onLoad(options) {},
  onReady() {},
  onShow() {},
  onHide() {},
  onUnload() {},
  onPullDownRefresh() {},
  onReachBottom() {},
  onShareAppMessage() {},
  showSuccessDialog: function (cat_name) {
    Dialog.confirm({
      title: '恭喜',
      message: `您发现了可爱的${cat_name}!\n可以在猫猫档案查看Ta的详细信息！`,
      messageAlign: 'left',
      showConfirmButton: 'true',
      showCancelButton: 'true',
    }).then(() => {
      console.log('用户关闭了弹窗');
    });
  },
  showFailDialog: function () {
    Dialog.confirm({
      title: '错误',
      message: `您上传的图像中可能没有猫脸！\n请重新上传图像或拍照！`,
      messageAlign: 'left',
      showConfirmButton: 'true',
      showCancelButton: 'true',
    }).then(() => {
      console.log('用户关闭了弹窗');
    });
  },
  showNewDialog: function (cat_specics) {
    Dialog.confirm({
      title: '恭喜',
      message: `您发现了全新的${cat_specics}!\n您将获得它的取名权！`,
    }).then(() => {
      console.log('用户关闭了弹窗');
    });
  }
});