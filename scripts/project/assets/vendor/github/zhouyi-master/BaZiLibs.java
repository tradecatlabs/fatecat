package com.liumulingyu.utils;


/**
 * @author 流木领域
 * 关注公众号：”流木领域“获取更多资料
 * 联系方式：wx:liumulingyu QQ:526100560
 * 周易根据阳历以24节气来计算四柱八字
 */
public class BaZiLibs {

    /**
     * 十天干
     */
    public static final String tianGanArray[]={"甲","乙","丙","丁","戊","己","庚","辛","壬","癸"};
    /**
     * 十天干五行关系
     */
    public static final String tianGanWuXingArray[]={"阳木","阴木","阳火","阴火","阳土","阴土","阳金","阴金","阳水","阴水"};
    /**
     * 十天干对应身体部位
     */
    public static final String tianGanShengTingArray[]={"头，胆","肩，肝","心，小肠","齿，舌心","鼻，胃","面，脾","筋，大肠","胸，肺","胫，膀胱","足，肾"};
    /**
     * 十二地支
     */
    public static final String diZhiArray[]={"子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"};

    /**
     * 十二地支五行关系
     */
    public static final String diZhiWuXingArray[]={"阳水,北方","阴土,中央","阳木,东方","阴木,东方","阳土,中央","阴火,南方","阳火,南方","阴土,中央","阳金,西方","阴金,西方","阳土,中央","阴水,北方"};

    /**
     * 月的地支排序
     */
    public static final String yueDiZhiArray[]={"寅","卯","辰","巳","午","未","申","酉","戌","亥","子","丑"};

    /**
     * 子-鼠，丑-牛，寅-虎，卯-兔，辰-龙，巳-蛇， 午-马，未-羊，申-猴，酉-鸡，戌-狗，亥-猪
     * 12生肖对应12地支
     */
    public static final String shengXiaoArray[]={"鼠","牛","虎","兔","龙","蛇","马","羊","猴","鸡","狗","猪"};
    /**
     * 获取60甲子数组
     * 规律为——阳干配阳支，阴干配阴支
     * @return
     * */
    public static final String[] jiaZiArray= {
            "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉",
            "甲戌", "乙亥", "丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未",
            "甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳",
            "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑", "壬寅", "癸卯",
            "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥", "壬子", "癸丑",
            "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥"
    };
    /**
     * 节气D值
     */
    private static final double D = 0.2422;
    /**
     * 20世纪的节气C值
     */
    private static final double[] C_20 = { 6.11, 20.84, 4.6295, 19.4599, 6.3826, 21.4155, 5.59, 20.888, 6.318, 21.86,
            6.5, 22.2, 7.928, 23.65, 8.35, 23.95, 8.44, 23.822, 9.098, 24.218, 8.218, 23.08, 7.9, 22.6 };

    /**
     * 21世纪的节气C值
     */
    private static final double[] C_21 = { 5.4055, 20.12, 3.87, 18.73, 5.63, 20.646, 4.81, 20.1, 5.52, 21.04, 5.678,
            21.37, 7.108, 22.83, 7.5, 23.13, 7.646, 23.042, 8.318, 23.438, 7.438, 22.36, 7.18, 21.94 };
    /**
     * 24节气
     */
    private static final String[] TERM = { "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑",
            "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至" };


    /**
     * 年数表（1950年—1999年）
     */
    private static final int[] Year19Table = { 31, 36, 42, 47, 52, 57, 3, 8, 13, 18, 24,
            29, 34, 39, 45, 50, 55, 0, 6, 11, 16, 21, 27, 32 ,37,42,48,53,58,3,9,14,19,24,30,35,40,45,51,56,1,6,12,17,22,27,33,38,43,48};

    /**
     *年数表（2000年-2049年）
     */
    private static final int[] Year20Table = {54,59,4,9,15,20,25,30,36,41,46,51,57,2,7,12,18,23,28,33,39,44,49,54,0,5,10,15,21,26,31,36,42,47,52,57,3,8,13,18,24,29,34,39,45,50,55,0,6,11};
    /**
     * 月数表（月数表万年通用，最好背熟）
     * 从下一年的1月开始的
     */
    private static final int[] MonthTable = {6,37,0,31,1,32,2,33,4,34,5,35};
    /**
     * 根据节气名称获取节气角标
     * @param name
     * @return
     */
    public static int getJiQiPositionByName(String name){
        for (int i = 0; i < TERM.length; i++) {
            if (TERM[i].equals(name)){
                return i;
            }
        }
        return -1;
    }

