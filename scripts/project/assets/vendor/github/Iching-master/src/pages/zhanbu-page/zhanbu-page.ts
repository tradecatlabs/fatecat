import { Component } from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';
import * as lunarCalendar from 'lunar-calendar';
import * as iching from 'iching.js';
import * as d3 from 'd3';

/*
  Generated class for the ZhanbuPage page.

  See http://ionicframework.com/docs/v2/components/#navigation for more info on
  Ionic pages and navigation.
*/
@Component({
  selector: 'page-zhanbu-page',
  templateUrl: 'zhanbu-page.html'
})
export class ZhanbuPage {
  flip1: number;
  flip2: number;
  flip3: number;
  flip4: number;
  flip5: number;
  flip6: number;
  gua_infos: Array<{sizhu: string, gong: string, name: string, wuxing: string}>;

  constructor(public navCtrl: NavController, public navParams: NavParams) {
  }

  updateChanges(event) {
    if( typeof this.flip1 != 'undefined' && typeof this.flip2 != 'undefined' && typeof this.flip3 != 'undefined'
      && typeof this.flip4 != 'undefined' && typeof this.flip5 != 'undefined' && typeof this.flip6 != 'undefined') {
      var first_yao = iching.zheng2yinyang(this.flip1);
      var second_yao = iching.zheng2yinyang(this.flip2);
      var third_yao = iching.zheng2yinyang(this.flip3);
      var forth_yao = iching.zheng2yinyang(this.flip4);
      var fifth_yao = iching.zheng2yinyang(this.flip5);
      var sixth_yao = iching.zheng2yinyang(this.flip6);

      var upper_yao = iching.yinyang2trigram(forth_yao, fifth_yao, sixth_yao);
      var lower_yao = iching.yinyang2trigram(first_yao, second_yao, third_yao);

      var today = new Date();
      var day = today.getDate();
      var month = today.getMonth()+1; //January is 0!
      var year = today.getFullYear();
      var lunarInfo = lunarCalendar.solarToLunar(year, month, day);

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
      var svgContainer = d3.select('#zhanbu').append("svg")
                           .attr("width", 400)
                           .attr("height", 420);
      iching.drawTrigrams(svgContainer, upper_yao, lower_yao, lunarInfo.GanZhiDay.substring(0,1));
    }
  }

}
