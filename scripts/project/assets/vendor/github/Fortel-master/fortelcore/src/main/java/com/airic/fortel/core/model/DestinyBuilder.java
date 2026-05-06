package com.airic.fortel.core.model;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.airic.fortel.core.destiny.config.Config;
import com.airic.fortel.core.model.Data.Direction;
import com.airic.fortel.core.model.Data.FiveElement;
import com.airic.fortel.core.model.Data.Sex;
import com.airic.fortel.core.model.Data.ShadowLight;
import com.airic.fortel.core.model.Data.StarEnergyLevel;
import com.airic.fortel.core.util.CommonUtil;
import com.airic.fortel.core.util.CommonUtil.MapWrapper;

/**
 * The Class DestinyBuilder.
 *
 * @author Eric Yu
 */
public final class DestinyBuilder {

	/** The Constant NUM_CELLS. */
	private static final int NUM_CELLS = Data.NUM_CELLS;

	/**
	 * Instantiates a new destiny builder.
	 */
	private DestinyBuilder() {
	}

	/**
	 * Setup basic temple cells.
	 *
	 * @param config
	 *            the config
	 * @param cells
	 *            the cells
	 * @param groundToCellMap
	 *            the ground to cell map
	 */
	public static void setupBasicTempleCells(Config config, List<Cell> cells, Map<Ground, Cell> groundToCellMap) {
		List<Cell> cells_ = new ArrayList<Cell>();
		// init cells
		for (int i = 0; i < NUM_CELLS; i++) {
			Cell cell = new Cell();
			cell.setSky(Sky.getByIndex(config.getYearSky().getIndex() % 5 * 2 + 2 + i));
			cell.setGround(Ground.getByIndex(i + 2));
			cells_.add(cell);
		}
		for (int i = -2; i < -2 + NUM_CELLS; i++) {
			cells.add(cells_.get((i + 12) % 12));
		}
		for (int i = 0; i < NUM_CELLS; i++) {
			cells.get(i).setPrevCell(cells.get(CommonUtil.mod(i - 1, NUM_CELLS)));
			cells.get(i).setNextCell(cells.get((i + 1) % NUM_CELLS));
		}

		// init ground to cell map
		for (Cell cell : cells) {
			groundToCellMap.put(cell.getGround(), cell);
		}
	}

	/**
	 * Setup temples.
	 *
	 * @param config
	 *            the config
	 * @param templeToCellMap
	 *            the temple to cell map
	 * @param groundToCellMap
	 *            the ground to cell map
	 */
	public static void setupTemples(Config config, Map<Temple, Cell> templeToCellMap,
			Map<Ground, Cell> groundToCellMap) {
		templeToCellMap.put(Temple.TEMPLE_BODY, groundToCellMap.get(
				getBodyTempleGround(config.getDoubleMonthLogicalMonth(), config.getBornTimeGround().getGround())));

		// 安命
		switch (config.getConfigType()) {
		case SKY:
			templeToCellMap.put(Temple.TEMPLE_DESTINY,
					groundToCellMap.get(getDestinyTempleGround(config.getDoubleMonthLogicalMonth(),
							config.getBornTimeGround().getGround())));
			break;
		case GROUND:
			templeToCellMap.put(Temple.TEMPLE_DESTINY, templeToCellMap.get(Temple.TEMPLE_BODY));
			break;
		case HUMAN:
			templeToCellMap.put(Temple.TEMPLE_DESTINY,
					groundToCellMap.get(getDestinyTempleGround(config.getDoubleMonthLogicalMonth(),
							config.getBornTimeGround().getGround()).shift(2)));
			break;
		}

		// 以命宮安其他宮
		for (int i = 0; i < Temple.COUNT - 2; i++) {
			templeToCellMap.put(Temple.getByIndex(2 + i),
					groundToCellMap.get(templeToCellMap.get(Temple.TEMPLE_DESTINY).getGround().shift(-1 - i)));
		}

		// update cell temple info
		for (int i = 0; i < Temple.COUNT; i++) {
			Temple temple = Temple.getByIndex(i);
			templeToCellMap.get(temple).getTemples().add(temple);
		}

	}

	/**
	 * Sets the up five element.
	 *
	 * @param destiny
	 *            the new up five element
	 */
	public static void setupFiveElement(Destiny destiny) {
		Cell cell = destiny.getTempleCell(Temple.TEMPLE_DESTINY);
		int skyGroup = cell.getSky().getIndex() / 2;
		int groundGroup = cell.getGround().getIndex() / 2;

		if (skyGroup >= 0 && skyGroup < Sky.COUNT / 2 && groundGroup >= 0 && groundGroup < Ground.COUNT / 2) {
			destiny.setFiveElement(Data.fiveElementMap[skyGroup][groundGroup]);
		}
	}

