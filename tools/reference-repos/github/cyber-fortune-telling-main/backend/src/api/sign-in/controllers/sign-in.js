'use strict';

/**
 * sign-in controller
 */

const { createCoreController } = require('@strapi/strapi').factories;

module.exports = createCoreController('api::sign-in.sign-in', ({ strapi }) => ({
  async signIn(ctx) {
    const { sign_in_uid, sign_in_date } = ctx.request.body;
    if (!sign_in_uid || !sign_in_date) {
      return ctx.badRequest('sign_in_uid and sign_in_date are required');
    }
    // 查找是否已存在该用户
    const existing = await strapi.entityService.findMany('api::sign-in.sign-in', {
      filters: { sign_in_uid },
    });
    let record;
    if (existing && existing.length > 0) {
      // 已存在，更新签到日期列表
      record = existing[0];
      let dateList = record.sign_in_date_list || [];
      if (!dateList.includes(sign_in_date)) {
        dateList.push(sign_in_date);
        await strapi.entityService.update('api::sign-in.sign-in', record.id, {
          data: { sign_in_date_list: dateList },
        });
      }
      ctx.send({ sign_in_uid, sign_in_date_list: dateList });
    } else {
      // 不存在，创建新记录
      const newRecord = await strapi.entityService.create('api::sign-in.sign-in', {
        data: {
          sign_in_uid,
          sign_in_date_list: [sign_in_date],
        },
      });
      ctx.send({ sign_in_uid, sign_in_date_list: [sign_in_date] });
    }
  },

  async getSignInDates(ctx) {
    const { sign_in_uid } = ctx.query;
    if (!sign_in_uid) {
      return ctx.badRequest('sign_in_uid is required');
    }
    const existing = await strapi.entityService.findMany('api::sign-in.sign-in', {
      filters: { sign_in_uid },
    });
    if (existing && existing.length > 0) {
      ctx.send({ sign_in_uid, sign_in_date_list: existing[0].sign_in_date_list || [] });
    } else {
      ctx.send({ sign_in_uid, sign_in_date_list: [] });
    }
  },
}));
