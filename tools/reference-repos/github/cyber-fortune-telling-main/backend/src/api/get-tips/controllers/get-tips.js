'use strict';

/**
 * A set of functions called "actions" for `get-tips`
 */

module.exports = {
  getTips: async (ctx, next) => {
    const { query } = ctx.request;
    console.log("==query get-tips==", query);
    // 办公桌东南方摆绿植
    // 手机壁纸换成蓝色系
    // 给久未联系的朋友发条问候
    // 午餐加一份绿色蔬菜
    // 整理钱包，清理过期票据
    // 佩戴银饰增强气场
    // 记录今日灵感笔记
    // 睡前听15分钟轻音乐
    // 检查手机app权限设置
    // 对镜子微笑三次
    // 写下一句今日感恩的话
    const tips = [
      "办公桌东南方摆绿植",
      "手机壁纸换成蓝色系",
      "给久未联系的朋友发条问候",
      "午餐加一份绿色蔬菜",
      "整理钱包，清理过期票据",
      "佩戴银饰增强气场",
      "记录今日灵感笔记",
      "睡前听15分钟轻音乐",
      "检查手机app权限设置",
      "对镜子微笑三次",
      "写下一句今日感恩的话"
    ]

    // 随机获取一个提示
    const randomIndex = Math.floor(Math.random() * tips.length);
    const randomTip = tips[randomIndex];

    try {
      ctx.body = {
        username: "zhaoolee",
        randomTip: randomTip,
      };
    } catch (err) {
      ctx.body = err;
    }
  }
};