	/**
	 * Gets the body temple ground.
	 *
	 * @param bornMonth
	 *            the born month
	 * @param bornTimeGround
	 *            the born time ground
	 * @return the body temple ground
	 */
	private static Ground getBodyTempleGround(int bornMonth, Ground bornTimeGround) {
		return bornTimeGround.shift(2 + bornMonth - 1);
	}

	/**
	 * Gets the destiny temple ground.
	 *
	 * @param bornMonth
	 *            the born month
	 * @param bornTimeGround
	 *            the born time ground
	 * @return the destiny temple ground
	 */
	private static Ground getDestinyTempleGround(int bornMonth, Ground bornTimeGround) {
		return Ground.getByIndex(-bornTimeGround.getIndex() + 2 + bornMonth - 1);
	}

	/**
	 * Gets the element to persist12 begin ground.
	 *
	 * @param fiveElement
	 *            the five element
	 * @return the element to persist12 begin ground
	 */
	private static Ground getElementToPersist12BeginGround(FiveElement fiveElement) {
		return new MapWrapper<FiveElement, Ground>(new HashMap<FiveElement, Ground>())
				.put(FiveElement.WATER, Ground.getByDisplayName("申").get())
				.put(FiveElement.WOOD, Ground.getByDisplayName("亥").get())
				.put(FiveElement.GOLD, Ground.getByDisplayName("巳").get())
				.put(FiveElement.EARTH, Ground.getByDisplayName("申").get())
				.put(FiveElement.FIRE, Ground.getByDisplayName("寅").get()).getMap().get(fiveElement);
	}

	/**
	 * Setup age range.
	 *
	 * @param destiny
	 *            the destiny
	 * @param ageStartIndexedCells
	 *            the age start indexed cells
	 */
	public static void setupAgeRange(Destiny destiny, List<Cell> ageStartIndexedCells) {
		// 陽男陰女順行
		int vector = destiny.getShadowLight() == ShadowLight.LIGHT ? 1 : -1;
		vector *= destiny.getConfig().getSex() == Sex.M ? 1 : -1;
		Direction direction = vector == 1 ? Direction.CLOCKWISE : Direction.ANTICLOCKWISE;

		int ageStart = destiny.getFiveElement().getNumber();
		Cell destinyCell = destiny.getTempleCell(Temple.TEMPLE_DESTINY);

		for (int i = 0; i < NUM_CELLS; i++) {
			Cell cell = null;
			if (direction == Direction.CLOCKWISE) {
				cell = destinyCell.getNextICell(i).get();
			} else {
				cell = destinyCell.getPrevICell(i).get();
			}
			cell.setAgeStart(ageStart + 10 * i);// 歲數BEGIN
			cell.setAgeEnd(ageStart + 10 * i + 9);// 歲數END

			ageStartIndexedCells.add(cell);
		}

		// 長生12神
		Ground persist12BeginGround = getElementToPersist12BeginGround(destiny.getFiveElement());
		Cell persist12BeginCell = destiny.getGroundCell(persist12BeginGround);
		for (int i = 0; i < NUM_CELLS; i++) {
			Cell cell = null;
			if (direction == Direction.CLOCKWISE) {
				cell = persist12BeginCell.getNextICell(i).get();
			} else {
				cell = persist12BeginCell.getPrevICell(i).get();
			}
			cell.setPersist12(Persist12.values()[i]);
		}
	}

	/**
	 * Setup major stars.
	 *
	 * @param destiny
	 *            the destiny
	 * @param starToCellMap
	 *            the star to cell map
	 * @param majorStarEnergy
	 *            the major star energy
	 */
	public static void setupMajorStars(Destiny destiny, Map<Star, Cell> starToCellMap,
			Map<MajorStar, StarEnergyLevel> majorStarEnergy) {
		for (MajorStar majorStar : MajorStar.values()) {
			Cell cell = destiny.getGroundCell(majorStar.getGround(destiny));
			cell.getMajorStars().add(majorStar);
			starToCellMap.put(majorStar, cell);
			majorStarEnergy.put(majorStar, StarEnergyLevel.getByLevel(majorStar.getStarEnergy(cell.getGround())));
		}
	}