    /**
     * 计算公式：[Y*D+C]-L
     * 根据节气名称获取节气日期
     * @param year
     * @param name
     * @return
     */
    public static int getJiQiDayByName(int year,String name){
        int y=(year%100);
        if (year>=2000){
            return (int)(y*D+C_21[getJiQiPositionByName(name)]-((y-1)/4));
        }else{
            return (int)(y*D+C_20[getJiQiPositionByName(name)]-((y-1)/4));
        }
    }
    /**
     * 得到月的地支
     * @param year
     * @param month
     * @param day
     * @return
     */
    public static String getYueDiZhi(int year,int month,int day){
        //月的地支，首先判断处于那个月份，然后求得是在那个节气里面
          switch (month){
              case 1:
                  //计算day在小寒及其之后为丑月，之前为子月
                  int xiaoHanDay=getJiQiDayByName(year,"小寒");
                  if (day>=xiaoHanDay){
                      return "丑";
                  }
                  return "子";
              case 2:
                  //计算day在立春及其之后为寅月，之前为丑月
                  int liChunDay=getJiQiDayByName(year,"立春");
                  if (day>=liChunDay){
                      return "寅";
                  }
                  return "丑";
              case 3:
                  //计算day在惊蛰及其之后为卯月，之前为寅月
                  int jiZhenDay=getJiQiDayByName(year,"惊蛰");
                  if (day>=jiZhenDay){
                      return "卯";
                  }
                  return "寅";
              case 4:
                  //计算day在清明及其之后为辰月，之前为卯月
                  int qinMingDay=getJiQiDayByName(year,"清明");
                  if (day>=qinMingDay){
                      return "辰";
                  }
                  return "卯";
              case 5:
                  //计算day在立夏及其之后为巳月，之前为辰月
                  int liXiaDay=getJiQiDayByName(year,"立夏");
                  if (day>=liXiaDay){
                      return "巳";
                  }
                  return "辰";
              case 6:
                  //计算day在芒种及其之后为午月，之前为巳月
                  int mangZhongDay=getJiQiDayByName(year,"芒种");
                  if (day>=mangZhongDay){
                      return "午";
                  }
                  return "巳";
              case 7:
                  //计算day在小暑及其之后为未月，之前为午月
                  int xiaoShuDay=getJiQiDayByName(year,"小暑");
                  if (day>=xiaoShuDay){
                      return "未";
                  }
                  return "午";
              case 8:
                  //计算day在立秋及其之后为申月，之前为未月
                  int liQiuDay=getJiQiDayByName(year,"立秋");
                  if (day>=liQiuDay){
                      return "申";
                  }
                  return "未";
              case 9:
                  //计算day在白露及其之后为酉月，之前为申月
                  int baiLuDay=getJiQiDayByName(year,"白露");
                  if (day>=baiLuDay){
                      return "酉";
                  }
                  return "申";
              case 10:
                  //计算day在寒露及其之后为戌月，之前为酉月
                  int hanLuDay=getJiQiDayByName(year,"寒露");
                  if (day>=hanLuDay){
                      return "戌";
                  }
                  return "酉";
              case 11:
                  //计算day在立秋及其之后为亥月，之前为戌月
                  int liDongDay=getJiQiDayByName(year,"立秋");
                  if (day>=liDongDay){
                      return "亥";
                  }
                  return "戌";
              case 12:
                  //计算day在立秋及其之后为申月，之前为亥月
                  int daXueDay=getJiQiDayByName(year,"大雪");
                  if (day>=daXueDay){
                      return "子";
                  }
                  return "亥";
          }
          return null;
    }
    /**
     * 根据天干的名称获取年干的序列角标
     * @param text
     * @return
     */
    public static int getTianGanPositionByText(String text){
        for (int i = 0; i < tianGanArray.length; i++) {
            if (tianGanArray[i].equals(text)){
                return i;
            }
        }
        return -1;
    }

