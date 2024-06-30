const {
  cats
} = require("../library/data");

Page({
  data: {
    catName: '',
    catUrl: '',
    catColor: '',
    catGender: '',
    catNeutered: '',
    catDate: '',
    catHealth: '',
    catPersonality: ''
  },
  onLoad: function (options) {
    const app = getApp(); // 获取全局应用实例
    const allCatsArray = app.globalData.allCatsArray;
    if (options.catsName) {
      const catsName = decodeURIComponent(options.catsName);
      const catInfo = allCatsArray.find(cat => cat[1] === catsName);
      console.log(catInfo)
      if (catInfo) {
        this.setData({
          catName: catsName,
          catUrl: catInfo[0],
          catColor: catInfo[2],
          catGender: catInfo[3],
          catNeutered: catInfo[4],
          catDate: catInfo[5],
          catHealth: catInfo[6],
          catPersonality: catInfo[7]
        });
      }
    }
  },
  onReady() {},
  onShow() {},
  onHide() {},
  onUnload() {},
  onPullDownRefresh() {},
  onReachBottom() {},
  onShareAppMessage() {}
});