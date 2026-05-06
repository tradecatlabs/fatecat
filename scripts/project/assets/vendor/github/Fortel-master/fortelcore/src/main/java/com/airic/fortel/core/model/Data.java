package com.airic.fortel.core.model;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import com.airic.fortel.core.util.CommonUtil;
import com.airic.fortel.core.util.CommonUtil.MapWrapper;
import com.fasterxml.jackson.annotation.JsonValue;

/**
 * The Class Data.
 */
public final class Data {

	/** The Constant NUM_CELLS. */
	public static final int NUM_CELLS = 12;

	/**
	 * The Enum Calendar.
	 */
	public static enum Calendar {
		/** The lunar. */
		LUNAR,
		/** The solar. */
		SOLAR
	}

	/**
	 * The Enum GroundTime.
	 */
	public static enum GroundTime {

		/** The GROUN d_0. */
		GROUND_0("早子", 0, "00:00am-00:59am", 0, 1),
		/** The GROUN d_1. */
		GROUND_1("丑", 1, "01:00am-02:59am", 1, 3),
		/** The GROUN d_2. */
		GROUND_2("寅", 2, "03:00am-04:59am", 3, 5),
		/** The GROUN d_3. */
		GROUND_3("卯", 3, "05:00am-06:59am", 5, 7),
		/** The GROUN d_4. */
		GROUND_4("辰", 4, "07:00am-08:59am", 7, 9),
		/** The GROUN d_5. */
		GROUND_5("巳", 5, "09:00am-10:59am", 9, 11),
		/** The GROUN d_6. */
		GROUND_6("午", 6, "11:00am-12:59pm", 11, 13),
		/** The GROUN d_7. */
		GROUND_7("未", 7, "13:00pm-14:59pm", 13, 15),
		/** The GROUN d_8. */
		GROUND_8("申", 8, "15:00pm-16:59pm", 15, 17),
		/** The GROUN d_9. */
		GROUND_9("酉", 9, "17:00pm-18:59pm", 17, 19),
		/** The GROUN d_10. */
		GROUND_10("戌", 10, "19:00pm-20:59pm", 19, 21),
		/** The GROUN d_11. */
		GROUND_11("亥", 11, "21:00pm-22:59pm", 21, 23),
		/** The GROUN d_12. */
		GROUND_12("夜子", 12, "23:00pm-23:59pm", 23, 24);

		/** The display name. */
		private String displayName;

		/** The index. */
		private int index;

		/** The time period. */
		private String timePeriod;

		/** The start hour. */
		private int startHour;

		/** The end hour. */
		private int endHour;

		/** The Constant COUNT. */
		public static final int COUNT = GroundTime.values().length;

		/**
		 * Instantiates a new ground time.
		 *
		 * @param displayName
		 *            the display name
		 * @param index
		 *            the index
		 * @param timePeriod
		 *            the time period
		 * @param startHour
		 *            the start hour
		 * @param endHour
		 *            the end hour
		 */
		private GroundTime(String displayName, int index, String timePeriod, int startHour, int endHour) {
			this.displayName = displayName;
			this.index = index;
			this.timePeriod = timePeriod;
			this.startHour = startHour;
			this.endHour = endHour;
		}

		/**
		 * Gets the display name.
		 *
		 * @return the display name
		 */
		public String getDisplayName() {
			return this.displayName;
		}

		/**
		 * Gets the index.
		 *
		 * @return the index
		 */
		@JsonValue
		public int getIndex() {
			return index;
		}

		/**
		 * Gets the time period.
		 *
		 * @return the time period
		 */
		public String getTimePeriod() {
			return timePeriod;
		}

		/**
		 * Gets the start hour.
		 *
		 * @return the start hour
		 */
		public int getStartHour() {
			return startHour;
		}

		/**
		 * Gets the end hour.
		 *
		 * @return the end hour
		 */
		public int getEndHour() {
			return endHour;
		}

