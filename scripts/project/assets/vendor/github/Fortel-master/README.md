# Fortel
Java紫微斗數排盤Library (中州派)

Author: Eric Yu

-----------------------

## Samples

### 排盤

排盤：一九五二年十二月十五日早子時天盤，男性

```Java
Config destinyConfig = new Config(ConfigType.SKY, Sex.M, 1952, 12, 15, false, GroundTime.getByName("早子").get());

Destiny destiny = new Destiny(destinyConfig);

System.out.println(destiny.toJsonString());
```

JSON Output(Formatted):
```javascript
{
	"config": {
		"configType": "天盤",
		"sex": "男",
		"yearSky": 8,
		"yearGround": 4,
		"bornYear": 1952,
		"bornMonth": 12,
		"bornDay": 15,
		"bornTimeGround": 0,
		"isDoubleMonth": false
	},
	"shadowLight": "陽",
	"fiveElement": "木三局",
	"cells": [{
			"sky": 8,
			"ground": 0,
			"temples": ["兄弟"],
			"majorStars": ["貪狼"],
			"minorStars": ["擎羊"],
			"miniStars": ["天姚"],
			"preGeneralStar": "將星",
			"preAgeStar": "白虎",
			"preDoctorStar": "力士",
			"ageStart": 113,
			"ageEnd": 122,
			"persist12": "沐浴",
			"metadata": {}
		}, {
			"sky": 9,
			"ground": 1,
			"temples": ["身宮", "命宮"],
			"majorStars": ["天同", "巨門"],
			"minorStars": [],
			"miniStars": ["寡宿", "破碎"],
			"preGeneralStar": "攀鞍",
			"preAgeStar": "天德",
			"preDoctorStar": "青龍",
			"ageStart": 3,
			"ageEnd": 12,
			"persist12": "冠帶",
			"metadata": {}
		}, {
			"sky": 8,
			"ground": 2,
			"temples": ["父母"],
			"majorStars": ["武曲", "天相"],
			"minorStars": ["火星", "天馬"],
			"miniStars": ["天哭", "旬空", "截空", "封誥", "天月"],
			"preGeneralStar": "歲驛",
			"preAgeStar": "弔客",
			"preDoctorStar": "小耗",
			"ageStart": 13,
			"ageEnd": 22,
			"persist12": "臨官",
			"metadata": {}
		}, {
			"sky": 9,
			"ground": 3,
			"temples": ["福德"],
			"majorStars": ["太陽", "天梁"],
			"minorStars": ["天魁", "左輔"],
			"miniStars": ["旬空", "截空"],
			"preGeneralStar": "息神",
			"preAgeStar": "病符",
			"preDoctorStar": "將軍",
			"ageStart": 23,
			"ageEnd": 32,
			"persist12": "帝旺",
			"metadata": {}
		}, {
			"sky": 0,
			"ground": 4,
			"temples": ["田宅"],
			"majorStars": ["七殺"],
			"minorStars": ["文曲"],
			"miniStars": ["陰煞"],
			"preGeneralStar": "華蓋",
			"preAgeStar": "太歲",
			"preDoctorStar": "奏書",
			"ageStart": 33,
			"ageEnd": 42,
			"persist12": "衰",
			"metadata": {}
		}, {
			"sky": 1,
			"ground": 5,
			"temples": ["事業"],
			"majorStars": ["天機"],
			"minorStars": ["天鉞"],
			"miniStars": ["天喜", "孤辰", "劫煞", "天才", "天壽", "天空", "三台", "天貴"],
			"preGeneralStar": "劫煞",
			"preAgeStar": "晦氣",
			"preDoctorStar": "蜚廉",
			"ageStart": 43,
			"ageEnd": 52,
			"persist12": "病",
			"metadata": {}
		}, {
			"sky": 2,
			"ground": 6,
			"temples": ["交友"],
			"majorStars": ["紫微"],
			"minorStars": [],
			"miniStars": ["天福", "鳳閣", "解神", "台輔", "解神", "蜚廉", "天傷"],
			"preGeneralStar": "災煞",
			"preAgeStar": "喪門",
			"preDoctorStar": "喜神",
			"ageStart": 53,
			"ageEnd": 62,
			"persist12": "死",
			"metadata": {}
		}, {
			"sky": 3,
			"ground": 7,
			"temples": ["遷移"],
			"majorStars": [],
			"minorStars": [],
			"miniStars": [],
			"preGeneralStar": "天煞",
			"preAgeStar": "貫索",
			"preDoctorStar": "病符",
			"ageStart": 63,
			"ageEnd": 72,
			"persist12": "墓",
			"metadata": {}
		}, {
			"sky": 4,
			"ground": 8,
			"temples": ["疾厄"],
			"majorStars": ["破軍"],
			"minorStars": [],
			"miniStars": ["龍池", "天刑", "天使"],
			"preGeneralStar": "指背",
			"preAgeStar": "官符",
			"preDoctorStar": "大耗",
			"ageStart": 73,
			"ageEnd": 82,
			"persist12": "絕",
			"metadata": {}
		}, {
			"sky": 5,
			"ground": 9,
			"temples": ["財帛"],
			"majorStars": [],
			"minorStars": [],
			"miniStars": ["天廚", "咸池", "月德", "八座"],
			"preGeneralStar": "咸池",
			"preAgeStar": "小耗",
			"preDoctorStar": "伏兵",
			"ageStart": 83,
			"ageEnd": 92,
			"persist12": "胎",
			"metadata": {}
		}, {
			"sky": 6,
			"ground": 10,
			"temples": ["子女"],
			"majorStars": ["廉貞", "天府"],
			"minorStars": ["鈴星", "陀羅", "文昌"],
			"miniStars": ["天官", "天虛"],
			"preGeneralStar": "月煞",
			"preAgeStar": "歲破",
			"preDoctorStar": "官府",
			"ageStart": 93,
			"ageEnd": 102,
			"persist12": "養",
			"metadata": {}
		}, {
			"sky": 7,
			"ground": 11,
			"temples": ["夫妻"],
			"majorStars": ["太陰"],
			"minorStars": ["地空", "地劫", "祿存", "右弼"],
			"miniStars": ["紅鸞", "大耗", "天巫", "恩光"],
			"preGeneralStar": "亡神",
			"preAgeStar": "龍德",
			"preDoctorStar": "博士",
			"ageStart": 103,
			"ageEnd": 112,
			"persist12": "長生",
			"metadata": {}
		}
	],
	"starReactionMap": {
		"科": "天府",
		"權": "紫微",
		"忌": "武曲",
		"祿": "天梁"
	},
	"majorStarEnergy": {
		"貪狼": 1,
		"天同": -1,
		"天機": 0,
		"太陽": 2,
		"廉貞": 1,
		"武曲": 0,
		"破軍": -1,
		"天府": 2,
		"天梁": 2,
		"紫微": 2,
		"太陰": 2,
		"巨門": 1,
		"天相": 2,
		"七殺": 1
	},
	"destinyMaster": "廉貞",
	"bodyMaster": "文昌",
	"sonDou": 1
}
```