    /**
     * 根据地支的名称获取年干的序列角标
     * @param text
     * @return
     */
    public static int getDiZhiPositionByText(String text){
        for (int i = 0; i < diZhiArray.length; i++) {
            if (diZhiArray[i].equals(text)){
                return i;
            }
        }
        return -1;
    }
    /**
     * 根据月的地支的名称获取年干的序列角标
     * @param text
     * @return
     */
    public static int getYueDiZhiPositionByText(String text){
        for (int i = 0; i < yueDiZhiArray.length; i++) {
            if (yueDiZhiArray[i].equals(text)){
                return i;
            }
        }
        return -1;
    }

    /**
     * 获取日的干支
     * @param year
     * @param month
     * @param day
     * @return
     */
    public static String getDayGanZhi(int year,int month,int day){
        int yearNumber=0;
        if (month==1||month==2){
            yearNumber=-1;
        }
        if (year<2000){
            yearNumber=Year19Table[year%100-50-yearNumber];
        }else{
            yearNumber=Year20Table[year%100-yearNumber];
        }
       int dayPosition= yearNumber+MonthTable[month-1]+day;
        if (dayPosition>60){
            dayPosition=dayPosition-60;
        }
        return jiaZiArray[dayPosition-1];
    }

    /**
     * ①时支公式：时支=小时÷2-1（小时为偶数），时支=（小时+1）÷2-1（小时为奇数）
     * ②时干公式：时干=日干×2+时支（晨子=-1，夜子=11）
     * @param hour
     * @return
     */
    public static String getHourGanZhi(int dayTianGan,int hour){
        int hourDiZhiPosition;
        if (hour/2==0){
            hourDiZhiPosition=hour/2-1;
        }else{
            hourDiZhiPosition=(hour+1)/2-1;
        }
        hourDiZhiPosition=hourDiZhiPosition+1;
        String hourDiZhi;
        if (hourDiZhiPosition==12){
            hourDiZhi="子(夜)";
        }else if (hourDiZhiPosition==0){
            hourDiZhi="子(晨)";
        }else{
            hourDiZhi=diZhiArray[hourDiZhiPosition];
        }
        String hourTianGan=tianGanArray[((dayTianGan*2+hourDiZhiPosition-1)-1)%10];
        return hourTianGan+hourDiZhi;
    }
    /**
     * 以阳历的日期来算四柱八字
     * 比如：2020-10-11 14：00
     * @param year  年份
     * @param month 月份
     * @param day  日期
     * @param hour 小时
     * @return
     */
    public static String[] getYangLiBaZi(int year,int month,int day,int hour){
        int liCun=getJiQiDayByName(year,"立春");
        int yearPosition;
        if (month<2||month==2&&day<liCun){ //没有立春的话算上一年的
            yearPosition= (year-1-1864) % 60;
        }else{
            yearPosition=(year - 1864) % 60;
        }
        String yearGanZhiText=jiaZiArray[yearPosition];//此处求的年份的干支
        String monthDiZhi=getYueDiZhi(year,month,day);
        int monthDiZhiPosition=getYueDiZhiPositionByText(monthDiZhi);
        int monthGan=(getTianGanPositionByText(yearGanZhiText.substring(0,1))+1)*2+monthDiZhiPosition+1;
        if (monthGan>10){
            monthGan=monthGan%10-1;
        }else{
            monthGan=monthGan-1;
        }
        String monthGanZhiText= tianGanArray[monthGan]+monthDiZhi;//求得月的干支
        //日的干支
        String dayGanzhiText=getDayGanZhi(year,month,day);
        //时的干支
        String hourGanZhiText=getHourGanZhi(getTianGanPositionByText(dayGanzhiText.substring(0,1))-1,hour);
        return new String[]{yearGanZhiText,monthGanZhiText,dayGanzhiText,hourGanZhiText};
    }
    /**
     * 以阴历的日期来算四柱八字
     * @param year
     * @param month
     * @param day
     * @param hour
     * @return
     */
    public static String[] getYingLinBaZi(int year,int month,int day,int hour){
        return getYangLiBaZi(year,month,day,hour);
    }

    /**
     * 获取生肖
     * @param bazi
     * @return
     */
    public static String getShengXiao(String [] bazi){
        return bazi[0].substring(1,2)+shengXiaoArray[getDiZhiPositionByText( bazi[0].substring(1,2))];
    }

}