		/**
		 * Gets the ground.
		 *
		 * @return the ground
		 */
		public Ground getGround() {
			return Ground.getByIndex(this.index % 12);
		}

		/**
		 * Gets the GroundTime by index.
		 *
		 * @param index
		 *            the index
		 * @return the by index
		 */
		public static GroundTime getByIndex(int index) {
			return GroundTime.values()[CommonUtil.mod(index, GroundTime.values().length)];
		}

		/**
		 * Gets the GroundTime by name.
		 *
		 * @param name
		 *            the name
		 * @return the GroundTime
		 */
		public static Optional<GroundTime> getByName(String name) {
			return Optional.ofNullable(name).map(name_ -> {
				for (GroundTime groundTime : GroundTime.values()) {
					if (groundTime.getDisplayName().equalsIgnoreCase(name_)) {
						return groundTime;
					}
				}
				return null;
			});
		}

		/**
		 * Shift.
		 *
		 * @param i
		 *            the i
		 * @return the ground time
		 */
		public GroundTime shift(int i) {
			return getByIndex(this.index + i);
		}
	}

	/**
	 * The Enum ChineseMonth.
	 */
	public static enum ChineseMonth {

		/** The MONT h1. */
		MONTH1("一月"),
		/** The MONT h2. */
		MONTH2("二月"),
		/** The MONT h3. */
		MONTH3("三月"),
		/** The MONT h4. */
		MONTH4("四月"),
		/** The MONT h5. */
		MONTH5("五月"),
		/** The MONT h6. */
		MONTH6("六月"),
		/** The MONT h7. */
		MONTH7("七月"),
		/** The MONT h8. */
		MONTH8("八月"),
		/** The MONT h9. */
		MONTH9("九月"),
		/** The MONT h10. */
		MONTH10("十月"),
		/** The MONT h11. */
		MONTH11("十一月"),
		/** The MONT h12. */
		MONTH12("十二月");

		/** The display name. */
		private String displayName = "";

		/**
		 * Instantiates a new chinese month.
		 *
		 * @param displayName
		 *            the display name
		 */
		private ChineseMonth(String displayName) {
			this.displayName = displayName;
		}

		/**
		 * Gets the display name.
		 *
		 * @return the display name
		 */
		public String getDisplayName() {
			return this.displayName;
		}
	}

	/**
	 * The Enum ChineseDay.
	 */
	public static enum ChineseDay {

		/** The DA y1. */
		DAY1("初一"),
		/** The DA y2. */
		DAY2("初二"),
		/** The DA y3. */
		DAY3("初三"),
		/** The DA y4. */
		DAY4("初四"),
		/** The DA y5. */
		DAY5("初五"),
		/** The DA y6. */
		DAY6("初六"),
		/** The DA y7. */
		DAY7("初七"),
		/** The DA y8. */
		DAY8("初八"),
		/** The DA y9. */
		DAY9("初九"),
		/** The DA y10. */
		DAY10("初十"),
		/** The DA y11. */
		DAY11("十一"),
		/** The DA y12. */
		DAY12("十二"),
		/** The DA y13. */
		DAY13("十三"),
		/** The DA y14. */
		DAY14("十四"),
		/** The DA y15. */
		DAY15("十五"),
		/** The DA y16. */
		DAY16("十六"),
		/** The DA y17. */
		DAY17("十七"),
		/** The DA y18. */
		DAY18("十八"),
		/** The DA y19. */
		DAY19("十九"),
		/** The DA y20. */
		DAY20("二十"),
		/** The DA y21. */
		DAY21("廿一"),
		/** The DA y22. */
		DAY22("廿二"),
		/** The DA y23. */
		DAY23("廿三"),
		/** The DA y24. */
		DAY24("廿四"),
		/** The DA y25. */
		DAY25("廿五"),
		/** The DA y26. */
		DAY26("廿六"),
		/** The DA y27. */
		DAY27("廿七"),
		/** The DA y28. */
		DAY28("廿八"),
		/** The DA y29. */
		DAY29("廿九"),
		/** The DA y30. */
		DAY30("三十");

