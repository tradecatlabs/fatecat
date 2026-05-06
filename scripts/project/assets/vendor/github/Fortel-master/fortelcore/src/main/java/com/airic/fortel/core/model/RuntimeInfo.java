package com.airic.fortel.core.model;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

import org.joda.time.DateTime;
import org.joda.time.DateTimeZone;
import org.joda.time.Duration;

import com.airic.fortel.core.calendar.util.Lunar;
import com.airic.fortel.core.calendar.util.LunarUtil;
import com.airic.fortel.core.calendar.util.Solar;
import com.airic.fortel.core.util.CommonUtil;

/**
 * The Class RuntimeInfo.
 */
public class RuntimeInfo implements Serializable {

	/** The Constant serialVersionUID. */
	private static final long serialVersionUID = 7575181113448042752L;

	/**
	 * The Enum RuntimeCategory.
	 */
	public static enum RuntimeCategory {

		/** The ten year. */
		TEN_YEAR,
		/** The year. */
		YEAR,
		/** The month. */
		MONTH,
		/** The day. */
		DAY
	}

	/** The runtime star reaction map. */
	private Map<StarReaction, Star> runtimeStarReactionMap = new HashMap<StarReaction, Star>();

	/** The runtime minor stars map. */
	private Map<MinorStar, Ground> runtimeMinorStarsMap = new HashMap<MinorStar, Ground>();

	/** The runtime destiny temple ground. */
	private Ground runtimeDestinyTempleGround = null;

	/**
	 * Instantiates a new runtime info.
	 */
	public RuntimeInfo() {
	}

	/**
	 * Gets the runtime star reaction map.
	 *
	 * @return the runtime star reaction map
	 */
	public Map<StarReaction, Star> getRuntimeStarReactionMap() {
		return runtimeStarReactionMap;
	}

	/**
	 * Sets the runtime star reaction map.
	 *
	 * @param runtimeStarReactionMap
	 *            the runtime star reaction map
	 */
	public void setRuntimeStarReactionMap(Map<StarReaction, Star> runtimeStarReactionMap) {
		this.runtimeStarReactionMap = runtimeStarReactionMap;
	}

	/**
	 * Gets the runtime minor stars map.
	 *
	 * @return the runtime minor stars map
	 */
	public Map<MinorStar, Ground> getRuntimeMinorStarsMap() {
		return runtimeMinorStarsMap;
	}

	/**
	 * Sets the runtime minor stars map.
	 *
	 * @param runtimeMinorStarsMap
	 *            the runtime minor stars map
	 */
	public void setRuntimeMinorStarsMap(Map<MinorStar, Ground> runtimeMinorStarsMap) {
		this.runtimeMinorStarsMap = runtimeMinorStarsMap;
	}

	/**
	 * Gets the runtime destiny temple ground.
	 *
	 * @return the runtime destiny temple ground
	 */
	public Ground getRuntimeDestinyTempleGround() {
		return runtimeDestinyTempleGround;
	}

	/**
	 * Sets the runtime destiny temple ground.
	 *
	 * @param runtimeDestinyTempleGround
	 *            the new runtime destiny temple ground
	 */
	public void setRuntimeDestinyTempleGround(Ground runtimeDestinyTempleGround) {
		this.runtimeDestinyTempleGround = runtimeDestinyTempleGround;
	}

	/**
	 * Prepare runtime star star reaction info.
	 *
	 * @param sky
	 *            the sky
	 * @param ground
	 *            the ground
	 * @return the runtime info
	 */
	private static RuntimeInfo prepareRuntimeStarStarReactionInfo(Sky sky, Ground ground) {
		RuntimeInfo runtimeInfo = new RuntimeInfo();
		for (MinorStar star : Data.RUNTIME_MINOR_STARS) {
			if (star != MinorStar.MINOR_STAR_HORSE_CHANGE) {
				runtimeInfo.getRuntimeMinorStarsMap().put(star, star.getRuntimeGroundBySky(sky));
			} else {
				runtimeInfo.getRuntimeMinorStarsMap().put(MinorStar.MINOR_STAR_HORSE_CHANGE,
						MinorStar.getHorseChangeRuntimeGroundByGround(ground));
			}
		}

		runtimeInfo.getRuntimeStarReactionMap().put(StarReaction.STAR_TO_TREASURE,
				StarReaction.getStarReactionTreasureStar(sky));
		runtimeInfo.getRuntimeStarReactionMap().put(StarReaction.STAR_TO_POWER,
				StarReaction.getStarReactionPowerStar(sky));
		runtimeInfo.getRuntimeStarReactionMap().put(StarReaction.STAR_TO_POSITION,
				StarReaction.getStarReactionPositionStar(sky));
		runtimeInfo.getRuntimeStarReactionMap().put(StarReaction.STAR_TO_PROBLEM,
				StarReaction.getStarReactionProblemStar(sky));

		return runtimeInfo;
	}

