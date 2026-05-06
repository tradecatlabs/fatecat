import { NgModule, ErrorHandler } from '@angular/core';
import { IonicApp, IonicModule, IonicErrorHandler } from 'ionic-angular';
import { MyApp } from './app.component';
import { BagongPage } from '../pages/bagong-page/bagong-page';
import { BaziPage } from '../pages/bazi-page/bazi-page';
import { ZhanbuPage } from '../pages/zhanbu-page/zhanbu-page';
import { FengshuiPage } from '../pages/fengshui-page/fengshui-page';

@NgModule({
  declarations: [
    MyApp,
    BagongPage,
    BaziPage,
    ZhanbuPage,
    FengshuiPage
  ],
  imports: [
    IonicModule.forRoot(MyApp)
  ],
  bootstrap: [IonicApp],
  entryComponents: [
    MyApp,
    BagongPage,
    BaziPage,
    ZhanbuPage,
    FengshuiPage
  ],
  providers: [{provide: ErrorHandler, useClass: IonicErrorHandler}]
})
export class AppModule {}
