'use strict';

/**
 * sign-in service
 */

const { createCoreService } = require('@strapi/strapi').factories;

module.exports = createCoreService('api::sign-in.sign-in');
