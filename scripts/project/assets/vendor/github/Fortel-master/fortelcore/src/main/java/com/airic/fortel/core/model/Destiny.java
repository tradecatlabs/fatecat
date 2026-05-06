package com.airic.fortel.core.model;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;

import org.joda.time.DateTime;
import org.joda.time.DateTimeZone;
import org.joda.time.Duration;

import com.airic.fortel.core.calendar.util.Lunar;
import com.airic.fortel.core.calendar.util.LunarUtil;
import com.airic.fortel.core.calendar.util.Solar;
import com.airic.fortel.core.destiny.config.Config;
import com.airic.fortel.core.model.Data.Direction;
import com.airic.fortel.core.model.Data.FiveElement;
import com.airic.fortel.core.model.Data.Sex;
import com.airic.fortel.core.model.Data.ShadowLight;
import com.airic.fortel.core.model.Data.StarEnergyLevel;
import com.airic.fortel.core.util.CommonUtil;
import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonAutoDetect.Visibility;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * The Class Destiny.
 */
@JsonAutoDetect(getterVisibility = Visibility.ANY, isGetterVisibility = Visibility.NONE, setterVisibility = Visibility.NONE, creatorVisibility = Visibility.NONE, fieldVisibility = Visibility.NONE)
public final class Destiny implements Serializable {

	/** The Constant serialVersionUID. */
	private static final long serialVersionUID = 5645150155960144003L;

	/** The config. */
	private Config config = null;

	/** The shadow light. */
	private ShadowLight shadowLight = null;

	/** The five element. */
	private FiveElement fiveElement = null;

	/** The cells. */
	private List<Cell> cells = new ArrayList<Cell>();

	/** The star reaction map. */
	private Map<StarReaction, Star> starReactionMap = new HashMap<StarReaction, Star>();

	/** The major star energy. */
	private Map<MajorStar, StarEnergyLevel> majorStarEnergy = new HashMap<MajorStar, StarEnergyLevel>();

	/** The destiny master. */
	private Star destinyMaster = null;

	/** The body master. */
	private Star bodyMaster = null;

	/** The son dou. */
	private Ground sonDou;// 子斗

	/** The path clockwise. */
	private boolean pathClockwise;

	/** The ground to cell map. */
	protected transient Map<Ground, Cell> groundToCellMap = new HashMap<Ground, Cell>();

	/** The temple to cell map. */
	protected transient Map<Temple, Cell> templeToCellMap = new HashMap<Temple, Cell>();

	/** The star to cell map. */
	protected transient Map<Star, Cell> starToCellMap = new HashMap<Star, Cell>();

	/** The age start indexed cells. */
	private transient List<Cell> ageStartIndexedCells = new ArrayList<Cell>();

	/** The Constant ABLE_REACTION_STARS_SET. */
	private static final Set<Star> ABLE_REACTION_STARS_SET = new HashSet<Star>(
			Arrays.asList(MajorStar.MAJOR_STAR_EMPEROR, MajorStar.MAJOR_STAR_COUNSELLOR, MajorStar.MAJOR_STAR_SUN,
					MajorStar.MAJOR_STAR_MONEY, MajorStar.MAJOR_STAR_RECREATION, MajorStar.MAJOR_STAR_HONEST,
					MajorStar.MAJOR_STAR_TREASURY, MajorStar.MAJOR_STAR_MOON, MajorStar.MAJOR_STAR_GREED,
					MajorStar.MAJOR_STAR_MOUTH, MajorStar.MAJOR_STAR_LAW, MajorStar.MAJOR_STAR_SOLDIER,
					MinorStar.MINOR_STAR_CLEVER, MinorStar.MINOR_STAR_SKILL));

	/**
	 * Instantiates a new destiny.
	 *
	 * @param config
	 *            the config
	 */
	public Destiny(Config config) {
		this.config = config;
		this.setShadowLight((config.getYearSky().getIndex() % 2 == 0) ? ShadowLight.LIGHT : ShadowLight.SHADOW);

		setupDestiny();
	}

