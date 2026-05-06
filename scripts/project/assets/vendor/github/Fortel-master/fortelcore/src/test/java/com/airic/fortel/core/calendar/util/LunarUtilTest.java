package com.airic.fortel.core.calendar.util;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

/**
 * The Class LunarUtilTest.
 */
public class LunarUtilTest {

	/**
	 * Test.
	 */
	@Test
	public void test() {
		{
			Lunar lunar = new Lunar(LunarUtil.LUNAR_MAX_DATE.getYear(), LunarUtil.LUNAR_MAX_DATE.getMonthOfYear(),
					LunarUtil.LUNAR_MAX_DATE.getDayOfMonth(), false);
			Solar solar = LunarUtil.lunar2Solar(lunar.getYear(), lunar.getMonth(), lunar.getDay(), lunar.isLeap())
					.orElse(null);
			System.out.println(lunar);
			System.out.println(solar);
		}
		System.out.println("test LunarUtil");

		/*
		 * 農曆西曆互相轉換
		 */
		for (int year = LunarUtil.LUNAR_MIN_DATE.getYear(); year < LunarUtil.LUNAR_MAX_DATE.getYear(); year++) {
			for (int month = 1; month <= 12; month++) {
				for (int day = 1; day <= 31; day++) {
					Lunar lunar = new Lunar(year, month, day, false);
					if (LunarUtil.testDateInputValidRange(lunar)) {
						Solar solarDate = LunarUtil.lunar2Solar(year, month, day, false).orElse(null);
						if (solarDate != null && LunarUtil.testDateInputValidRange(solarDate)) {
							Lunar lunarDate = LunarUtil
									.solar2Lunar(solarDate.getYear(), solarDate.getMonth(), solarDate.getDay()).get();
							if (lunarDate.getYear() != year || lunarDate.getMonth() != month
									|| lunarDate.getDay() != day || lunarDate.isLeap()) {
								System.out.println("incorrect conversion of lunar->solar->lunar: " + year + " " + month
										+ " " + day);
							}
						}
					}

					Solar solar = new Solar(year, month, day);
					if (LunarUtil.testDateInputValidRange(solar)) {
						Lunar lunarDate = LunarUtil.solar2Lunar(year, month, day).orElse(null);
						if (lunarDate != null && LunarUtil.testDateInputValidRange(lunarDate)) {
							Solar solarDate = LunarUtil.lunar2Solar(lunarDate.getYear(), lunarDate.getMonth(),
									lunarDate.getDay(), lunarDate.isLeap()).get();
							if (solarDate.getYear() != year || solarDate.getMonth() != month
									|| solarDate.getDay() != day) {
								System.out.println("incorrect conversion of solar->lunar->solar: " + year + " " + month
										+ " " + day);
							}
						}
					}
				}
			}
		}

		{
			// test農曆1990-1-30並不存在，是錯誤日子
			Solar solar = LunarUtil.lunar2Solar(1990, 1, 30, false).orElse(null);
			Assertions.assertNull(solar);
			if (solar != null) {
				System.out.println("lunar2Solar incorrect: lunar 1901-1-30 should return null as it is invalid input.");
			}
		}

		{
			// test西曆1990-6-23->農曆閏五月初一
			Lunar lunar = LunarUtil.solar2Lunar(1990, 6, 23).orElse(null);
			Assertions.assertNotNull(lunar);
			Assertions.assertEquals(1990, lunar.getYear());
			Assertions.assertEquals(5, lunar.getMonth());
			Assertions.assertEquals(1, lunar.getDay());
			Assertions.assertEquals(true, lunar.isLeap());
			if (lunar == null || lunar.getYear() != 1990 || lunar.getMonth() != 5 || lunar.getDay() != 1
					|| !lunar.isLeap()) {
				System.out.println("solar2Lunar incorrect: solar 1990-6-23 should be lunar 1990-5-1(leap).");
			}
		}

		{
			// test農曆閏四月初一並不存在，是錯誤日子
			Solar solar = LunarUtil.lunar2Solar(1990, 4, 1, true).orElse(null);
			Assertions.assertNull(solar);
			if (solar != null) {
				System.out.println("lunar2Solar incorrect: lunar 1990-4-1(leap) should be invalid input(wrong leap).");
			}
		}

		{
			// test農曆閏六月三十日->西曆2017-8-21
			Solar solar = LunarUtil.lunar2Solar(2017, 6, 30, true).orElse(null);
			Assertions.assertNotNull(solar);
			Assertions.assertEquals(2017, solar.getYear());
			Assertions.assertEquals(8, solar.getMonth());
			Assertions.assertEquals(21, solar.getDay());
			if (solar == null || solar.getYear() != 2017 || solar.getMonth() != 8 || solar.getDay() != 21) {
				System.out.println("lunar2Solar incorrect: lunar 2017-6-30(leap) should be solar 2017-8-21.");
			}
		}

		{
			// test西曆2017-8-15->農曆閏六月廿四日
			Lunar lunar = LunarUtil.solar2Lunar(2017, 8, 15).orElse(null);
			Assertions.assertNotNull(lunar);
			Assertions.assertEquals(2017, lunar.getYear());
			Assertions.assertEquals(6, lunar.getMonth());
			Assertions.assertEquals(24, lunar.getDay());
			Assertions.assertEquals(true, lunar.isLeap());
			if (lunar == null || lunar.getYear() != 2017 || lunar.getMonth() != 6 || lunar.getDay() != 24
					|| !lunar.isLeap()) {
				System.out.println("solar2Lunar incorrect: solar 2017-8-15 should be lunar 2017-6-24(leap).");
			}
		}

		{
			// test西曆2033-8-25->農曆八月初一，測試2033置閏問題
			Lunar lunar = LunarUtil.solar2Lunar(2033, 8, 25).orElse(null);
			Assertions.assertNotNull(lunar);
			Assertions.assertEquals(2033, lunar.getYear());
			Assertions.assertEquals(8, lunar.getMonth());
			Assertions.assertEquals(1, lunar.getDay());
			Assertions.assertEquals(false, lunar.isLeap());
			if (lunar == null || lunar.getYear() != 2033 || lunar.getMonth() != 8 || lunar.getDay() != 1
					|| lunar.isLeap()) {
				System.out.println(
						"solar2Lunar incorrect: solar 2033-8-25 should be lunar 2033-8-1 instead of lunar 2033-7-1(leap)");
			}
		}

		{
			// test西曆2033-12-22->農曆閨十一月初一，測試2033置閏問題
			Lunar lunar = LunarUtil.solar2Lunar(2033, 12, 22).orElse(null);
			Assertions.assertNotNull(lunar);
			Assertions.assertEquals(2033, lunar.getYear());
			Assertions.assertEquals(11, lunar.getMonth());
			Assertions.assertEquals(1, lunar.getDay());
			Assertions.assertEquals(true, lunar.isLeap());
			if (lunar == null || lunar.getYear() != 2033 || lunar.getMonth() != 11 || lunar.getDay() != 1
					|| !lunar.isLeap()) {
				System.out.println(
						"solar2Lunar incorrect: solar 2033-12-22 should be lunar 2033-11-1(leap) instead of lunar 2033-11-1");
			}
		}

		System.out.println("test LunarUtil Finished.");
	}
}
