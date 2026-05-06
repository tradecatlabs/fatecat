package com.airic.fortel.core.model;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

import com.airic.fortel.core.model.Data.Direction;
import com.airic.fortel.core.model.Data.Sex;
import com.airic.fortel.core.model.Data.ShadowLight;
import com.airic.fortel.core.util.CommonUtil;
import com.airic.fortel.core.util.Const;
import com.fasterxml.jackson.annotation.JsonValue;

/**
 * The Enum MiniStar.
 *
 * @author Eric Yu
 */
public enum MiniStar implements Star {
	// 天官
	/** The mini star sky noble. */
	MINI_STAR_SKY_NOBLE(Const.MINI_STAR_SKY_NOBLE) {
		public Ground getGround(Destiny destiny) {
			Sky yearSky = destiny.getConfig().getYearSky();
			return Ground.getByDisplayName(
					new String[] { Const.GROUND_7, Const.GROUND_4, Const.GROUND_5, Const.GROUND_2, Const.GROUND_3,
							Const.GROUND_9, Const.GROUND_11, Const.GROUND_9, Const.GROUND_10, Const.GROUND_6 }[yearSky
									.getIndex()])
					.get();
		}
	},
	// 天福
	/** The mini star sky happiness. */
	MINI_STAR_SKY_HAPPINESS(Const.MINI_STAR_SKY_HAPPINESS) {
		public Ground getGround(Destiny destiny) {
			Sky yearSky = destiny.getConfig().getYearSky();
			return Ground.getByDisplayName(
					new String[] { Const.GROUND_9, Const.GROUND_8, Const.GROUND_0, Const.GROUND_11, Const.GROUND_3,
							Const.GROUND_2, Const.GROUND_6, Const.GROUND_5, Const.GROUND_6, Const.GROUND_5 }[yearSky
									.getIndex()])
					.get();
		}
	},
	// 天廚
	/** The mini star sky cook. */
	MINI_STAR_SKY_COOK(Const.MINI_STAR_SKY_COOK) {
		public Ground getGround(Destiny destiny) {
			Sky yearSky = destiny.getConfig().getYearSky();
			return Ground.getByDisplayName(
					new String[] { Const.GROUND_5, Const.GROUND_6, Const.GROUND_0, Const.GROUND_5, Const.GROUND_6,
							Const.GROUND_8, Const.GROUND_2, Const.GROUND_6, Const.GROUND_9, Const.GROUND_11 }[yearSky
									.getIndex()])
					.get();
		}
	},
	// 天哭
	/** The mini star sky cry. */
	MINI_STAR_SKY_CRY(Const.MINI_STAR_SKY_CRY) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(Const.GROUND_6).get().shift(-yearGround.getIndex());
		}
	},
	// 天虛
	/** The mini star sky lost. */
	MINI_STAR_SKY_LOST(Const.MINI_STAR_SKY_LOST) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(Const.GROUND_6).get().shift(yearGround.getIndex());
		}
	},
	// 龍池
	/** The mini star dragon skill. */
	MINI_STAR_DRAGON_SKILL(Const.MINI_STAR_DRAGON_SKILL) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(Const.GROUND_4).get().shift(yearGround.getIndex());
		}
	},
	// 鳳閣
	/** The mini star phoenix art. */
	MINI_STAR_PHOENIX_ART(Const.MINI_STAR_PHOENIX_ART) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(Const.GROUND_10).get().shift(-yearGround.getIndex());
		}
	},
	// 紅鸞
	/** The mini star red marriage. */
	MINI_STAR_RED_MARRIAGE(Const.MINI_STAR_RED_MARRIAGE) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(Const.GROUND_3).get().shift(-yearGround.getIndex());
		}
	},
	// 天喜
	/** The mini star sky joy reproduction. */
	MINI_STAR_SKY_JOY_REPRODUCTION(Const.MINI_STAR_SKY_JOY_REPRODUCTION) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(Const.GROUND_9).get().shift(-yearGround.getIndex());
		}
	},
	// 孤辰
	/** The mini star independent. */
	MINI_STAR_INDEPENDENT(Const.MINI_STAR_INDEPENDENT) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(new String[] { Const.GROUND_2, Const.GROUND_2, Const.GROUND_5,
					Const.GROUND_5, Const.GROUND_5, Const.GROUND_8, Const.GROUND_8, Const.GROUND_8, Const.GROUND_11,
					Const.GROUND_11, Const.GROUND_11, Const.GROUND_2 }[yearGround.getIndex()]).get();
		}
	},
	// 寡宿
	/** The mini star single. */
	MINI_STAR_SINGLE(Const.MINI_STAR_SINGLE) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(new String[] { Const.GROUND_10, Const.GROUND_10, Const.GROUND_1,
					Const.GROUND_1, Const.GROUND_1, Const.GROUND_4, Const.GROUND_4, Const.GROUND_4, Const.GROUND_7,
					Const.GROUND_7, Const.GROUND_7, Const.GROUND_10 }[yearGround.getIndex()]).get();
		}
	},
	// 解神
	/** The mini star resolve. */
	MINI_STAR_RESOLVE(Const.MINI_STAR_RESOLVE) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(Const.GROUND_10).get().shift(-yearGround.getIndex());
		}
	},
	// 破碎
	/** The mini star broken. */
	MINI_STAR_BROKEN(Const.MINI_STAR_BROKEN) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(new String[] { Const.GROUND_5, Const.GROUND_1, Const.GROUND_9,
					Const.GROUND_5, Const.GROUND_1, Const.GROUND_9, Const.GROUND_5, Const.GROUND_1, Const.GROUND_9,
					Const.GROUND_5, Const.GROUND_1, Const.GROUND_9 }[yearGround.getIndex()]).get();
		}
	},
	// 大耗
	/** The mini star big lost. */
	MINI_STAR_BIG_LOST(Const.MINI_STAR_BIG_LOST) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(new String[] { Const.GROUND_7, Const.GROUND_6, Const.GROUND_9,
					Const.GROUND_8, Const.GROUND_11, Const.GROUND_10, Const.GROUND_1, Const.GROUND_0, Const.GROUND_3,
					Const.GROUND_2, Const.GROUND_5, Const.GROUND_4 }[yearGround.getIndex()]).get();
		}
	},
	// 劫煞
	/** The mini star little disaster. */
	MINI_STAR_LITTLE_DISASTER(Const.MINI_STAR_LITTLE_DISASTER) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(new String[] { Const.GROUND_5, Const.GROUND_2, Const.GROUND_11,
					Const.GROUND_8, Const.GROUND_5, Const.GROUND_2, Const.GROUND_11, Const.GROUND_8, Const.GROUND_5,
					Const.GROUND_2, Const.GROUND_11, Const.GROUND_8 }[yearGround.getIndex()]).get();
		}
	},
	// 咸池
	/** The mini star bad romance. */
	MINI_STAR_BAD_ROMANCE(Const.MINI_STAR_BAD_ROMANCE) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(new String[] { Const.GROUND_9, Const.GROUND_6, Const.GROUND_3,
					Const.GROUND_0, Const.GROUND_9, Const.GROUND_6, Const.GROUND_3, Const.GROUND_0, Const.GROUND_9,
					Const.GROUND_6, Const.GROUND_3, Const.GROUND_0 }[yearGround.getIndex()]).get();
		}
	},
	// 月德
	/** The mini star moon ethic. */
	MINI_STAR_MOON_ETHIC(Const.MINI_STAR_MOON_ETHIC) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(Const.GROUND_5).get().shift(yearGround.getIndex());
		}
	},
	// 天才
	/** The mini star genius. */
	MINI_STAR_GENIUS(Const.MINI_STAR_GENIUS) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return destiny.getTempleCell(Temple.TEMPLE_DESTINY).getNextICell(yearGround.getIndex()).get().getGround();
		}
	},
	// 天壽
	/** The mini star long life. */
	MINI_STAR_LONG_LIFE(Const.MINI_STAR_LONG_LIFE) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return destiny.getTempleCell(Temple.TEMPLE_BODY).getNextICell(yearGround.getIndex()).get().getGround();
		}
	},
	// 天空
	/** The mini star empty sky. */
	MINI_STAR_EMPTY_SKY(Const.MINI_STAR_EMPTY_SKY) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(new String[] { Const.GROUND_1, Const.GROUND_2, Const.GROUND_3,
					Const.GROUND_4, Const.GROUND_5, Const.GROUND_6, Const.GROUND_7, Const.GROUND_8, Const.GROUND_9,
					Const.GROUND_10, Const.GROUND_11, Const.GROUND_0 }[yearGround.getIndex()]).get();
		}
	},
	// 旬空
	/** The mini star lazy sky. */
	MINI_STAR_LAZY_SKY(Const.MINI_STAR_LAZY_SKY) {
		public Ground getGround(Destiny destiny) {
			Sky yearSky = destiny.getConfig().getYearSky();
			Ground yearGround = destiny.getConfig().getYearGround();
			
			int offset = CommonUtil.mod(yearSky.getIndex() - yearGround.getIndex(), 12)/2;
			return Ground.getByIndex(10 - 2 * offset);
		}
	},
	// 旬空2
	/** The MIN i_ sta r_ laz y_ sk y2. */
	MINI_STAR_LAZY_SKY2(Const.MINI_STAR_LAZY_SKY2, Const.MINI_STAR_LAZY_SKY) {
		public Ground getGround(Destiny destiny) {
			Sky yearSky = destiny.getConfig().getYearSky();
			Ground yearGround = destiny.getConfig().getYearGround();

			int offset = CommonUtil.mod(yearSky.getIndex() - yearGround.getIndex(), 12)/2;
			return Ground.getByIndex(10 - 2 * offset + 1);			
		}
	},
	// 截空
	/** The mini star interrupt sky. */
	MINI_STAR_INTERRUPT_SKY(Const.MINI_STAR_INTERRUPT_SKY) {
		public Ground getGround(Destiny destiny) {
			Sky yearSky = destiny.getConfig().getYearSky();
			if (yearSky.getIndex() % 2 == 0) {
				return Ground.getByIndex(8 - yearSky.getIndex() * 2 % 10);
			} else {
				return Ground.getByIndex(8 - yearSky.getIndex() * 2 % 10 + 1);
			}
		}
	},
	// 截空2
	/** The MIN i_ sta r_ interrup t_ sk y2. */
	MINI_STAR_INTERRUPT_SKY2(Const.MINI_STAR_INTERRUPT_SKY2, Const.MINI_STAR_INTERRUPT_SKY) {
		public Ground getGround(Destiny destiny) {
			Sky yearSky = destiny.getConfig().getYearSky();
			if (yearSky.getIndex() % 2 == 0) {
				return Ground.getByIndex(8 - yearSky.getIndex() * 2 % 10 + 1);
			} else {
				return Ground.getByIndex(8 - yearSky.getIndex() * 2 % 10);
			}
		}
	},
	// 台輔
	/** The mini star platform support. */
	MINI_STAR_PLATFORM_SUPPORT(Const.MINI_STAR_PLATFORM_SUPPORT) {
		public Ground getGround(Destiny destiny) {
			Ground bornGround = destiny.getConfig().getBornTimeGround().getGround();
			return Ground.getByDisplayName(Const.GROUND_6).get().shift(bornGround.getIndex());
		}
	},
	// 封誥
	/** The mini star reward. */
	MINI_STAR_REWARD(Const.MINI_STAR_REWARD) {
		public Ground getGround(Destiny destiny) {
			Ground bornGround = destiny.getConfig().getBornTimeGround().getGround();
			return Ground.getByDisplayName(Const.GROUND_2).get().shift(bornGround.getIndex());
		}
	},
	// 天刑
	/** The mini star sky punishment. */
	MINI_STAR_SKY_PUNISHMENT(Const.MINI_STAR_SKY_PUNISHMENT) {
		public Ground getGround(Destiny destiny) {
			int month = destiny.getConfig().getDoubleMonthLogicalMonth();
			return Ground.getByDisplayName(Const.GROUND_9).get().shift(month - 1);
		}
	},
	// 天姚
	/** The mini star sky romantic. */
	MINI_STAR_SKY_ROMANTIC(Const.MINI_STAR_SKY_ROMANTIC) {
		public Ground getGround(Destiny destiny) {
			int month = destiny.getConfig().getDoubleMonthLogicalMonth();
			return Ground.getByDisplayName(Const.GROUND_1).get().shift(month - 1);
		}
	},
	// 天巫
	/** The mini star sky witch. */
	MINI_STAR_SKY_WITCH(Const.MINI_STAR_SKY_WITCH) {
		public Ground getGround(Destiny destiny) {
			int month = destiny.getConfig().getDoubleMonthLogicalMonth();
			// return Ground.getByName(new String[] { Const.GROUND_5,
			// Const.GROUND_8, Const.GROUND_11, Const.GROUND_2, Const.GROUND_5,
			// Const.GROUND_8, Const.GROUND_11, Const.GROUND_2, Const.GROUND_5,
			// Const.GROUND_8, Const.GROUND_11, Const.GROUND_2 }[month-1]);
			return Ground.getByDisplayName(new String[] { Const.GROUND_5, Const.GROUND_8, Const.GROUND_2,
					Const.GROUND_11, Const.GROUND_5, Const.GROUND_8, Const.GROUND_2, Const.GROUND_11, Const.GROUND_5,
					Const.GROUND_8, Const.GROUND_2, Const.GROUND_11 }[month - 1]).get();
		}
	},
	// 天月
	/** The mini star sky moon. */
	MINI_STAR_SKY_MOON(Const.MINI_STAR_SKY_MOON) {
		public Ground getGround(Destiny destiny) {
			int month = destiny.getConfig().getDoubleMonthLogicalMonth();
			return Ground.getByDisplayName(new String[] { Const.GROUND_10, Const.GROUND_5, Const.GROUND_4,
					Const.GROUND_2, Const.GROUND_7, Const.GROUND_3, Const.GROUND_11, Const.GROUND_7, Const.GROUND_2,
					Const.GROUND_6, Const.GROUND_10, Const.GROUND_2 }[month - 1]).get();
		}
	},
	// 陰煞
	/** The mini star ghost. */
	MINI_STAR_GHOST(Const.MINI_STAR_GHOST) {
		public Ground getGround(Destiny destiny) {
			int month = destiny.getConfig().getDoubleMonthLogicalMonth();
			return Ground.getByDisplayName(new String[] { Const.GROUND_2, Const.GROUND_0, Const.GROUND_10,
					Const.GROUND_8, Const.GROUND_6, Const.GROUND_4, Const.GROUND_2, Const.GROUND_0, Const.GROUND_10,
					Const.GROUND_8, Const.GROUND_6, Const.GROUND_4 }[month - 1]).get();
		}
	},
	// 解神2
	/** The MIN i_ sta r_ resolv e2. */
	MINI_STAR_RESOLVE2(Const.MINI_STAR_RESOLVE2, Const.MINI_STAR_RESOLVE) {
		public Ground getGround(Destiny destiny) {
			int month = destiny.getConfig().getDoubleMonthLogicalMonth();
			return Ground.getByDisplayName(new String[] { Const.GROUND_8, Const.GROUND_8, Const.GROUND_10,
					Const.GROUND_10, Const.GROUND_0, Const.GROUND_0, Const.GROUND_2, Const.GROUND_2, Const.GROUND_4,
					Const.GROUND_4, Const.GROUND_6, Const.GROUND_6 }[month - 1]).get();
		}
	},
	// 子丑寅年在申酉戍, 卯辰巳年在巳午未, 午未申年在寅卯辰, 酉戍亥年在亥子丑
	// 蜚廉2
	/** The MIN i_ sta r_ wron g_ mout h2. */
	MINI_STAR_WRONG_MOUTH2(Const.MINI_STAR_WRONG_MOUTH2, Const.MINI_STAR_WRONG_MOUTH) {
		public Ground getGround(Destiny destiny) {
			int yearSkyGroundIndex = destiny.getConfig().getYearGround().getIndex();
			if (yearSkyGroundIndex / 3 == 0) {// 子丑寅
				return Ground.getByIndex(8 + yearSkyGroundIndex % 3);
			} else if (yearSkyGroundIndex / 3 == 1) {// 卯辰巳
				return Ground.getByIndex(5 + yearSkyGroundIndex % 3);
			} else if (yearSkyGroundIndex / 3 == 2) {// 午未申
				return Ground.getByIndex(2 + yearSkyGroundIndex % 3);
			} else if (yearSkyGroundIndex / 3 == 3) {// 酉戍亥
				return Ground.getByIndex(11 + yearSkyGroundIndex % 3);
			}
			return Ground.getByDisplayName(Const.GROUND_8).get().shift(destiny.getConfig().getYearGround().getIndex());
		}
	},
	// 博士
	/** The mini star doctor. */
	MINI_STAR_DOCTOR(Const.MINI_STAR_DOCTOR) {
		public Ground getGround(Destiny destiny) {
			return MinorStar.MINOR_STAR_CLOTH.getGround(destiny);
		}
	},
	// 力士
	/** The mini star strength. */
	MINI_STAR_STRENGTH(Const.MINI_STAR_STRENGTH) {
		public Ground getGround(Destiny destiny) {
			// 陽男陰女順行
			int vector = destiny.getShadowLight() == ShadowLight.LIGHT ? 1 : -1;
			vector *= destiny.getConfig().getSex() == Sex.M ? 1 : -1;
			Direction direction = vector == 1 ? Direction.CLOCKWISE : Direction.ANTICLOCKWISE;
			return MinorStar.MINOR_STAR_CLOTH.getGround(destiny).shift(direction.getNumber());
		}
	},
	// 青龍
	/** The mini star green dragon. */
	MINI_STAR_GREEN_DRAGON(Const.MINI_STAR_GREEN_DRAGON) {
		public Ground getGround(Destiny destiny) {
			// 陽男陰女順行
			int vector = destiny.getShadowLight() == ShadowLight.LIGHT ? 1 : -1;
			vector *= destiny.getConfig().getSex() == Sex.M ? 1 : -1;
			Direction direction = vector == 1 ? Direction.CLOCKWISE : Direction.ANTICLOCKWISE;
			return MinorStar.MINOR_STAR_CLOTH.getGround(destiny).shift(direction.getNumber() * 2);
		}
	},
	// 小耗
	/** The mini star small lost. */
	MINI_STAR_SMALL_LOST(Const.MINI_STAR_SMALL_LOST) {
		public Ground getGround(Destiny destiny) {
			// 陽男陰女順行
			int vector = destiny.getShadowLight() == ShadowLight.LIGHT ? 1 : -1;
			vector *= destiny.getConfig().getSex() == Sex.M ? 1 : -1;
			Direction direction = vector == 1 ? Direction.CLOCKWISE : Direction.ANTICLOCKWISE;
			return MinorStar.MINOR_STAR_CLOTH.getGround(destiny).shift(direction.getNumber() * 3);
		}
	},
	// 將軍
	/** The mini star general. */
	MINI_STAR_GENERAL(Const.MINI_STAR_GENERAL) {
		public Ground getGround(Destiny destiny) {
			// 陽男陰女順行
			int vector = destiny.getShadowLight() == ShadowLight.LIGHT ? 1 : -1;
			vector *= destiny.getConfig().getSex() == Sex.M ? 1 : -1;
			Direction direction = vector == 1 ? Direction.CLOCKWISE : Direction.ANTICLOCKWISE;
			return MinorStar.MINOR_STAR_CLOTH.getGround(destiny).shift(direction.getNumber() * 4);
		}
	},
	// 奏書
	/** The mini star letter to king. */
	MINI_STAR_LETTER_TO_KING(Const.MINI_STAR_LETTER_TO_KING) {
		public Ground getGround(Destiny destiny) {
			// 陽男陰女順行
			int vector = destiny.getShadowLight() == ShadowLight.LIGHT ? 1 : -1;
			vector *= destiny.getConfig().getSex() == Sex.M ? 1 : -1;
			Direction direction = vector == 1 ? Direction.CLOCKWISE : Direction.ANTICLOCKWISE;
			return MinorStar.MINOR_STAR_CLOTH.getGround(destiny).shift(direction.getNumber() * 5);
		}
	},
	// 蜚廉
	/** The mini star wrong mouth. */
	MINI_STAR_WRONG_MOUTH(Const.MINI_STAR_WRONG_MOUTH) {
		public Ground getGround(Destiny destiny) {
			// 陽男陰女順行
			int vector = destiny.getShadowLight() == ShadowLight.LIGHT ? 1 : -1;
			vector *= destiny.getConfig().getSex() == Sex.M ? 1 : -1;
			Direction direction = vector == 1 ? Direction.CLOCKWISE : Direction.ANTICLOCKWISE;
			return MinorStar.MINOR_STAR_CLOTH.getGround(destiny).shift(direction.getNumber() * 6);
		}
	},
	// 喜神
	/** The mini star joy god. */
	MINI_STAR_JOY_GOD(Const.MINI_STAR_JOY_GOD) {
		public Ground getGround(Destiny destiny) {
			// 陽男陰女順行
			int vector = destiny.getShadowLight() == ShadowLight.LIGHT ? 1 : -1;
			vector *= destiny.getConfig().getSex() == Sex.M ? 1 : -1;
			Direction direction = vector == 1 ? Direction.CLOCKWISE : Direction.ANTICLOCKWISE;
			return MinorStar.MINOR_STAR_CLOTH.getGround(destiny).shift(direction.getNumber() * 7);
		}
	},
	// 病符
	/** The mini star sick ticket. */
	MINI_STAR_SICK_TICKET(Const.MINI_STAR_SICK_TICKET) {
		public Ground getGround(Destiny destiny) {
			// 陽男陰女順行
			int vector = destiny.getShadowLight() == ShadowLight.LIGHT ? 1 : -1;
			vector *= destiny.getConfig().getSex() == Sex.M ? 1 : -1;
			Direction direction = vector == 1 ? Direction.CLOCKWISE : Direction.ANTICLOCKWISE;
			return MinorStar.MINOR_STAR_CLOTH.getGround(destiny).shift(direction.getNumber() * 8);
		}
	},
	// 大耗2
	/** The MIN i_ sta r_ bi g_ los t2. */
	MINI_STAR_BIG_LOST2(Const.MINI_STAR_BIG_LOST2, Const.MINI_STAR_BIG_LOST) {
		public Ground getGround(Destiny destiny) {
			// 陽男陰女順行
			int vector = destiny.getShadowLight() == ShadowLight.LIGHT ? 1 : -1;
			vector *= destiny.getConfig().getSex() == Sex.M ? 1 : -1;
			Direction direction = vector == 1 ? Direction.CLOCKWISE : Direction.ANTICLOCKWISE;
			return MinorStar.MINOR_STAR_CLOTH.getGround(destiny).shift(direction.getNumber() * 9);
		}
	},
	// 伏兵
	/** The mini star army trap. */
	MINI_STAR_ARMY_TRAP(Const.MINI_STAR_ARMY_TRAP) {
		public Ground getGround(Destiny destiny) {
			// 陽男陰女順行
			int vector = destiny.getShadowLight() == ShadowLight.LIGHT ? 1 : -1;
			vector *= destiny.getConfig().getSex() == Sex.M ? 1 : -1;
			Direction direction = vector == 1 ? Direction.CLOCKWISE : Direction.ANTICLOCKWISE;
			return MinorStar.MINOR_STAR_CLOTH.getGround(destiny).shift(direction.getNumber() * 10);
		}
	},
	// 官府
	/** The mini star government. */
	MINI_STAR_GOVERNMENT(Const.MINI_STAR_GOVERNMENT) {
		public Ground getGround(Destiny destiny) {
			// 陽男陰女順行
			int vector = destiny.getShadowLight() == ShadowLight.LIGHT ? 1 : -1;
			vector *= destiny.getConfig().getSex() == Sex.M ? 1 : -1;
			Direction direction = vector == 1 ? Direction.CLOCKWISE : Direction.ANTICLOCKWISE;
			return MinorStar.MINOR_STAR_CLOTH.getGround(destiny).shift(direction.getNumber() * 11);
		}
	},
	// 三台
	/** The mini star three table. */
	MINI_STAR_THREE_TABLE(Const.MINI_STAR_THREE_TABLE) {
		public Ground getGround(Destiny destiny) {
			int bornDay = destiny.getConfig().getBornDay();
			return destiny.getGroundCell(MinorStar.MINOR_STAR_LEFT_SUPPORT.getGround(destiny)).getNextICell(bornDay - 1)
					.get().getGround();
		}
	},
	// 八座
	/** The mini star eight seat. */
	MINI_STAR_EIGHT_SEAT(Const.MINI_STAR_EIGHT_SEAT) {
		public Ground getGround(Destiny destiny) {
			int bornDay = destiny.getConfig().getBornDay();
			return destiny.getGroundCell(MinorStar.MINOR_STAR_RIGHT_SUPPORT.getGround(destiny))
					.getPrevICell(bornDay - 1).get().getGround();
		}
	},
	// 恩光
	/** The mini star holy light. */
	MINI_STAR_HOLY_LIGHT(Const.MINI_STAR_HOLY_LIGHT) {
		public Ground getGround(Destiny destiny) {
			int bornDay = destiny.getConfig().getBornDay();
			return destiny.getGroundCell(MinorStar.MINOR_STAR_CLEVER.getGround(destiny)).getNextICell(bornDay - 2).get()
					.getGround();
		}
	},
	// 天貴
	/** The mini star sky precious. */
	MINI_STAR_SKY_PRECIOUS(Const.MINI_STAR_SKY_PRECIOUS) {
		public Ground getGround(Destiny destiny) {
			int bornDay = destiny.getConfig().getBornDay();
			return destiny.getGroundCell(MinorStar.MINOR_STAR_SKILL.getGround(destiny)).getNextICell(bornDay - 2).get()
					.getGround();
		}
	},
	// 太歲
	/** The mini star year god. */
	MINI_STAR_YEAR_GOD(Const.MINI_STAR_YEAR_GOD) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(Const.GROUND_0).get().shift(yearGround.getIndex());
		}
	},
	// 晦氣
	/** The mini star negative mindset. */
	MINI_STAR_NEGATIVE_MINDSET(Const.MINI_STAR_NEGATIVE_MINDSET) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(Const.GROUND_1).get().shift(yearGround.getIndex());
		}
	},
	// 喪門
	/** The mini star lost door. */
	MINI_STAR_LOST_DOOR(Const.MINI_STAR_LOST_DOOR) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(Const.GROUND_2).get().shift(yearGround.getIndex());
		}
	},
	// 貫索
	/** The mini star penetration. */
	MINI_STAR_PENETRATION(Const.MINI_STAR_PENETRATION) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(Const.GROUND_3).get().shift(yearGround.getIndex());
		}
	},
	// 官符
	/** The mini star government ticket. */
	MINI_STAR_GOVERNMENT_TICKET(Const.MINI_STAR_GOVERNMENT_TICKET) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(Const.GROUND_4).get().shift(yearGround.getIndex());
		}
	},
	// 小耗2
	/** The MIN i_ sta r_ smal l_ los t2. */
	MINI_STAR_SMALL_LOST2(Const.MINI_STAR_SMALL_LOST2, Const.MINI_STAR_SMALL_LOST) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(Const.GROUND_5).get().shift(yearGround.getIndex());
		}
	},
	// 歲破
	/** The mini star age broken. */
	MINI_STAR_AGE_BROKEN(Const.MINI_STAR_AGE_BROKEN) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(Const.GROUND_6).get().shift(yearGround.getIndex());
		}
	},
	// 龍德
	/** The mini star dragon ethic. */
	MINI_STAR_DRAGON_ETHIC(Const.MINI_STAR_DRAGON_ETHIC) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(Const.GROUND_7).get().shift(yearGround.getIndex());
		}
	},
	// 白虎
	/** The mini star white tiger. */
	MINI_STAR_WHITE_TIGER(Const.MINI_STAR_WHITE_TIGER) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(Const.GROUND_8).get().shift(yearGround.getIndex());
		}
	},
	// 天德
	/** The mini star father gift. */
	MINI_STAR_FATHER_GIFT(Const.MINI_STAR_FATHER_GIFT) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(Const.GROUND_9).get().shift(yearGround.getIndex());
		}
	},
	// 弔客
	/** The mini star parent die. */
	MINI_STAR_PARENT_DIE(Const.MINI_STAR_PARENT_DIE) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(Const.GROUND_10).get().shift(yearGround.getIndex());
		}
	},
	// 病符2
	/** The MIN i_ sta r_ sic k_ ticke t2. */
	MINI_STAR_SICK_TICKET2(Const.MINI_STAR_SICK_TICKET2, Const.MINI_STAR_SICK_TICKET) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(Const.GROUND_11).get().shift(yearGround.getIndex());
		}
	},
	// 天使
	/** The mini star angel. */
	MINI_STAR_ANGEL(Const.MINI_STAR_ANGEL) {
		public Ground getGround(Destiny destiny) {
			int vector = destiny.getShadowLight() == ShadowLight.LIGHT ? 1 : -1;
			vector *= destiny.getConfig().getSex() == Sex.M ? 1 : -1;
			if (vector == 1) {
				return destiny.getTempleCell(Temple.TEMPLE_SICK).getGround();
			} else {
				return destiny.getTempleCell(Temple.TEMPLE_FRIEND).getGround();
			}
		}
	},
	// 天傷
	/** The mini star sky hurt. */
	MINI_STAR_SKY_HURT(Const.MINI_STAR_SKY_HURT) {
		public Ground getGround(Destiny destiny) {
			int vector = destiny.getShadowLight() == ShadowLight.LIGHT ? 1 : -1;
			vector *= destiny.getConfig().getSex() == Sex.M ? 1 : -1;
			if (vector == 1) {
				return destiny.getTempleCell(Temple.TEMPLE_FRIEND).getGround();
			} else {
				return destiny.getTempleCell(Temple.TEMPLE_SICK).getGround();
			}
		}
	},
	// 將星
	/** The mini star general star. */
	MINI_STAR_GENERAL_STAR(Const.MINI_STAR_GENERAL_STAR) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(new String[] { Const.GROUND_0, Const.GROUND_9, Const.GROUND_6,
					Const.GROUND_3, Const.GROUND_0, Const.GROUND_9, Const.GROUND_6, Const.GROUND_3, Const.GROUND_0,
					Const.GROUND_9, Const.GROUND_6, Const.GROUND_3 }[yearGround.getIndex()]).get();
		}
	},
	// 攀鞍
	/** The mini star climb horse. */
	MINI_STAR_CLIMB_HORSE(Const.MINI_STAR_CLIMB_HORSE) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(new String[] { Const.GROUND_1, Const.GROUND_10, Const.GROUND_7,
					Const.GROUND_4, Const.GROUND_1, Const.GROUND_10, Const.GROUND_7, Const.GROUND_4, Const.GROUND_1,
					Const.GROUND_10, Const.GROUND_7, Const.GROUND_4 }[yearGround.getIndex()]).get();
		}
	},
	// 歲驛
	/** The mini star age horse. */
	MINI_STAR_AGE_HORSE(Const.MINI_STAR_AGE_HORSE) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(new String[] { Const.GROUND_2, Const.GROUND_11, Const.GROUND_8,
					Const.GROUND_5, Const.GROUND_2, Const.GROUND_11, Const.GROUND_8, Const.GROUND_5, Const.GROUND_2,
					Const.GROUND_11, Const.GROUND_8, Const.GROUND_5 }[yearGround.getIndex()]).get();
		}
	},
	// 息神
	/** The mini star rest god. */
	MINI_STAR_REST_GOD(Const.MINI_STAR_REST_GOD) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(new String[] { Const.GROUND_3, Const.GROUND_0, Const.GROUND_9,
					Const.GROUND_6, Const.GROUND_3, Const.GROUND_0, Const.GROUND_9, Const.GROUND_6, Const.GROUND_3,
					Const.GROUND_0, Const.GROUND_9, Const.GROUND_6 }[yearGround.getIndex()]).get();
		}
	},
	// 華蓋
	/** The mini star mystic. */
	MINI_STAR_MYSTIC(Const.MINI_STAR_MYSTIC) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(new String[] { Const.GROUND_4, Const.GROUND_1, Const.GROUND_10,
					Const.GROUND_7, Const.GROUND_4, Const.GROUND_1, Const.GROUND_10, Const.GROUND_7, Const.GROUND_4,
					Const.GROUND_1, Const.GROUND_10, Const.GROUND_7 }[yearGround.getIndex()]).get();
		}
	},
	// 劫煞2
	/** The MIN i_ sta r_ littl e_ disaste r2. */
	MINI_STAR_LITTLE_DISASTER2(Const.MINI_STAR_LITTLE_DISASTER2, Const.MINI_STAR_LITTLE_DISASTER) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(new String[] { Const.GROUND_5, Const.GROUND_2, Const.GROUND_11,
					Const.GROUND_8, Const.GROUND_5, Const.GROUND_2, Const.GROUND_11, Const.GROUND_8, Const.GROUND_5,
					Const.GROUND_2, Const.GROUND_11, Const.GROUND_8 }[yearGround.getIndex()]).get();
		}
	},
	// 災煞
	/** The mini star disaster. */
	MINI_STAR_DISASTER(Const.MINI_STAR_DISASTER) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(new String[] { Const.GROUND_6, Const.GROUND_3, Const.GROUND_0,
					Const.GROUND_9, Const.GROUND_6, Const.GROUND_3, Const.GROUND_0, Const.GROUND_9, Const.GROUND_6,
					Const.GROUND_3, Const.GROUND_0, Const.GROUND_9 }[yearGround.getIndex()]).get();
		}
	},
	// 天煞
	/** The mini star sky disaster. */
	MINI_STAR_SKY_DISASTER(Const.MINI_STAR_SKY_DISASTER) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(new String[] { Const.GROUND_7, Const.GROUND_4, Const.GROUND_1,
					Const.GROUND_10, Const.GROUND_7, Const.GROUND_4, Const.GROUND_1, Const.GROUND_10, Const.GROUND_7,
					Const.GROUND_4, Const.GROUND_1, Const.GROUND_10 }[yearGround.getIndex()]).get();
		}
	},
	// 指背
	/** The mini star betray. */
	MINI_STAR_BETRAY(Const.MINI_STAR_BETRAY) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(new String[] { Const.GROUND_8, Const.GROUND_5, Const.GROUND_2,
					Const.GROUND_11, Const.GROUND_8, Const.GROUND_5, Const.GROUND_2, Const.GROUND_11, Const.GROUND_8,
					Const.GROUND_5, Const.GROUND_2, Const.GROUND_11 }[yearGround.getIndex()]).get();
		}
	},
	// 咸池2
	/** The MIN i_ sta r_ ba d_ romanc e2. */
	MINI_STAR_BAD_ROMANCE2(Const.MINI_STAR_BAD_ROMANCE2, Const.MINI_STAR_BAD_ROMANCE) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(new String[] { Const.GROUND_9, Const.GROUND_6, Const.GROUND_3,
					Const.GROUND_0, Const.GROUND_9, Const.GROUND_6, Const.GROUND_3, Const.GROUND_0, Const.GROUND_9,
					Const.GROUND_6, Const.GROUND_3, Const.GROUND_0 }[yearGround.getIndex()]).get();
		}
	},
	// 月煞
	/** The mini star moon monster. */
	MINI_STAR_MOON_MONSTER(Const.MINI_STAR_MOON_MONSTER) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(new String[] { Const.GROUND_10, Const.GROUND_7, Const.GROUND_4,
					Const.GROUND_1, Const.GROUND_10, Const.GROUND_7, Const.GROUND_4, Const.GROUND_1, Const.GROUND_10,
					Const.GROUND_7, Const.GROUND_4, Const.GROUND_1 }[yearGround.getIndex()]).get();
		}
	},
	// 亡神
	/** The mini star dead god. */
	MINI_STAR_DEAD_GOD(Const.MINI_STAR_DEAD_GOD) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(new String[] { Const.GROUND_11, Const.GROUND_8, Const.GROUND_5,
					Const.GROUND_2, Const.GROUND_11, Const.GROUND_8, Const.GROUND_5, Const.GROUND_2, Const.GROUND_11,
					Const.GROUND_8, Const.GROUND_5, Const.GROUND_2 }[yearGround.getIndex()]).get();
		}
	},;

	/** The star name. */
	private String starName;

	/** The display name. */
	private String displayName;

	/** The display name to value map. */
	private static Map<String, MiniStar> displayNameToValueMap = new HashMap<String, MiniStar>();

	/** The Constant COUNT. */
	public static final int COUNT = Ground.values().length;

	static {
		for (MiniStar secondaryStar : MiniStar.values()) {
			displayNameToValueMap.put(secondaryStar.displayName, secondaryStar);
		}
	}

	/**
	 * Instantiates a new mini star.
	 *
	 * @param starName
	 *            the star name
	 */
	private MiniStar(String starName) {
		this.starName = starName;
		this.displayName = starName;
	}

	/**
	 * Instantiates a new mini star.
	 *
	 * @param starName
	 *            the star name
	 * @param displayName
	 *            the display name
	 */
	private MiniStar(String starName, String displayName) {
		this.starName = starName;
		this.displayName = displayName;
	}

	/**
	 * Gets the star name.
	 *
	 * @return the star name
	 */
	public String getStarName() {
		return starName;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.airic.fortel.model.Star#getDisplayName()
	 */
	public String getDisplayName() {
		return this.displayName;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see java.lang.Enum#toString()
	 */
	@JsonValue
	public String toString() {
		return this.displayName;
	}

	/**
	 * Gets the by display name.
	 *
	 * @param name
	 *            the name
	 * @return the by display name
	 */
	public static Optional<MiniStar> getByDisplayName(String name) {
		return Optional.<MiniStar>of(displayNameToValueMap.get(name));
	}

	/**
	 * Contain.
	 *
	 * @param displayName
	 *            the display name
	 * @return true, if successful
	 */
	public static boolean contain(String displayName) {
		return displayNameToValueMap.get(displayName) != null;
	}
}