	/**
	 * Inits the temple cells.
	 */
	private void setupDestiny() {
		DestinyBuilder.setupBasicTempleCells(config, cells, groundToCellMap);
		DestinyBuilder.setupTemples(config, templeToCellMap, groundToCellMap);
		DestinyBuilder.setupFiveElement(this);
		DestinyBuilder.setupAgeRange(this, ageStartIndexedCells);
		DestinyBuilder.setupMajorStars(this, starToCellMap, majorStarEnergy);
		DestinyBuilder.setupStars(this, starToCellMap);
		DestinyBuilder.setupStarReactions(this, starReactionMap);
		DestinyBuilder.setupBrowserCells(this);
		DestinyBuilder.setupSonDou(this);
		DestinyBuilder.setupDestinyBodyMaster(this);
		DestinyBuilder.setupPathClockwise(this);
	}

	/**
	 * Gets the config.
	 *
	 * @return the config
	 */
	public Config getConfig() {
		return config;
	}

	/**
	 * Sets the config.
	 *
	 * @param config
	 *            the new config
	 */
	public void setConfig(Config config) {
		this.config = config;
	}

	/**
	 * Gets the shadow light.
	 *
	 * @return the shadow light
	 */
	public ShadowLight getShadowLight() {
		return shadowLight;
	}

	/**
	 * Sets the shadow light.
	 *
	 * @param shadowLight
	 *            the new shadow light
	 */
	public void setShadowLight(ShadowLight shadowLight) {
		this.shadowLight = shadowLight;
	}

	/**
	 * Gets the five element.
	 *
	 * @return the five element
	 */
	public FiveElement getFiveElement() {
		return fiveElement;
	}

	/**
	 * Sets the five element.
	 *
	 * @param fiveElement
	 *            the new five element
	 */
	public void setFiveElement(FiveElement fiveElement) {
		this.fiveElement = fiveElement;
	}

	/**
	 * Gets the destiny master.
	 *
	 * @return the destiny master
	 */
	public Star getDestinyMaster() {
		return destinyMaster;
	}

	/**
	 * Sets the destiny master.
	 *
	 * @param destinyMaster
	 *            the new destiny master
	 */
	public void setDestinyMaster(Star destinyMaster) {
		this.destinyMaster = destinyMaster;
	}

	/**
	 * Gets the body master.
	 *
	 * @return the body master
	 */
	public Star getBodyMaster() {
		return bodyMaster;
	}

	/**
	 * Sets the body master.
	 *
	 * @param bodyMaster
	 *            the new body master
	 */
	public void setBodyMaster(Star bodyMaster) {
		this.bodyMaster = bodyMaster;
	}

	/**
	 * Gets the son dou.
	 *
	 * @return the son dou
	 */
	public Ground getSonDou() {
		return sonDou;
	}

	/**
	 * Sets the son dou.
	 *
	 * @param sonDou
	 *            the new son dou
	 */
	public void setSonDou(Ground sonDou) {
		this.sonDou = sonDou;
	}

	/**
	 * Checks if is path clockwise.
	 *
	 * @return true, if is path clockwise
	 */
	public boolean isPathClockwise() {
		return pathClockwise;
	}

	/**
	 * Sets the path clockwise.
	 *
	 * @param pathClockwise
	 *            the new path clockwise
	 */
	public void setPathClockwise(boolean pathClockwise) {
		this.pathClockwise = pathClockwise;
	}

	/**
	 * Gets the cells.
	 *
	 * @return the cells
	 */
	public List<Cell> getCells() {
		return cells;
	}

	/**
	 * Gets the cell index.
	 *
	 * @param cell
	 *            the cell
	 * @return the cell index
	 */
	@JsonIgnore
	public int getCellIndex(Cell cell) {
		if (cell != null) {
			for (int i = 0; i < cells.size(); i++) {
				if (cells.get(i).getGround() == cell.getGround()) {
					return i;
				}
			}
		}
		return -1;
	}