		/** The display name. */
		private String displayName = "";

		/**
		 * Instantiates a new chinese day.
		 *
		 * @param displayName
		 *            the display name
		 */
		private ChineseDay(String displayName) {
			this.displayName = displayName;
		}

		/**
		 * Gets the display name.
		 *
		 * @return the display name
		 */
		public String getDisplayName() {
			return this.displayName;
		}
	}

	/**
	 * The Class DoubleMonth.
	 */
	public static class DoubleMonth {

		/** The year double month mapping. */
		private static Map<Integer, Integer> yearDoubleMonthMapping = getyearDoubleMonthMapping();

		/**
		 * Gets the year double month mapping.
		 *
		 * @return the year double month mapping
		 */
		private static Map<Integer, Integer> getyearDoubleMonthMapping() {
			MapWrapper<Integer, Integer> mapWrapper = new CommonUtil.MapWrapper<Integer, Integer>(
					new HashMap<Integer, Integer>());
			List<int[]> yearDoubleMonthMatrix = new ArrayList<int[]>();
			yearDoubleMonthMatrix.add(new int[] {});// 1
			yearDoubleMonthMatrix.add(new int[] { 1890, 1909, 1917, 1928, 1947, 2004, 2023, 2042 });// 2
			yearDoubleMonthMatrix.add(new int[] { 1860, 1879, 1898, 1936, 1955, 1966, 1993, 2031, 2050 });// 3
			yearDoubleMonthMatrix
					.add(new int[] { 1849, 1868, 1887, 1906, 1925, 1944, 1963, 1974, 1982, 2001, 2012, 2020 });// 4
			yearDoubleMonthMatrix.add(new int[] { 1857, 1865, 1876, 1884, 1895, 1903, 1914, 1922, 1933, 1952, 1971,
					1990, 1998, 2009, 2028, 2039, 2047 });// 5
			yearDoubleMonthMatrix.add(new int[] { 1873, 1892, 1911, 1930, 1941, 1960, 1979, 1987, 2017, 2025, 2036 });// 6
			yearDoubleMonthMatrix.add(new int[] { 1854, 1881, 1919, 1938, 1949, 1968, 2006, 2044 });// 7
			yearDoubleMonthMatrix.add(new int[] { 1851, 1862, 1900, 1957, 1976, 1995 });// 8
			yearDoubleMonthMatrix.add(new int[] { 2014 });// 9
			yearDoubleMonthMatrix.add(new int[] { 1870, 1984 });// 10
			yearDoubleMonthMatrix.add(new int[] { 2033 });// 11
			yearDoubleMonthMatrix.add(new int[] {});// 12

			for (int i = 0; i < yearDoubleMonthMatrix.size(); i++) {
				for (int year : yearDoubleMonthMatrix.get(i)) {
					mapWrapper.put(year, i + 1);
				}
			}

			return mapWrapper.getMap();
		}

		/**
		 * Gets the year double month.
		 *
		 * @param year
		 *            the year
		 * @return the year double month
		 */
		public static Optional<Integer> getYearDoubleMonth(int year) {
			return Optional.<Integer>ofNullable(yearDoubleMonthMapping.get(year));
		}

		/**
		 * Check double month valid.
		 *
		 * @param year
		 *            the year
		 * @param month
		 *            the month
		 * @return true, if successful
		 */
		public static boolean checkDoubleMonthValid(int year, int month) {
			return getYearDoubleMonth(year).map(doubleMonth -> {
				return doubleMonth.intValue() == month;
			}).orElse(false);
		}
	}

	/**
	 * The Enum Sex.
	 */
	public enum Sex {

		/** The m. */
		M("男"),
		/** The f. */
		F("女");

		/** The display name. */
		private String displayName;

		/**
		 * Instantiates a new sex.
		 *
		 * @param displayName
		 *            the display name
		 */
		private Sex(String displayName) {
			this.displayName = displayName;
		}