-----------------------

### 檢查宮垣

排盤：一九九零年三月十一日午時地盤，男性

檢查命盤命宮是否: 會見廉貞, 並且同時"天魁或天鉞同宮"或"不見化忌"

```Java
Config destinyConfig = new Config(ConfigType.GROUND, Sex.M, 1990, 3, 11, false, GroundTime.getByName("午").get());
Destiny destiny = new Destiny(destinyConfig);

/*
* 檢查命盤命宮是否: 會見廉貞, 並且同時"天魁或天鉞同宮"或"不見化忌"
*/
boolean result = new DestinyCellCriteria(destiny, Temple.TEMPLE_DESTINY) //命宮
    .and()
        .meetStars(MajorStar.MAJOR_STAR_HONEST) //廉貞
        .or()
            .sameCellSomeStars(MinorStar.MINOR_STAR_HONOR, MinorStar.MINOR_STAR_HONOR2) //天魁或天鉞同宮
            .notMeetStars(StarReaction.STAR_TO_PROBLEM) //不見化忌
        .endOr()
    .endAnd()
    .getResult();

System.out.println(result);
```

Output:
```
false
```

-----------------------

檢查命盤命宮是否: 會見廉貞, 並且同時"天魁或天鉞同宮"或"不見化忌"

```Java
/*
* 檢查命盤命宮是否: 會見貪狼, 並且同時"文曲及龍池同宮"或"宮位在戌"
*/
boolean result = new DestinyCellCriteria(destiny, Temple.TEMPLE_DESTINY) //命宮
    .and()
        .meetStars(MajorStar.MAJOR_STAR_GREED) //貪狼
        .or()
            .sameCellStars(MinorStar.MINOR_STAR_SKILL, MiniStar.MINI_STAR_DRAGON_SKILL) //文曲及龍池同宮
            .isCellGrounds(Ground.getByDisplayName("戌").get()) //宮位在戌
        .endOr()
    .endAnd()
    .getResult();

System.out.println(result);
```

Output:
```
true
```

-----------------------

JavaDoc:

You can view the Javadoc page at "\fortelcore\javadoc\index.html"