	/**
	 * Gets the ground cell.
	 *
	 * @param ground
	 *            the ground
	 * @return the ground cell
	 */
	@JsonIgnore
	public Cell getGroundCell(Ground ground) {
		return this.groundToCellMap.get(ground);
	}

	/**
	 * Gets the temple cell.
	 *
	 * @param temple
	 *            the temple
	 * @return the temple cell
	 */
	@JsonIgnore
	public Cell getTempleCell(Temple temple) {
		return this.templeToCellMap.get(temple);
	}

	/**
	 * Gets the star cell.
	 *
	 * @param star
	 *            the star
	 * @return the star cell
	 */
	@JsonIgnore
	public Cell getStarCell(Star star) {
		return this.starToCellMap.get(star);
	}

	/**
	 * Gets the star temples.
	 *
	 * @param star
	 *            the star
	 * @return the star temples
	 */
	@JsonIgnore
	public List<Temple> getStarTemples(Star star) {
		return this.getStarCell(star).getTemples();
	}

	/**
	 * Gets the reaction star.
	 *
	 * @param starReaction
	 *            the star reaction
	 * @return the reaction star
	 */
	@JsonIgnore
	public Star getReactionStar(StarReaction starReaction) {
		return this.starReactionMap.get(starReaction);
	}

	/**
	 * Gets the reaction cell.
	 *
	 * @param starReaction
	 *            the star reaction
	 * @return the reaction cell
	 */
	@JsonIgnore
	public Cell getReactionCell(StarReaction starReaction) {
		return this.getStarCell(this.starReactionMap.get(starReaction));
	}

	/**
	 * Gets the star level.
	 *
	 * @param majorStar
	 *            the major star
	 * @return the star level
	 */
	@JsonIgnore
	public StarEnergyLevel getStarLevel(MajorStar majorStar) {
		return majorStarEnergy.get(majorStar);
	}

	@Override
	public String toString() {
		return "Destiny [config=" + config + ", shadowLight=" + shadowLight + ", fiveElement=" + fiveElement
				+ ", cells=" + cells + ", starReactionMap=" + starReactionMap + ", majorStarEnergy=" + majorStarEnergy
				+ ", destinyMaster=" + destinyMaster + ", bodyMaster=" + bodyMaster + ", sonDou=" + sonDou
				+ ", pathClockwise=" + pathClockwise + "]";
	}
	
	public String toJsonString() {
		try {
			return new ObjectMapper().writeValueAsString(this);
		} catch (JsonProcessingException e) {
			e.printStackTrace();
		}
		
		return "";
	}

	/**
	 * Gets the ten year runtime cell ground sequence.
	 *
	 * @return the ten year runtime cell ground sequence
	 */
	@JsonIgnore
	public List<Ground> getTenYearRuntimeCellGroundSequence() {
		List<Ground> groundSeq = new ArrayList<Ground>();
		Cell currentCell = this.getTempleCell(Temple.TEMPLE_DESTINY);

		// 陽男陰女順行
		int vector = this.getShadowLight() == ShadowLight.LIGHT ? 1 : -1;
		vector *= this.getConfig().getSex() == Sex.M ? 1 : -1;
		Direction direction = vector == 1 ? Direction.CLOCKWISE : Direction.ANTICLOCKWISE;

		for (int i = 0; i < Ground.COUNT; i++) {
			groundSeq.add(currentCell.getGround());
			if (direction == Direction.CLOCKWISE) {
				currentCell = currentCell.getNextCell();
			} else {
				currentCell = currentCell.getPrevCell();
			}
		}

		return groundSeq;
	}

	/** The Constant TEN_YEAR_RUNTIME. */
	public static final String TEN_YEAR_RUNTIME = "TEN_YEAR_RUNTIME";

