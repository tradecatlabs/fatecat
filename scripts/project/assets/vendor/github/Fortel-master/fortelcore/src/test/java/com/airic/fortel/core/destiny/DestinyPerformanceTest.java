package com.airic.fortel.core.destiny;

import java.util.Arrays;
import java.util.Optional;

import com.airic.fortel.core.destiny.config.Config;
import com.airic.fortel.core.destiny.config.Config.ConfigType;
import com.airic.fortel.core.destiny.pattern.impl.DummyPatternChecker;
import com.airic.fortel.core.destiny.visitor.DestinyPatternCheckAgent;
import com.airic.fortel.core.destiny.visitor.DestinyPatterns;
import com.airic.fortel.core.model.Data.GroundTime;
import com.airic.fortel.core.model.Data.Sex;
import com.airic.fortel.core.model.Destiny;

/**
 * The Class AppTest.
 */
public class DestinyPerformanceTest {

	/**
	 * The main method.
	 *
	 * @param args the arguments
	 */
	public static void main(String[] args) {
		DestinyPerformanceTest test = new DestinyPerformanceTest();
		test.testAllConfig();
	}

	/**
	 * Test all config.
	 */
	public void testAllConfig() {
		Config initConfig = new Config(ConfigType.SKY, Sex.M, 1900, 1, 1, false, GroundTime.GROUND_0);
		testAllConfigUntil(initConfig, 2048, 12, 30, false, GroundTime.GROUND_12);
	}

	/**
	 * Test all config until.
	 *
	 * @param initConfig the init config
	 * @param endYear the end year
	 * @param endMonth the end month
	 * @param endDay the end day
	 * @param endMonthIsDoubleMonth the end month is double month
	 * @param endGroundTime the end ground time
	 */
	private static void testAllConfigUntil(Config initConfig, int endYear, int endMonth, int endDay,
			boolean endMonthIsDoubleMonth, GroundTime endGroundTime) {
		boolean done = false;
		Config currentConfig = initConfig;
		Destiny destiny = null;
		int count = 0;
		long startTime = System.currentTimeMillis();

		while (!done) {
			count++;
			destiny = new Destiny(currentConfig);

			DestinyPatterns destinyPatterns = DestinyPatternCheckAgent.checkDestiny(destiny,
					Arrays.asList(new DummyPatternChecker()));
			// List<Pattern> formations = destinyPatterns.getPatterns(FormationPatternType.getInstance());
			// List<Pattern> characteristics =
			// destinyPatterns.getPatterns(GeneralCharacteristicPatternType.getInstance());

			Optional<Config> currentConfigOptional = currentConfig.getNextConfig();
			if (!currentConfigOptional.isPresent()) {
				done = true;
			} else {
				currentConfig = currentConfigOptional.get();
				if (!testDateInRange(currentConfig.getBornYear(), currentConfig.getBornMonth(),
						currentConfig.getBornDay(), currentConfig.isDoubleMonth(), currentConfig.getBornTimeGround(),
						endYear, endMonth, endDay, endMonthIsDoubleMonth, endGroundTime)) {
					done = true;
				}
			}
		}
		long endTime = System.currentTimeMillis();

		System.out.println(String.format("Total destiny config: %d", count));
		System.out.println(String.format("Total time: %.2f s", (endTime - startTime) / 1000D));
		System.out.println(String.format("Average time: %.6f s", (endTime - startTime) / 1000D / (double) count));
	}

	/**
	 * Test date in range.
	 *
	 * @param year the year
	 * @param month the month
	 * @param day the day
	 * @param isDoubleMonth the is double month
	 * @param groundTime the ground time
	 * @param endYear the end year
	 * @param endMonth the end month
	 * @param endDay the end day
	 * @param endIsDoubleMonth the end is double month
	 * @param endGroundTime the end ground time
	 * @return true, if successful
	 */
	private static boolean testDateInRange(int year, int month, int day, boolean isDoubleMonth, GroundTime groundTime,
			int endYear, int endMonth, int endDay, boolean endIsDoubleMonth, GroundTime endGroundTime) {
		float effectiveMonth = month + (isDoubleMonth ? 0.5f : 0);
		float effectiveEndMonth = endMonth + (endIsDoubleMonth ? 0.5f : 0);

		if (year > endYear) {
			return false;
		} else if (year == endYear) {
			if (effectiveMonth > effectiveEndMonth) {
				return false;
			} else if (effectiveMonth == effectiveEndMonth) {
				if (day > endDay) {
					return false;
				} else if (day == endDay) {
					if (groundTime.getIndex() > endGroundTime.getIndex()) {
						return false;
					}
				}
			}
		}

		return true;
	}

}