	/**
	 * Setup stars.
	 *
	 * @param destiny
	 *            the destiny
	 * @param starToCellMap
	 *            the star to cell map
	 */
	public static void setupStars(Destiny destiny, Map<Star, Cell> starToCellMap) {
		Star[] stars = new Star[] { MinorStar.MINOR_STAR_EMPTY_GROUND, // 地空
				MinorStar.MINOR_STAR_GROUND_DISASTER, // 地劫
				MinorStar.MINOR_STAR_FIRE_BURN, // 火星
				MinorStar.MINOR_STAR_INVISIBLE_PROBLEM, // 鈴星
				MinorStar.MINOR_STAR_FAILURE, // 擎羊
				MinorStar.MINOR_STAR_HINDER, // 陀羅
				MinorStar.MINOR_STAR_HORSE_CHANGE, // 天馬
				MinorStar.MINOR_STAR_CLOTH, // 祿存
				MinorStar.MINOR_STAR_HONOR, // 天魁
				MinorStar.MINOR_STAR_HONOR2, // 天鉞
				MinorStar.MINOR_STAR_CLEVER, // 文昌
				MinorStar.MINOR_STAR_SKILL, // 文曲
				MinorStar.MINOR_STAR_LEFT_SUPPORT, // 左輔
				MinorStar.MINOR_STAR_RIGHT_SUPPORT, // 右弼

				MiniStar.MINI_STAR_SKY_NOBLE, // 天貴
				MiniStar.MINI_STAR_SKY_HAPPINESS, // 天喜
				MiniStar.MINI_STAR_SKY_COOK, // 天廚
				MiniStar.MINI_STAR_SKY_CRY, // 天哭
				MiniStar.MINI_STAR_SKY_LOST, // 天虛
				MiniStar.MINI_STAR_DRAGON_SKILL, // 龍池
				MiniStar.MINI_STAR_PHOENIX_ART, // 鳳閣
				MiniStar.MINI_STAR_RED_MARRIAGE, // 紅鸞
				MiniStar.MINI_STAR_SKY_JOY_REPRODUCTION, // 天喜
				MiniStar.MINI_STAR_INDEPENDENT, // 孤辰
				MiniStar.MINI_STAR_SINGLE, // 寡宿
				MiniStar.MINI_STAR_RESOLVE, // 年解
				MiniStar.MINI_STAR_BROKEN, // 破碎
				MiniStar.MINI_STAR_BIG_LOST, // 大耗
				MiniStar.MINI_STAR_LITTLE_DISASTER, // 小耗
				MiniStar.MINI_STAR_BAD_ROMANCE, // 咸池
				MiniStar.MINI_STAR_MOON_ETHIC, // 月德
				MiniStar.MINI_STAR_GENIUS, // 天才
				MiniStar.MINI_STAR_LONG_LIFE, // 天壽
				MiniStar.MINI_STAR_EMPTY_SKY, // 天空
				MiniStar.MINI_STAR_LAZY_SKY, // 旬空
				MiniStar.MINI_STAR_LAZY_SKY2, // 旬空2
				MiniStar.MINI_STAR_INTERRUPT_SKY, // 截空
				MiniStar.MINI_STAR_INTERRUPT_SKY2, // 截空2
				MiniStar.MINI_STAR_PLATFORM_SUPPORT, // 台輔
				MiniStar.MINI_STAR_REWARD, // 封誥
				MiniStar.MINI_STAR_SKY_PUNISHMENT, // 天刑
				MiniStar.MINI_STAR_SKY_ROMANTIC, // 天姚
				MiniStar.MINI_STAR_SKY_WITCH, // 天巫
				MiniStar.MINI_STAR_SKY_MOON, // 天月
				MiniStar.MINI_STAR_GHOST, // 陰煞
				MiniStar.MINI_STAR_RESOLVE2, // 解神
				MiniStar.MINI_STAR_WRONG_MOUTH2, // 蜚廉
				MiniStar.MINI_STAR_THREE_TABLE, // 三台
				MiniStar.MINI_STAR_EIGHT_SEAT, // 八座
				MiniStar.MINI_STAR_HOLY_LIGHT, // 恩光
				MiniStar.MINI_STAR_SKY_PRECIOUS, // 天貴
				MiniStar.MINI_STAR_ANGEL, // 天使
				MiniStar.MINI_STAR_SKY_HURT // 天傷
		};
		for (Star star : stars) {
			Cell cell = destiny.getGroundCell(star.getGround(destiny));
			cell.addStar(star);
			starToCellMap.put(star, cell);
		}

		// 博士12神
		MiniStar[] twelvePreDoctorStars = new MiniStar[] { MiniStar.MINI_STAR_DOCTOR, // 博士
				MiniStar.MINI_STAR_STRENGTH, // 力士
				MiniStar.MINI_STAR_GREEN_DRAGON, // 青龍
				MiniStar.MINI_STAR_SMALL_LOST, // 小耗
				MiniStar.MINI_STAR_GENERAL, // 將軍
				MiniStar.MINI_STAR_LETTER_TO_KING, // 奏書
				MiniStar.MINI_STAR_WRONG_MOUTH, // 蜚廉
				MiniStar.MINI_STAR_JOY_GOD, // 喜神
				MiniStar.MINI_STAR_SICK_TICKET, // 病符
				MiniStar.MINI_STAR_BIG_LOST2, // 大耗
				MiniStar.MINI_STAR_ARMY_TRAP, // 伏兵
				MiniStar.MINI_STAR_GOVERNMENT // 官府
		};
		for (MiniStar star : twelvePreDoctorStars) {
			Cell cell = destiny.getGroundCell(star.getGround(destiny));
			cell.setPreDoctorStar(star);
			starToCellMap.put(star, cell);
		}

		// 歲前12神
		MiniStar[] twelvePreAgeStars = new MiniStar[] { MiniStar.MINI_STAR_YEAR_GOD, // 太歲
				MiniStar.MINI_STAR_NEGATIVE_MINDSET, // 晦氣
				MiniStar.MINI_STAR_LOST_DOOR, // 喪門
				MiniStar.MINI_STAR_PENETRATION, // 貫索
				MiniStar.MINI_STAR_GOVERNMENT_TICKET, // 官符
				MiniStar.MINI_STAR_SMALL_LOST2, // 小耗
				MiniStar.MINI_STAR_AGE_BROKEN, // 歲破
				MiniStar.MINI_STAR_DRAGON_ETHIC, // 龍德
				MiniStar.MINI_STAR_WHITE_TIGER, // 白虎
				MiniStar.MINI_STAR_FATHER_GIFT, // 天德
				MiniStar.MINI_STAR_PARENT_DIE, // 弔客
				MiniStar.MINI_STAR_SICK_TICKET2 // 病符
		};
		for (MiniStar star : twelvePreAgeStars) {
			Cell cell = destiny.getGroundCell(star.getGround(destiny));
			cell.setPreAgeStar(star);
			starToCellMap.put(star, cell);
		}

		// 將前12神
		MiniStar[] twelvePreGeneralStars = new MiniStar[] { MiniStar.MINI_STAR_GENERAL_STAR, // 將星
				MiniStar.MINI_STAR_CLIMB_HORSE, // 攀鞍
				MiniStar.MINI_STAR_AGE_HORSE, // 歲驛
				MiniStar.MINI_STAR_REST_GOD, // 息神
				MiniStar.MINI_STAR_MYSTIC, // 華蓋
				MiniStar.MINI_STAR_LITTLE_DISASTER2, // 劫煞
				MiniStar.MINI_STAR_DISASTER, // 災煞
				MiniStar.MINI_STAR_SKY_DISASTER, // 天煞
				MiniStar.MINI_STAR_BETRAY, // 指背
				MiniStar.MINI_STAR_BAD_ROMANCE2, // 咸池
				MiniStar.MINI_STAR_MOON_MONSTER, // 月煞
				MiniStar.MINI_STAR_DEAD_GOD // 亡神
		};
		for (MiniStar star : twelvePreGeneralStars) {
			Cell cell = destiny.getGroundCell(star.getGround(destiny));
			cell.setPreGeneralStar(star);
			starToCellMap.put(star, cell);
		}

	}