	/** The Constant YEAR_RUNTIME. */
	public static final String YEAR_RUNTIME = "YEAR_RUNTIME";

	/** The Constant MONTH_RUNTIME. */
	public static final String MONTH_RUNTIME = "MONTH_RUNTIME";

	/** The Constant DAY_RUNTIME. */
	public static final String DAY_RUNTIME = "DAY_RUNTIME";

	/**
	 * Gets the runtime minor stars map.
	 *
	 * @param lunar
	 *            the lunar
	 * @return the runtime minor stars map
	 */
	@JsonIgnore
	public Map<String, Map<MinorStar, Ground>> getRuntimeMinorStarsMap(Lunar lunar) {
		Map<String, Map<MinorStar, Ground>> runtimeMinorStarMap = new HashMap<String, Map<MinorStar, Ground>>();

		Map<MinorStar, Ground> tenYearRuntimeMinorStarMap = new HashMap<MinorStar, Ground>();
		Map<MinorStar, Ground> yearRuntimeMinorStarMap = new HashMap<MinorStar, Ground>();
		Map<MinorStar, Ground> monthRuntimeMinorStarMap = new HashMap<MinorStar, Ground>();
		Map<MinorStar, Ground> dayRuntimeMinorStarMap = new HashMap<MinorStar, Ground>();

		runtimeMinorStarMap.put(TEN_YEAR_RUNTIME, tenYearRuntimeMinorStarMap);
		runtimeMinorStarMap.put(YEAR_RUNTIME, yearRuntimeMinorStarMap);
		runtimeMinorStarMap.put(MONTH_RUNTIME, monthRuntimeMinorStarMap);
		runtimeMinorStarMap.put(DAY_RUNTIME, dayRuntimeMinorStarMap);

		Sky tenYearSky = getTenYearSky(lunar);// 十年大運天干
		Sky yearSky = Sky.getByIndex(CommonUtil.mod(lunar.getYear() % 60 - 4, 60) % 10);// 流年天干
		Sky monthSky = Sky.getByIndex((yearSky.getIndex() % 5 + 1) * 2 + (lunar.getEffectiveMonth() - 1)
				+ (lunar.isLeap() && lunar.getDay() > 15 ? 1 : 0));// 流月天干
		Sky daySky = null;// 流日天干

		// get流日天干
		Optional<Solar> solarOptional = LunarUtil.lunar2Solar(lunar.getYear(), lunar.getMonth(), lunar.getDay(),
				lunar.isLeap());
		if (solarOptional.isPresent()) {
			Solar solar = solarOptional.get();
			DateTime solarDate = new DateTime(solar.getYear(), solar.getMonth(), solar.getDay(), 0, 0, 0,
					DateTimeZone.forID("UTC"));
			DateTime refSolarDate = new DateTime(1900, 1, 31, 0, 0, 0, DateTimeZone.forID("UTC"));
			Duration dur = new Duration(refSolarDate, solarDate);
			int index = (int) (dur.getStandardDays() % 10);
			if (index > 0) {
				daySky = Sky.getByIndex(index);
			}
		}

		MinorStar[] runtimeMinorStars = new MinorStar[] { MinorStar.MINOR_STAR_CLOTH, MinorStar.MINOR_STAR_FAILURE,
				MinorStar.MINOR_STAR_HINDER, MinorStar.MINOR_STAR_HONOR, MinorStar.MINOR_STAR_HONOR2,
				MinorStar.MINOR_STAR_CLEVER, MinorStar.MINOR_STAR_SKILL };

		for (MinorStar minorStar : runtimeMinorStars) {
			if (tenYearSky != null) {
				tenYearRuntimeMinorStarMap.put(minorStar, minorStar.getRuntimeGroundBySky(tenYearSky));
			}
			if (yearSky != null) {
				yearRuntimeMinorStarMap.put(minorStar, minorStar.getRuntimeGroundBySky(yearSky));
			}
			if (monthSky != null) {
				monthRuntimeMinorStarMap.put(minorStar, minorStar.getRuntimeGroundBySky(monthSky));
			}
			if (daySky != null) {
				dayRuntimeMinorStarMap.put(minorStar, minorStar.getRuntimeGroundBySky(daySky));
			}
		}

		return runtimeMinorStarMap;
	}