		/**
		 * Gets the display name.
		 *
		 * @return the display name
		 */
		@JsonValue
		public String getDisplayName() {
			return this.displayName;
		}

		/*
		 * (non-Javadoc)
		 * 
		 * @see java.lang.Enum#toString()
		 */
		/**
		 * To string.
		 *
		 * @return the string
		 */
		public String toString() {
			return this.displayName;
		}

		/**
		 * Gets the by name.
		 *
		 * @param name
		 *            the name
		 * @return the by name
		 */
		public static Optional<Sex> getByName(String name) {
			return Optional.ofNullable(name).map(name_ -> {
				for (Sex sex : Sex.values()) {
					if (sex.name().equalsIgnoreCase(name_)) {
						return sex;
					}
				}
				return null;
			});
		}
	}

	/**
	 * The Enum ShadowLight.
	 */
	public enum ShadowLight {

		/** The shadow. */
		SHADOW("陰"),
		/** The light. */
		LIGHT("陽");

		/** The display name. */
		private String displayName;

		/**
		 * Instantiates a new shadow light.
		 *
		 * @param displayName
		 *            the display name
		 */
		private ShadowLight(String displayName) {
			this.displayName = displayName;
		}

		/**
		 * Gets the display name.
		 *
		 * @return the display name
		 */
		@JsonValue
		public String getDisplayName() {
			return this.displayName;
		}

		/*
		 * (non-Javadoc)
		 * 
		 * @see java.lang.Enum#toString()
		 */
		/**
		 * To string.
		 *
		 * @return the string
		 */
		public String toString() {
			return this.displayName;
		}

	}

	/**
	 * The Enum FiveElement.
	 */
	public enum FiveElement {

		/** The gold. */
		GOLD("金四局", 4),
		/** The wood. */
		WOOD("木三局", 3),
		/** The earth. */
		EARTH("土五局", 5),
		/** The water. */
		WATER("水二局", 2),
		/** The fire. */
		FIRE("火六局", 6);

		/** The display name. */
		private String displayName;

		/** The number. */
		private int number;

		/**
		 * Instantiates a new five element.
		 *
		 * @param displayName
		 *            the display name
		 * @param number
		 *            the number
		 */
		private FiveElement(String displayName, int number) {
			this.displayName = displayName;
			this.number = number;
		}

		/**
		 * Gets the display name.
		 *
		 * @return the display name
		 */
		@JsonValue
		public String getDisplayName() {
			return displayName;
		}

		/**
		 * Sets the display name.
		 *
		 * @param displayName
		 *            the new display name
		 */
		public void setDisplayName(String displayName) {
			this.displayName = displayName;
		}

		/**
		 * Gets the number.
		 *
		 * @return the number
		 */
		public int getNumber() {
			return number;
		}

		/**
		 * Sets the number.
		 *
		 * @param number
		 *            the new number
		 */
		public void setNumber(int number) {
			this.number = number;
		}
	}

	/**
	 * The Enum Direction.
	 */
	public enum Direction {

		/** The clockwise. */
		CLOCKWISE(1),
		/** The anticlockwise. */
		ANTICLOCKWISE(-1);

		/** The number. */
		private int number;

		/**
		 * Instantiates a new direction.
		 *
		 * @param number
		 *            the number
		 */
		private Direction(int number) {
			this.number = number;
		}

		/**
		 * Gets the number.
		 *
		 * @return the number
		 */
		public int getNumber() {
			return this.number;
		}
	}

	/**
	 * The Enum Luck.
	 */
	public enum Luck {

		/** The luck. */
		LUCK,
		/** The neutral. */
		NEUTRAL,
		/** The bad luck. */
		BAD_LUCK;
	}

	/**
	 * The Enum StarEnergyLevel.
	 */
	public enum StarEnergyLevel {

		/** The temple. */
		TEMPLE(2, "廟", "⊕"),

		/** The good. */
		GOOD(1, "旺", "Ｏ"),

		/** The normal. */
		NORMAL(0, "平", "　"),

