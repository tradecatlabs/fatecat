package com.airic.fortel.core.calendar.util;

import java.util.Optional;

import org.joda.time.DateTime;
import org.joda.time.DateTimeZone;
import org.joda.time.Duration;

/**
 * The Class LunarUtil.
 */
public final class LunarUtil {

	/** 大寫月數. */
	private static final String CHN_NUMBER[] = { "一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "冬", "臘" };

	/** 陰曆月數大小. */
	private static final String BIG_OR_SMALL[] = { "大", "小", "大", "小", "大", "小", "大", "大", "小", "大", "小", "大" };

	/** 二十四節氣. */
	/*
	 * private String[] LunarHolDayName = { "小寒", "大寒", "立春", "雨水", "驚蟄", "春分",
	 * "清明", "谷雨", "立夏", "小滿", "芒種", "夏至", "小暑", "大暑", "立秋", "處暑", "白露", "秋分",
	 * "寒露", "霜降", "立冬", "小雪", "大雪", "冬至" };
	 */

	public static final DateTime LUNAR_MIN_DATE = new DateTime(1900, 1, 1, 0, 0, 0, DateTimeZone.forID("UTC"));

	/** The Constant LUNAR_MAX_DATE. */
	public static final DateTime LUNAR_MAX_DATE = new DateTime(2099, 12, 30, 23, 59, 59, DateTimeZone.forID("UTC"));

	/** The Constant SOLAR_MIN_DATE. */
	public static final DateTime SOLAR_MIN_DATE = new DateTime(1900, 1, 31, 0, 0, 0, DateTimeZone.forID("UTC"));

	/** The Constant SOLAR_MAX_DATE. */
	public static final DateTime SOLAR_MAX_DATE = new DateTime(2099, 12, 31, 23, 59, 59, DateTimeZone.forID("UTC"));

	//@formatter:off
	/** 從1900到2049年的陰曆信息. */
	private static final long[] LUNAR_INFO = new long[] {
			0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2,// 1900-1909
	        0x04ae0, 0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0, 0x14977,// 1910-1919
	        0x04970, 0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970,// 1920-1929
	        0x06566, 0x0d4a0, 0x0ea50, 0x06e95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950,// 1930-1939
	        0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0, 0x092d0, 0x0d2b2, 0x0a950, 0x0b557,// 1940-1949
	        0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5b0, 0x14573, 0x052b0, 0x0a9a8, 0x0e950, 0x06aa0,// 1950-1959
	        0x0aea6, 0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260, 0x0f263, 0x0d950, 0x05b57, 0x056a0,// 1960-1969
	        0x096d0, 0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558, 0x0b540, 0x0b6a0, 0x195a6,// 1970-1979
	        0x095b0, 0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46, 0x0ab60, 0x09570,// 1980-1989
	        0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x055c0, 0x0ab60, 0x096d5, 0x092e0,// 1990-1999
	        0x0c960, 0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0, 0x0cab5,// 2000-2009
	        0x0a950, 0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x15176, 0x052b0, 0x0a930,// 2010-2019
	        0x07954, 0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0, 0x0d260, 0x0ea65, 0x0d530,// 2020-2029
	        0x05aa0, 0x076a3, 0x096d0, 0x04bdb, 0x04ad0, 0x0a4d0, 0x1d0b6, 0x0d250, 0x0d520, 0x0dd45,// 2030-2039
	        0x0b5a0, 0x056d0, 0x055b2, 0x049b0, 0x0a577, 0x0a4b0, 0x0aa50, 0x1b255, 0x06d20, 0x0ada0,// 2040-2049
	        0x14b63, 0x09370, 0x049f8, 0x04970, 0x064b0, 0x168a6, 0x0ea50, 0x06b20, 0x1a6c4, 0x0aae0,// 2050-2059
	        0x0a2e0, 0x0d2e3, 0x0c960, 0x0d557, 0x0d4a0, 0x0da50, 0x05d55, 0x056a0, 0x0a6d0, 0x055d4,// 2060-2069
	        0x052d0, 0x0a9b8, 0x0a950, 0x0b4a0, 0x0b6a6, 0x0ad50, 0x055a0, 0x0aba4, 0x0a5b0, 0x052b0,// 2070-2079
	        0x0b273, 0x06930, 0x07337, 0x06aa0, 0x0ad50, 0x14b55, 0x04b60, 0x0a570, 0x054e4, 0x0d160,// 2080-2089
	        0x0e968, 0x0d520, 0x0daa0, 0x16aa6, 0x056d0, 0x04ae0, 0x0a9d4, 0x0a2d0, 0x0d150, 0x0f252,// 2090-2099
	        0x0d520 };
	//@formatter:off

	/**
	 * 陰曆轉陽曆
	 * 
	 * 
	 * 
	 * 輸入的年-1後，循環遍曆獲取該年天數，一直遞減到1900年的己亥年，求出年的總天數。
	 * 
	 * 
	 * 再求出該年的陰曆月日到春節一月一日的天數（這裏就要註意閏月了）。
	 * 
	 * 
	 * 如果傳入的月數大於閏月，則要加上閏月的天數。
	 * 
	 * 
	 * 
	 * 
	 * 
	 * 如果傳入的是閏月，則沒關系，直接加上前面幾個月的天數和自己的日子。
	 * 
	 * 
	 * 
	 * 
	 * 
	 * 最後得到該陰曆日期到1900年1月31日的天數，再換算出公曆Date.
	 *
	 * @param year
	 *            the year
	 * @param month
	 *            the month
	 * @param day
	 *            the day
	 * @param isLeapMonth
	 *            傳入的月是否為閏月
	 * @return the optional
	 */
	public static Optional<Solar> lunar2Solar(int year, int month, int day, boolean isLeapMonth) {
		if (!testDateInputValidRange(new Lunar(year, month, day, isLeapMonth))) {
			return Optional.empty();
		}

		// 【1】數據準備
		int totalDays = 0;// 該陰曆到公曆1900年1月31日的總日子數

		// 【2】求出該年到春節一月一日的總天數
		// 2.1.獲取該年的閏月
		int leapMonth = leapMonth(year);
		// 2.2.如果該年存在閏月，且傳入的月份在閏月後，先加上一個閏月日子數
		if (leapMonth > 0 && leapMonth < month) {
			totalDays += leapDays(year);
		}
		// 2.3.如果傳入的是閏月，則先加上一個該月非閏月的天數，因為下面直接就跳過該月了。
		else if (leapMonth == month && isLeapMonth) {
			totalDays += monthDays(year, month);
		}
		// 2.4.求出到除本月後，其他先前月份的總日子數
		for (--month; month > 0; month--) {
			totalDays += monthDays(year, month);
		}
		// 2.5.加上日子的天數
		totalDays += day;

		// 【3】求出到1900年的己亥年，年的總天數。
		for (--year; year >= 1900; year--) {
			totalDays += yearDays(year);
		}

		// 【4】計算從1900年1月30日到入參陰曆的相對時間，以此得出該陰曆的陽曆日期
		DateTime date19000130 = new DateTime(1900, 1, 30, 0, 0, 0, DateTimeZone.forID("UTC"));
		DateTime solarDate = date19000130.plusDays(totalDays);

		Solar pojo = new Solar(solarDate.getYear(), solarDate.getMonthOfYear(), solarDate.getDayOfMonth());
		return Optional.of(pojo);
	}

	/**
	 * 陽曆日期轉換為陰曆日期.
	 *
	 * @param year
	 *            the year
	 * @param month
	 *            the month
	 * @param day
	 *            the day
	 * @return the optional
	 */
	public static Optional<Lunar> solar2Lunar(int year, int month, int day) {
		if (!testDateInputValidRange(new Solar(year, month, day))) {
			return Optional.empty();
		}

		// 【1】數據初始化和準備
		Lunar lunar = new Lunar();
		@SuppressWarnings("unused")
		int monCyl;// 從1900年1月31日以來,閏月數
		int leapMonth = 0;

		// 【2】求出和1900年1月31日相差的天數
		DateTime date19000131 = new DateTime(1900, 1, 31, 0, 0, 0, DateTimeZone.forID("UTC"));
		DateTime dateSolarDay = new DateTime(year, month, day, 0, 0, 0, DateTimeZone.forID("UTC"));
		Duration duration = new Duration(date19000131, dateSolarDay);
		int offset = (int) duration.getStandardDays();

		// 【3】通過相差天數，求出農曆年月日
		monCyl = 14;
		// 3.1.求出農曆年份
		int iYear, daysOfYear = 0;
		for (iYear = 1900; iYear < LUNAR_MAX_DATE.getYear() && offset > 0; iYear++) {
			// 一直減少從1900年1月31日的年天數，直到減到今年
			daysOfYear = yearDays(iYear);
			if (offset >= daysOfYear) {
				offset -= daysOfYear;
				monCyl += 12;
			} else {
				break;
			}
		}

		/*
		 * 求出了農曆年份。 農曆年份是以幹支標識的，以1900年1月31日己亥年開始。 默認1900為己亥年，1901則為辛醜。
		 * 但這個1901與公曆的1901不同，如公曆1901年1月還為己亥年，則其陰曆年為1900。
		 */
		lunar.setYear(iYear);

		// 3.2.計算農曆月份。包括是否為閏月
		leapMonth = leapMonth(iYear); // 閏哪個月,1-12
		boolean leap = false;

		// 用當年的天數offset,逐個減去每月（農曆）的天數，求出當天是本月的第幾天
		int iMonth, daysOfMonth = 0;
		for (iMonth = 1; iMonth < 13 && offset > 0; iMonth++) {
			// 判斷是否為閏月
			if (leapMonth > 0 && iMonth == (leapMonth + 1) && !leap) {
				--iMonth;
				leap = true;
				daysOfMonth = leapDays(lunar.getYear());
			} else {
				daysOfMonth = monthDays(lunar.getYear(), iMonth);
			}

			offset -= daysOfMonth;
			// 解除閏月
			if (leap && iMonth == (leapMonth + 1)) {
				leap = false;
			}
			if (!leap) {
				monCyl++;
			}
		}
		// offset為0時，並且剛才計算的月份是閏月，要校正
		if (offset == 0 && leapMonth > 0 && iMonth == leapMonth + 1) {
			if (leap) {
				leap = false;
			} else {
				leap = true;
				--iMonth;
				--monCyl;
			}
		}
		// offset小於0時，也要校正
		if (offset < 0) {
			offset += daysOfMonth;
			--iMonth;
			--monCyl;
		}
		// 求出了月日及是否為閏月
		lunar.setMonth(iMonth);
		lunar.setDay(offset + 1);
		lunar.setLeap(leap);
		return Optional.of(lunar);
	}

	/**
	 * * 傳回農曆 y年的生肖 * * @return.
	 *
	 * @param year
	 *            the year
	 * @return the string
	 */
	public static String animalsYear(int year) {
		final String[] Animals = new String[] { "鼠", "牛", "虎", "兔", "龍", "蛇", "馬", "羊", "猴", "雞", "狗", "豬" };
		return Animals[(year - 4) % 12];
	}

	/**
	 * * 傳回幹支, 0=甲子 * * @param year * @return.
	 *
	 * @param year
	 *            the year
	 * @return the string
	 */
	public static String cyclical(int year) {
		int num = year - 1900 + 36;
		return (cyclicalm(num));
	}

	/**
	 * * 返回陰曆的月份 * * @param month * @return.
	 *
	 * @param month
	 *            the month
	 * @return the chn month
	 */
	public static String getChnMonth(int month) {
		return CHN_NUMBER[month - 1];
	}

	/**
	 * * 返回陰曆的天 * * @param day * @return.
	 *
	 * @param day
	 *            the day
	 * @return the chn day
	 */
	public static String getChnDay(int day) {
		return getChinaDayString(day);
	}

	/**
	 * * 返回的月份的大或小 * * @param month * @return.
	 *
	 * @param month
	 *            the month
	 * @return the big or small
	 */
	public static String getBigOrSmall(int month) {
		return BIG_OR_SMALL[month - 1];
	}

	/**
	 * Gets the prev lunar.
	 *
	 * @param year
	 *            the year
	 * @param month
	 *            the month
	 * @param day
	 *            the day
	 * @param isLeap
	 *            the is leap
	 * @return the prev lunar
	 */
	public static Optional<Lunar> getPrevLunar(int year, int month, int day, boolean isLeap) {
		Optional<Solar> solarDate = lunar2Solar(year, month, day, isLeap);
		if (solarDate.isPresent()) {
			DateTime calendarRefDay = new DateTime(solarDate.get().getYear(), solarDate.get().getMonth(), solarDate.get().getDay(), 0, 0,
			        0, DateTimeZone.forID("UTC"));
			DateTime prevSolarDate = calendarRefDay.plusDays(-1);
			Optional<Lunar> prevLunarDate = LunarUtil.solar2Lunar(prevSolarDate.getYear(), prevSolarDate.getMonthOfYear(),
			        prevSolarDate.getDayOfMonth());
			return prevLunarDate;
		}
		return Optional.empty();
	}

	/**
	 * Gets the next lunar.
	 *
	 * @param year
	 *            the year
	 * @param month
	 *            the month
	 * @param day
	 *            the day
	 * @param isLeap
	 *            the is leap
	 * @return the next lunar
	 */
	public static Optional<Lunar> getNextLunar(int year, int month, int day, boolean isLeap) {
		Optional<Solar> solarDate = lunar2Solar(year, month, day, isLeap);
		if (solarDate.isPresent()) {
			DateTime calendarRefDay = new DateTime(solarDate.get().getYear(), solarDate.get().getMonth(), solarDate.get().getDay(), 0, 0,
			        0, DateTimeZone.forID("UTC"));
			DateTime nextSolarDate = calendarRefDay.plusDays(1);
			Optional<Lunar> nextLunarDate = LunarUtil.solar2Lunar(nextSolarDate.getYear(), nextSolarDate.getMonthOfYear(),
			        nextSolarDate.getDayOfMonth());
			return nextLunarDate;
		}
		return Optional.empty();
	}

	/**
	 * * 傳回農曆 y年的總天數 * * @param yyyy 四位年數 * @return.
	 *
	 * @param yyyy
	 *            the yyyy
	 * @return the int
	 */
	private static int yearDays(int yyyy) {
		int i, sum = 348;
		for (i = 0x8000; i > 0x8; i >>= 1) {
			if ((LUNAR_INFO[yyyy - 1900] & i) != 0)
				sum += 1;
		}
		return (sum + leapDays(yyyy));
	}

	/**
	 * 傳回農曆 y年閏月的天數.
	 *
	 * @param yyyy
	 *            四位年數
	 * @return the int
	 */
	private static int leapDays(int yyyy) {
		if (leapMonth(yyyy) != 0) {
			if ((LUNAR_INFO[yyyy - 1900] & 0x10000) != 0)
				return 30;
			else
				return 29;
		} else
			return 0;
	}

	/**
	 * 傳回農曆 y年閏哪個月 1-12 , 沒閏傳回 0.
	 *
	 * @param yyyy
	 *            四位年數
	 * @return the int
	 */
	public static int leapMonth(int yyyy) {
		return (int) (LUNAR_INFO[yyyy - 1900] & 0xf);
	}

	/**
	 * 傳回農曆 y年m月的總天數.
	 *
	 * @param y
	 *            the y
	 * @param m
	 *            the m
	 * @return the int
	 */
	private static int monthDays(int y, int m) {
		if ((LUNAR_INFO[y - 1900] & (0x10000 >> m)) == 0)
			return 29;
		else
			return 30;
	}

	/**
	 * 傳回幹支, 0=甲子.
	 *
	 * @param num
	 *            the num
	 * @return the string
	 */
	private static String cyclicalm(int num) {
		final String[] Gan = new String[] { "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸" };
		final String[] Zhi = new String[] { "子", "醜", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥" };
		return (Gan[num % 10] + Zhi[num % 12]);
	}

	/**
	 * 將數字日轉換為中國日。如21轉換為廿一.
	 *
	 * @param day
	 *            the day
	 * @return the china day string
	 */
	private static String getChinaDayString(int day) {
		String chineseTen[] = { "初", "十", "廿", "三" };
		int n = day % 10 == 0 ? 9 : day % 10 - 1;
		if (day > 30)
			return "";
		if (day == 10)
			return "初十";
		if (day == 20)
			return "二十";
		else
			return chineseTen[day / 10] + CHN_NUMBER[n];
	}

	/**
	 * Test date input valid range.
	 *
	 * @param lunar
	 *            the lunar
	 * @return true, if successful
	 */
	public static boolean testDateInputValidRange(Lunar lunar) {
		int year = lunar.getYear();
		int month = lunar.getMonth();
		int day = lunar.getDay();

		if (year < LUNAR_MIN_DATE.getYear()) {
			return false;
		} else if (year == LUNAR_MIN_DATE.getYear()) {
			if (month < LUNAR_MIN_DATE.getMonthOfYear()) {
				return false;
			} else if (month == LUNAR_MIN_DATE.getMonthOfYear()) {
				if (day < LUNAR_MIN_DATE.getDayOfMonth()) {
					return false;
				}
			}
		}

		if (year > LUNAR_MAX_DATE.getYear()) {
			return false;
		} else if (year == LUNAR_MAX_DATE.getYear()) {
			if (month > LUNAR_MAX_DATE.getMonthOfYear()) {
				return false;
			} else if (month == LUNAR_MAX_DATE.getMonthOfYear()) {
				if (day > LUNAR_MAX_DATE.getDayOfMonth()) {
					return false;
				}
			}
		}

		if (!lunar.isLeap() && day > monthDays(year, month)) {
			return false;
		}
		
		if (lunar.isLeap() && lunar.getMonth() != leapMonth(year)) {
			return false;
		}
		
		if (lunar.isLeap() && day > leapDays(year)) {
			return false;
		}
		
		return true;
	}

	/**
	 * Test date input valid range.
	 *
	 * @param solar
	 *            the solar
	 * @return true, if successful
	 */
	public static boolean testDateInputValidRange(Solar solar) {
		int year = solar.getYear();
		int month = solar.getMonth();
		int day = solar.getDay();

		int[] monthDayMax = new int[] { 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
		if (month < 1 || month > 12) {
			return false;
		}
		if (day < 1 || day > monthDayMax[month - 1]) {
			return false;
		}
		if (month == 2 && day == 29) {
			if (!(year % 4 == 0 && (year % 100 != 0 || year % 400 == 0))) {
				return false;
			}
		}

		if (year < SOLAR_MIN_DATE.getYear()) {
			return false;
		} else if (year == SOLAR_MIN_DATE.getYear()) {
			if (month < SOLAR_MIN_DATE.getMonthOfYear()) {
				return false;
			} else if (month == SOLAR_MIN_DATE.getMonthOfYear()) {
				if (day < SOLAR_MIN_DATE.getDayOfMonth()) {
					return false;
				}
			}
		}

		if (year > SOLAR_MAX_DATE.getYear()) {
			return false;
		} else if (year == SOLAR_MAX_DATE.getYear()) {
			if (month > SOLAR_MAX_DATE.getMonthOfYear()) {
				return false;
			} else if (month == SOLAR_MAX_DATE.getMonthOfYear()) {
				if (day > SOLAR_MAX_DATE.getDayOfMonth()) {
					return false;
				}
			}
		}

		return true;
	}

}