	/**
	 * Gets the ten year sky.
	 *
	 * @param lunar
	 *            the lunar
	 * @return the ten year sky
	 */
	@JsonIgnore
	private Sky getTenYearSky(Lunar lunar) {
		Sky tenYearSky = null;// 十年大運天干
		// get十年大運天干
		int age = lunar.getYear() - this.config.getBornYear() + 1;
		Cell targetCell = null;
		for (int i = 0; i < ageStartIndexedCells.size(); i++) {
			Cell nextCell = ageStartIndexedCells.get(i);
			if (nextCell != null && age <= nextCell.getAgeEnd()) {
				targetCell = nextCell;
				break;
			}
		}
		// he may be too old, we don't handle this case
		if (targetCell != null) {
			tenYearSky = targetCell.getSky();
		}

		return tenYearSky;
	}

	/**
	 * Gets the runtime star reaction map.
	 *
	 * @param lunar
	 *            the lunar
	 * @return the runtime star reaction map
	 */
	@JsonIgnore
	public Map<String, Map<StarReaction, Star>> getRuntimeStarReactionMap(Lunar lunar) {

		Map<String, Map<StarReaction, Star>> runtimeStarReactionMap = new HashMap<String, Map<StarReaction, Star>>();

		Map<StarReaction, Star> tenYearRuntimeStarReactionMap = new HashMap<StarReaction, Star>();
		Map<StarReaction, Star> yearRuntimeStarReactionMap = new HashMap<StarReaction, Star>();
		Map<StarReaction, Star> monthRuntimeStarReactionMap = new HashMap<StarReaction, Star>();
		Map<StarReaction, Star> dayRuntimeStarReactionMap = new HashMap<StarReaction, Star>();

		runtimeStarReactionMap.put(TEN_YEAR_RUNTIME, tenYearRuntimeStarReactionMap);
		runtimeStarReactionMap.put(YEAR_RUNTIME, yearRuntimeStarReactionMap);
		runtimeStarReactionMap.put(MONTH_RUNTIME, monthRuntimeStarReactionMap);
		runtimeStarReactionMap.put(DAY_RUNTIME, dayRuntimeStarReactionMap);

		Sky tenYearSky = getTenYearSky(lunar);// 十年大運天干
		Sky yearSky = Sky.getByIndex(CommonUtil.mod(lunar.getYear() % 60 - 4, 60) % 10);// 流年天干
		Sky monthSky = Sky.getByIndex((yearSky.getIndex() % 5 + 1) * 2 + (lunar.getMonth() - 1)
				+ (lunar.isLeap() && lunar.getDay() > 15 ? 1 : 0));// 流月天干
		Sky daySky = null;// 流日天干

		// get流日天干
		Optional<Solar> solarOptional = LunarUtil.lunar2Solar(lunar.getYear(), lunar.getMonth(), lunar.getDay(),
				lunar.isLeap());
		if (solarOptional.isPresent()) {
			Solar solar = solarOptional.get();
			DateTime solarDate = new DateTime(solar.getYear(), solar.getMonth(), solar.getDay(), 0, 0, 0,
					DateTimeZone.forID("UTC"));
			DateTime refSolarDate = new DateTime(1900, 1, 31, 0, 0, 0, DateTimeZone.forID("UTC"));
			Duration dur = new Duration(refSolarDate, solarDate);
			int index = (int) (dur.getStandardDays() % 10);
			if (index >= 0) {
				daySky = Sky.getByIndex(index);
			}
		}

		// 十年大運四化
		if (tenYearSky != null) {
			Sky sky = tenYearSky;
			Map<StarReaction, Star> runtimeMap = tenYearRuntimeStarReactionMap;
			runtimeMap.put(StarReaction.STAR_TO_TREASURE, StarReaction.getStarReactionTreasureStar(sky));
			runtimeMap.put(StarReaction.STAR_TO_POWER, StarReaction.getStarReactionPowerStar(sky));
			runtimeMap.put(StarReaction.STAR_TO_POSITION, StarReaction.getStarReactionPositionStar(sky));
			runtimeMap.put(StarReaction.STAR_TO_PROBLEM, StarReaction.getStarReactionProblemStar(sky));
		}

		// 流年四化
		if (yearSky != null) {
			Sky sky = yearSky;
			Map<StarReaction, Star> runtimeMap = yearRuntimeStarReactionMap;
			runtimeMap.put(StarReaction.STAR_TO_TREASURE, StarReaction.getStarReactionTreasureStar(sky));
			runtimeMap.put(StarReaction.STAR_TO_POWER, StarReaction.getStarReactionPowerStar(sky));
			runtimeMap.put(StarReaction.STAR_TO_POSITION, StarReaction.getStarReactionPositionStar(sky));
			runtimeMap.put(StarReaction.STAR_TO_PROBLEM, StarReaction.getStarReactionProblemStar(sky));
		}

		// 流月四化
		if (monthSky != null) {
			Sky sky = monthSky;
			Map<StarReaction, Star> runtimeMap = monthRuntimeStarReactionMap;
			runtimeMap.put(StarReaction.STAR_TO_TREASURE, StarReaction.getStarReactionTreasureStar(sky));
			runtimeMap.put(StarReaction.STAR_TO_POWER, StarReaction.getStarReactionPowerStar(sky));
			runtimeMap.put(StarReaction.STAR_TO_POSITION, StarReaction.getStarReactionPositionStar(sky));
			runtimeMap.put(StarReaction.STAR_TO_PROBLEM, StarReaction.getStarReactionProblemStar(sky));
		}

		// 流日四化
		if (daySky != null) {
			Sky sky = daySky;
			Map<StarReaction, Star> runtimeMap = dayRuntimeStarReactionMap;
			runtimeMap.put(StarReaction.STAR_TO_TREASURE, StarReaction.getStarReactionTreasureStar(sky));
			runtimeMap.put(StarReaction.STAR_TO_POWER, StarReaction.getStarReactionPowerStar(sky));
			runtimeMap.put(StarReaction.STAR_TO_POSITION, StarReaction.getStarReactionPositionStar(sky));
			runtimeMap.put(StarReaction.STAR_TO_PROBLEM, StarReaction.getStarReactionProblemStar(sky));
		}

		return runtimeStarReactionMap;
	}

	/**
	 * Gets the star reaction.
	 *
	 * @param star
	 *            the star
	 * @return the star reaction
	 */
	@JsonIgnore
	public Optional<StarReaction> getStarReaction(Star star) {
		if (ABLE_REACTION_STARS_SET.contains(star)) {
			for (StarReaction starReaction : StarReaction.values()) {
				if (this.starReactionMap.get(starReaction) == star) {
					return Optional.of(starReaction);
				}
			}
		}
		return Optional.empty();
	}

	/**
	 * Gets the star reaction map.
	 *
	 * @return the star reaction map
	 */
	public Map<StarReaction, Star> getStarReactionMap() {
		return Collections.unmodifiableMap(starReactionMap);
	}

	/**
	 * Gets the major star energy.
	 *
	 * @return the major star energy
	 */
	public Map<MajorStar, StarEnergyLevel> getMajorStarEnergy() {
		return Collections.unmodifiableMap(majorStarEnergy);
	}

	/**
	 * Gets the age start indexed cells.
	 *
	 * @return the age start indexed cells
	 */
	@JsonIgnore
	public List<Cell> getAgeStartIndexedCells() {
		return ageStartIndexedCells;
	}

}