		/** The ground. */
		GROUND(-1, "陷", "▲");

		/** The level. */
		private int level;

		/** The display name. */
		private String displayName;

		/** The display symbol. */
		private String displaySymbol;

		/**
		 * Instantiates a new star energy level.
		 *
		 * @param level
		 *            the level
		 * @param displayName
		 *            the display name
		 * @param displaySymbol
		 *            the display symbol
		 */
		private StarEnergyLevel(int level, String displayName, String displaySymbol) {
			this.level = level;
			this.displayName = displayName;
			this.displaySymbol = displaySymbol;
		}

		/**
		 * Gets the level.
		 *
		 * @return the level
		 */
		@JsonValue
		public int getLevel() {
			return level;
		}

		/**
		 * Gets the display name.
		 *
		 * @return the display name
		 */
		public String getDisplayName() {
			return displayName;
		}

		/**
		 * Gets the display symbol.
		 *
		 * @return the display symbol
		 */
		public String getDisplaySymbol() {
			return displaySymbol;
		}

		/**
		 * Gets the by level.
		 *
		 * @param level
		 *            the level
		 * @return the by level
		 */
		public static StarEnergyLevel getByLevel(int level) {
			if (level == 2) {
				return StarEnergyLevel.TEMPLE;
			} else if (level == 1) {
				return StarEnergyLevel.GOOD;
			} else if (level == -1) {
				return StarEnergyLevel.GROUND;
			} else {
				return StarEnergyLevel.NORMAL;
			}
		}
	}

	// 六煞
	/** The Constant BAD_STARS. */
	public static final MinorStar[] BAD_STARS = new MinorStar[] { MinorStar.MINOR_STAR_EMPTY_GROUND,
			MinorStar.MINOR_STAR_GROUND_DISASTER, MinorStar.MINOR_STAR_FIRE_BURN,
			MinorStar.MINOR_STAR_INVISIBLE_PROBLEM, MinorStar.MINOR_STAR_FAILURE, MinorStar.MINOR_STAR_HINDER };

	// 六煞加上化忌
	/** The Constant BAD_STARS_AND_REACTION_PROBLEM. */
	public static final StarElement[] BAD_STARS_AND_REACTION_PROBLEM = new StarElement[] {
			MinorStar.MINOR_STAR_EMPTY_GROUND, MinorStar.MINOR_STAR_GROUND_DISASTER, MinorStar.MINOR_STAR_FIRE_BURN,
			MinorStar.MINOR_STAR_INVISIBLE_PROBLEM, MinorStar.MINOR_STAR_FAILURE, MinorStar.MINOR_STAR_HINDER,
			StarReaction.STAR_TO_PROBLEM };

	// 四煞
	/** The Constant FOUR_BAD_STARS. */
	public static final MinorStar[] FOUR_BAD_STARS = new MinorStar[] { MinorStar.MINOR_STAR_FIRE_BURN,
			MinorStar.MINOR_STAR_INVISIBLE_PROBLEM, MinorStar.MINOR_STAR_FAILURE, MinorStar.MINOR_STAR_HINDER };

	// 四煞加上化忌
	/** The Constant FOUR_BAD_STARS_AND_REACTION_PROBLEM. */
	public static final StarElement[] FOUR_BAD_STARS_AND_REACTION_PROBLEM = new StarElement[] {
			MinorStar.MINOR_STAR_FIRE_BURN, MinorStar.MINOR_STAR_INVISIBLE_PROBLEM, MinorStar.MINOR_STAR_FAILURE,
			MinorStar.MINOR_STAR_HINDER, StarReaction.STAR_TO_PROBLEM };

	// 空曜
	/** The Constant EMPTY_STARS. */
	public static final Star[] EMPTY_STARS = new Star[] { MinorStar.MINOR_STAR_EMPTY_GROUND,
			MiniStar.MINI_STAR_EMPTY_SKY, MiniStar.MINI_STAR_LAZY_SKY, MiniStar.MINI_STAR_LAZY_SKY2,
			MiniStar.MINI_STAR_INTERRUPT_SKY, MiniStar.MINI_STAR_INTERRUPT_SKY2 };

