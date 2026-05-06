import { Component } from '@angular/core';

import { NavController, NavParams } from 'ionic-angular';
import * as lunarCalendar from 'lunar-calendar';
import * as iching from 'iching.js';
import * as d3 from 'd3';


@Component({
  selector: 'page-list',
  templateUrl: 'bazi-page.html'
})
export class BaziPage {
  calendar: string;
  birthday: string;
  birthtime: string;
  gua_infos: Array<{sizhu: string, gong: string, name: string, wuxing: string}>;

  constructor(public navCtrl: NavController, public navParams: NavParams) {

  }

  updateChanges() {
    if (this.calendar && this.birthday && this.birthtime) {
      var lunarInfo;
      var dateArray = this.birthday.split('-');
      if (this.calendar == 'solar') {
        lunarInfo = lunarCalendar.solarToLunar(dateArray[0], dateArray[1], dateArray[2]);
      } else {
        var solarInfo = lunarCalendar.lunarToSolar(dateArray[0], dateArray[1], dateArray[2]);
        lunarInfo = lunarCalendar.solarToLunar(solarInfo.year, solarInfo.month, solarInfo.day);
      }
      var upper_yao = iching.getXianTianBaGua(Math.round(lunarInfo.lunarDay));
      var lower_yao = iching.getXianTianBaGua(lunarInfo.lunarMonth);
      var hexagram = iching.trigram2hexagram(upper_yao, lower_yao);
      var gong = iching.getGongName(hexagram);
      var name = iching.getHexagramName(hexagram);
      var wuxing = iching.getWuXing(gong);
      var sizhu = lunarInfo.GanZhiYear + '年 ' + lunarInfo.GanZhiMonth + '月 ' + lunarInfo.GanZhiDay + '日';
      this.gua_infos = [];
      this.gua_infos.push({
        sizhu: sizhu,
        gong: gong,
        name: name,
        wuxing: wuxing
      });

      d3.select("svg").remove();
      var svgContainer = d3.select('#bazi').append("svg")
                           .attr("width", 400)
                           .attr("height", 420);
      iching.drawTrigrams(svgContainer, upper_yao, lower_yao, lunarInfo.GanZhiDay.substring(0,1));
    }
  }
}
