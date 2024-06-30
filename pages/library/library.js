const dataObj = require("../library/data.js");

Page({
  data: {},
  searchCats: function (e) {
    const searchInputValue = e.detail.value;
    const app = getApp();
    const allCatsArray = app.globalData.allCatsArray;
    const catInfo = allCatsArray.find(cat => cat[1] === searchInputValue);
    if (catInfo) {
      wx.navigateTo({
        url: `/pages/cat-Inf/cat-Inf?catsName=${encodeURIComponent(catInfo[1])}`,
      });
    } else {
      wx.showToast({
        title: '未查询到该猫咪！',
        icon: 'none',
      });
    }
  },
  toCatPage: function (event) {
    const catsName = event.currentTarget.dataset.catsname;
    wx.navigateTo({
      url: `/pages/cat-Inf/cat-Inf?catsName=${catsName}`
    });
  },
  onLoad(options) {
    this.setData({
      searchImage: dataObj.searchImage,
      searchInputValue: dataObj.searchInputValue,
      cats: dataObj.cats,
      showPopup: dataObj.showPopup,
    })
  },
  onReady() {},
  onShow() {},
  onHide() {},
  onUnload() {},
  onPullDownRefresh() {},
  onReachBottom() {},
  onShareAppMessage() {}
})