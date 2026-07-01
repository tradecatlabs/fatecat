import type { Schema, Struct } from '@strapi/strapi';

export interface SignInDateSignInCalendar extends Struct.ComponentSchema {
  collectionName: 'components_sign_in_date_sign_in_calendars';
  info: {
    displayName: 'sign_in_calendar';
    icon: 'apps';
  };
  attributes: {};
}

export interface SignInDateSignInDateList extends Struct.ComponentSchema {
  collectionName: 'components_sign_in_date_sign_in_date_lists';
  info: {
    displayName: 'sign_in_date_list';
    icon: 'apps';
  };
  attributes: {
    sign_in_date: Schema.Attribute.Date;
  };
}

declare module '@strapi/strapi' {
  export module Public {
    export interface ComponentSchemas {
      'sign-in-date.sign-in-calendar': SignInDateSignInCalendar;
      'sign-in-date.sign-in-date-list': SignInDateSignInDateList;
    }
  }
}
