import { Component } from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';

import * as fengshui from 'fengshui.js';
import * as d3 from 'd3';
/*
  Generated class for the FengshuiPage page.

  See http://ionicframework.com/docs/v2/components/#navigation for more info on
  Ionic pages and navigation.
*/
@Component({
  selector: 'page-fengshui-page',
  templateUrl: 'fengshui-page.html'
})
export class FengshuiPage {
	degree: number;
  fengshui_infos: Array<{xiang: string, shan: string, yun: string}>;

  constructor(public navCtrl: NavController, public navParams: NavParams) {}

  updateChanges(event) {
    var xiang = fengshui.getMountain(this.degree);
    var shan = fengshui.getOppositeMountain(xiang);
    var now=new Date();
    var yun = fengshui.getYun(now.getFullYear());

    this.fengshui_infos = [];
    this.fengshui_infos.push({
      xiang: xiang,
      shan: shan,
      yun: yun
    })

    d3.select("svg").remove();
    var svgContainer = d3.select('#fengshui').append("svg")
                                 .attr("width", 360)
                                 .attr("height", 360);
    fengshui.drawFeiXing(svgContainer, yun, shan, xiang, 360, 360);
  }

}