	/**
	 * Gets the runtime info map.
	 *
	 * @param destiny
	 *            the destiny
	 * @param lunar
	 *            the lunar
	 * @return the runtime info map
	 */
	public static Map<RuntimeCategory, RuntimeInfo> getRuntimeInfoMap(Destiny destiny, Lunar lunar) {
		Map<RuntimeCategory, RuntimeInfo> runtimeInfoMap = new HashMap<RuntimeCategory, RuntimeInfo>();

		int runtimeEffectiveMonth = (lunar.isLeap() && lunar.getDay() > 15) ? lunar.getMonth() + 1 : lunar.getMonth();

		Cell tenYearCell = getTenYearCell(destiny, lunar);
		Sky tenYearSky = tenYearCell.getSky();// 十年大運天干
		Ground tenYearGround = tenYearCell.getGround();// 十年大運地支
		Sky yearSky = Sky.getByIndex(CommonUtil.mod(lunar.getYear() % 60 - 4, 60) % 10);// 流年天干
		Ground yearGround = Ground.getByIndex(CommonUtil.mod(lunar.getYear() % 60 - 4, 60) % 12);// 流年地支
		Sky monthSky = Sky.getByIndex((yearSky.getIndex() % 5 + 1) * 2 + (runtimeEffectiveMonth - 1));// 流月天干
		Ground monthGround = Ground.getByIndex((runtimeEffectiveMonth + 1) % 12);
		Sky daySky = null;// 流日天干
		Ground dayGround = null;// 流日地支

		// get流日天干
		Optional<Solar> solarOptional = LunarUtil.lunar2Solar(lunar.getYear(), lunar.getMonth(), lunar.getDay(),
				lunar.isLeap());
		if (solarOptional.isPresent()) {
			Solar solar = solarOptional.get();
			DateTime solarDate = new DateTime(solar.getYear(), solar.getMonth(), solar.getDay(), 0, 0, 0,
					DateTimeZone.forID("UTC"));
			DateTime refSolarDate = new DateTime(1900, 1, 31, 0, 0, 0, DateTimeZone.forID("UTC"));
			Duration dur = new Duration(refSolarDate, solarDate);
			daySky = Sky.getByIndex((int) ((dur.getStandardDays()) % 10));
			dayGround = Ground.getByIndex((int) ((dur.getStandardDays() + 4) % 12));
		}

		RuntimeInfo tenYearRuntime = prepareRuntimeStarStarReactionInfo(tenYearSky, tenYearGround);
		tenYearRuntime.setRuntimeDestinyTempleGround(tenYearCell.getGround());

		RuntimeInfo yearRuntime = prepareRuntimeStarStarReactionInfo(yearSky, yearGround);
		yearRuntime.setRuntimeDestinyTempleGround(yearGround);

		RuntimeInfo monthRuntime = prepareRuntimeStarStarReactionInfo(monthSky, monthGround);
		int monthRuntimeDestinyCellGroundIndex = ((destiny.getSonDou().getIndex() + yearGround.getIndex()) % 12
				+ runtimeEffectiveMonth - 1) % 12;
		monthRuntime.setRuntimeDestinyTempleGround(Ground.getByIndex(monthRuntimeDestinyCellGroundIndex));

		RuntimeInfo dayRuntime = prepareRuntimeStarStarReactionInfo(daySky, dayGround);
		int dayRuntimeDestinyCellGroundIndex = (monthRuntimeDestinyCellGroundIndex + lunar.getDay() - 1) % 12;
		if (lunar.isLeap() && lunar.getDay() <= 15) {
			int prevMonthDays = LunarUtil.getPrevLunar(lunar.getYear(), lunar.getMonth(), 1, true).get().getDay();
			dayRuntimeDestinyCellGroundIndex = (monthRuntimeDestinyCellGroundIndex + prevMonthDays - 1 + lunar.getDay())
					% 12;
		} else if (lunar.isLeap() && lunar.getDay() > 15) {
			dayRuntimeDestinyCellGroundIndex = (monthRuntimeDestinyCellGroundIndex + lunar.getDay() - 15 - 1) % 12;
		}
		dayRuntime.setRuntimeDestinyTempleGround(Ground.getByIndex(dayRuntimeDestinyCellGroundIndex));

		runtimeInfoMap.put(RuntimeCategory.TEN_YEAR, tenYearRuntime);
		runtimeInfoMap.put(RuntimeCategory.YEAR, yearRuntime);
		runtimeInfoMap.put(RuntimeCategory.MONTH, monthRuntime);
		runtimeInfoMap.put(RuntimeCategory.DAY, dayRuntime);

		return runtimeInfoMap;
	}

	// TODO better algorithm
	/**
	 * Gets the ten year cell.
	 *
	 * @param destiny
	 *            the destiny
	 * @param lunar
	 *            the lunar
	 * @return the ten year cell
	 */
	private static Cell getTenYearCell(Destiny destiny, Lunar lunar) {
		int age = lunar.getYear() - destiny.getConfig().getBornYear() + 1;
		Cell targetCell = null;
		for (int i = 0; i < destiny.getAgeStartIndexedCells().size(); i++) {
			Cell nextCell = destiny.getAgeStartIndexedCells().get(i);
			if (nextCell != null && age <= nextCell.getAgeEnd()) {
				targetCell = nextCell;
				break;
			}
		}
		// he may be too old, we don't handle this case
		return targetCell;
	}

}