	// 命主, 身主
	/**
	 * Sets the up destiny body master.
	 *
	 * @param destiny
	 *            the new up destiny body master
	 */
	public static void setupDestinyBodyMaster(Destiny destiny) {
		destiny.setDestinyMaster(
				new Star[] { MajorStar.MAJOR_STAR_GREED, MajorStar.MAJOR_STAR_MOUTH, MinorStar.MINOR_STAR_CLOTH,
						MinorStar.MINOR_STAR_SKILL, MajorStar.MAJOR_STAR_HONEST, MajorStar.MAJOR_STAR_MONEY,
						MajorStar.MAJOR_STAR_SOLDIER, MajorStar.MAJOR_STAR_MONEY, MajorStar.MAJOR_STAR_HONEST,
						MinorStar.MINOR_STAR_SKILL, MinorStar.MINOR_STAR_CLOTH, MajorStar.MAJOR_STAR_MOUTH }[destiny
								.getConfig().getYearGround().getIndex()]);

		destiny.setBodyMaster(new Star[] { MinorStar.MINOR_STAR_FIRE_BURN, MajorStar.MAJOR_STAR_HANDPRINT,
				MajorStar.MAJOR_STAR_LAW, MajorStar.MAJOR_STAR_RECREATION, MinorStar.MINOR_STAR_CLEVER,
				MajorStar.MAJOR_STAR_COUNSELLOR, MinorStar.MINOR_STAR_FIRE_BURN, MajorStar.MAJOR_STAR_HANDPRINT,
				MajorStar.MAJOR_STAR_LAW, MajorStar.MAJOR_STAR_RECREATION, MinorStar.MINOR_STAR_CLEVER,
				MajorStar.MAJOR_STAR_COUNSELLOR }[destiny.getConfig().getYearGround().getIndex()]);
	}