	// 吉曜
	/** The Constant GOOD_STARS. */
	public static final MinorStar[] GOOD_STARS = new MinorStar[] { MinorStar.MINOR_STAR_CLOTH,
			MinorStar.MINOR_STAR_CLEVER, MinorStar.MINOR_STAR_SKILL, MinorStar.MINOR_STAR_HONOR,
			MinorStar.MINOR_STAR_HONOR2, MinorStar.MINOR_STAR_LEFT_SUPPORT, MinorStar.MINOR_STAR_RIGHT_SUPPORT };

	// 吉曜加上化祿
	/** The Constant GOOD_STARS_AND_REACTION_TREASURE. */
	public static final StarElement[] GOOD_STARS_AND_REACTION_TREASURE = new StarElement[] { MinorStar.MINOR_STAR_CLOTH,
			MinorStar.MINOR_STAR_CLEVER, MinorStar.MINOR_STAR_SKILL, MinorStar.MINOR_STAR_HONOR,
			MinorStar.MINOR_STAR_HONOR2, MinorStar.MINOR_STAR_LEFT_SUPPORT, MinorStar.MINOR_STAR_RIGHT_SUPPORT,
			StarReaction.STAR_TO_TREASURE };

	// 桃花星
	/** The Constant GOOD_STARS. */
	public static final Star[] ROMANCE_STARS = new Star[] { MinorStar.MINOR_STAR_SKILL, MiniStar.MINI_STAR_SKY_ROMANTIC,
			MiniStar.MINI_STAR_BAD_ROMANCE, MiniStar.MINI_STAR_BAD_ROMANCE2, MiniStar.MINI_STAR_RED_MARRIAGE };

	/** The Constant RUNTIME_MINOR_STARS. */
	public static final MinorStar[] RUNTIME_MINOR_STARS = new MinorStar[] { MinorStar.MINOR_STAR_CLEVER,
			MinorStar.MINOR_STAR_CLOTH, MinorStar.MINOR_STAR_EMPTY_GROUND, MinorStar.MINOR_STAR_FAILURE,
			MinorStar.MINOR_STAR_FIRE_BURN, MinorStar.MINOR_STAR_GROUND_DISASTER, MinorStar.MINOR_STAR_HINDER,
			MinorStar.MINOR_STAR_HONOR, MinorStar.MINOR_STAR_HONOR2, MinorStar.MINOR_STAR_HORSE_CHANGE,
			MinorStar.MINOR_STAR_INVISIBLE_PROBLEM, MinorStar.MINOR_STAR_LEFT_SUPPORT,
			MinorStar.MINOR_STAR_RIGHT_SUPPORT, MinorStar.MINOR_STAR_SKILL };

	/** The Constant fiveElementMap. */
	public static final FiveElement[][] fiveElementMap = new FiveElement[][] {
			new FiveElement[] { FiveElement.GOLD, FiveElement.WATER, FiveElement.FIRE, FiveElement.GOLD,
					FiveElement.WATER, FiveElement.FIRE },
			new FiveElement[] { FiveElement.WATER, FiveElement.FIRE, FiveElement.EARTH, FiveElement.WATER,
					FiveElement.FIRE, FiveElement.EARTH },
			new FiveElement[] { FiveElement.FIRE, FiveElement.EARTH, FiveElement.WOOD, FiveElement.FIRE,
					FiveElement.EARTH, FiveElement.WOOD },
			new FiveElement[] { FiveElement.EARTH, FiveElement.WOOD, FiveElement.GOLD, FiveElement.EARTH,
					FiveElement.WOOD, FiveElement.GOLD },
			new FiveElement[] { FiveElement.WOOD, FiveElement.GOLD, FiveElement.WATER, FiveElement.WOOD,
					FiveElement.GOLD, FiveElement.WATER } };
}
