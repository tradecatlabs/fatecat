import { Component, ViewChild } from '@angular/core';

import { Platform, MenuController, Nav } from 'ionic-angular';

import { StatusBar, Splashscreen } from 'ionic-native';

import { BagongPage } from '../pages/bagong-page/bagong-page';
import { BaziPage } from '../pages/bazi-page/bazi-page';
import { ZhanbuPage } from '../pages/zhanbu-page/zhanbu-page';
import { FengshuiPage } from '../pages/fengshui-page/fengshui-page';


@Component({
  templateUrl: 'app.html'
})
export class MyApp {
  @ViewChild(Nav) nav: Nav;

  // make BagongPage the root (or first) page
  rootPage: any = BagongPage;
  pages: Array<{title: string, component: any}>;

  constructor(
    public platform: Platform,
    public menu: MenuController
  ) {
    this.initializeApp();

    // set our app's pages
    this.pages = [
      { title: '八宫', component: BagongPage },
      { title: '八字', component: BaziPage },
      { title: '占卜', component: ZhanbuPage },
      { title: '风水', component: FengshuiPage }
    ];
  }

  initializeApp() {
    this.platform.ready().then(() => {
      // Okay, so the platform is ready and our plugins are available.
      // Here you can do any higher level native things you might need.
      StatusBar.styleDefault();
      Splashscreen.hide();
    });
  }

  openPage(page) {
    // close the menu when clicking a link from the menu
    this.menu.close();
    // navigate to the new page if it is not the current page
    this.nav.setRoot(page.component);
  }
}