	// 子斗
	/**
	 * Sets the up son dou.
	 *
	 * @param destiny
	 *            the new up son dou
	 */
	public static void setupSonDou(Destiny destiny) {
		Ground bornTimeGround = destiny.getConfig().getBornTimeGround().getGround();
		int bornMonth = destiny.getConfig().getDoubleMonthLogicalMonth();
		destiny.setSonDou(bornTimeGround.shift(-bornMonth + 1));
	}

	/**
	 * Sets the up path clockwise.
	 *
	 * @param destiny
	 *            the new up path clockwise
	 */
	public static void setupPathClockwise(Destiny destiny) {
		destiny.setPathClockwise(destiny.getShadowLight() == ShadowLight.LIGHT && destiny.getConfig().getSex() == Sex.M
				|| destiny.getShadowLight() == ShadowLight.SHADOW && destiny.getConfig().getSex() == Sex.F);
	}

	// 四化
	/**
	 * Setup star reactions.
	 *
	 * @param destiny
	 *            the destiny
	 * @param starReactionMap
	 *            the star reaction map
	 */
	public static void setupStarReactions(Destiny destiny, Map<StarReaction, Star> starReactionMap) {
		Sky yearSky = destiny.getConfig().getYearSky();

		Star starTreasure = StarReaction.getStarReactionTreasureStar(yearSky);
		starReactionMap.put(StarReaction.STAR_TO_TREASURE, starTreasure);

		Star starPower = StarReaction.getStarReactionPowerStar(yearSky);
		starReactionMap.put(StarReaction.STAR_TO_POWER, starPower);

		Star starPosition = StarReaction.getStarReactionPositionStar(yearSky);
		starReactionMap.put(StarReaction.STAR_TO_POSITION, starPosition);

		Star starProblem = StarReaction.getStarReactionProblemStar(yearSky);
		starReactionMap.put(StarReaction.STAR_TO_PROBLEM, starProblem);
	}

	// 借星
	/**
	 * Sets the up browser cells.
	 *
	 * @param destiny
	 *            the new up browser cells
	 */
	public static void setupBrowserCells(Destiny destiny) {
		List<Cell> cells = destiny.getCells();
		for (Cell cell : cells) {
			if (cell.getMajorStars().isEmpty()) {

				if (cell.getNextICell(4).get().getMajorStars().isEmpty()) {
					cell.setBorrowCells(Arrays.asList(new BorrowCell(54.26f, cell.getNextICell(6).get()),
							new BorrowCell(32.45f, cell.getPrevICell(4).get()),
							new BorrowCell(13.29f, cell.getPrevICell(2).get())));

				} else if (cell.getPrevICell(4).get().getMajorStars().isEmpty()) {
					cell.setBorrowCells(Arrays.asList(new BorrowCell(54.26f, cell.getNextICell(6).get()),
							new BorrowCell(32.45f, cell.getNextICell(4).get()),
							new BorrowCell(13.29f, cell.getNextICell(2).get())));
				} else {
					cell.setBorrowCells(Arrays.asList(new BorrowCell(51f, cell.getNextICell(6).get()),
							new BorrowCell(24.5f, cell.getNextICell(4).get()),
							new BorrowCell(24.5f, cell.getPrevICell(4).get())));
				}
			}
		}
	}
}
