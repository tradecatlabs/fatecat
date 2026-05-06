import { Component } from '@angular/core';
import * as iching from "iching.js";

@Component({
  selector: 'page-hello-ionic',
  templateUrl: 'bagong-page.html'
})
export class BagongPage {
  upper_yao: string;
  lower_yao: string;
  gua_infos: Array<{title: string, gong: string, name: string, wuxing: string}>;
  items: Array<{title: string}>;
  constructor() {
    this.items = [];
    for(let i = 0; i < 8; i++) {
        this.items.push({
            title: iching.getTrigrams()[i]
        })
    }
  }

  updateSelectedValue() {
    if(this.upper_yao && this.lower_yao) {
      var hexagram = iching.trigram2hexagram(this.upper_yao, this.lower_yao);
      var gong = iching.getGongName(hexagram);
      var name = iching.getHexagramName(hexagram);
      var wuxing = iching.getWuXing(gong);
      this.gua_infos = [];
      this.gua_infos.push({
        title: hexagram,
        gong: gong,
        name: name,
        wuxing: wuxing
      })
    }
  }

}
