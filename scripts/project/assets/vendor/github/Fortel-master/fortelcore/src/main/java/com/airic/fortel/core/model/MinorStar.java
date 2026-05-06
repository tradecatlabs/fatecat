package com.airic.fortel.core.model;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

import com.airic.fortel.core.model.Data.Luck;
import com.airic.fortel.core.util.Const;
import com.fasterxml.jackson.annotation.JsonValue;

/**
 * The Enum MinorStar.
 *
 * @author Eric Yu
 */
public enum MinorStar implements Star {
	// 祿存
	/** The minor star cloth. */
	MINOR_STAR_CLOTH(Const.MINOR_STAR_CLOTH, Luck.LUCK) {
		public Ground getGround(Destiny destiny) {
			Sky yearSky = destiny.getConfig().getYearSky();
			return getRuntimeGroundBySky(yearSky);
		}

		public Ground getRuntimeGroundBySky(Sky sky) {
			return Ground.getByDisplayName(
					new String[] { Const.GROUND_2, Const.GROUND_3, Const.GROUND_5, Const.GROUND_6, Const.GROUND_5,
							Const.GROUND_6, Const.GROUND_8, Const.GROUND_9, Const.GROUND_11, Const.GROUND_0 }[sky
									.getIndex()])
					.get();
		}
	},
	// 天魁
	/** The minor star honor. */
	MINOR_STAR_HONOR(Const.MINOR_STAR_HONOR, Luck.LUCK) {
		public Ground getGround(Destiny destiny) {
			Sky yearSky = destiny.getConfig().getYearSky();
			return getRuntimeGroundBySky(yearSky);
		}

		public Ground getRuntimeGroundBySky(Sky sky) {
			return Ground.getByDisplayName(
					new String[] { Const.GROUND_1, Const.GROUND_0, Const.GROUND_11, Const.GROUND_11, Const.GROUND_1,
							Const.GROUND_0, Const.GROUND_1, Const.GROUND_2, Const.GROUND_3, Const.GROUND_3 }[sky
									.getIndex()])
					.get();
		}
	},
	// 天鉞
	/** The MINO r_ sta r_ hono r2. */
	MINOR_STAR_HONOR2(Const.MINOR_STAR_HONOR2, Luck.LUCK) {
		public Ground getGround(Destiny destiny) {
			Sky yearSky = destiny.getConfig().getYearSky();
			return getRuntimeGroundBySky(yearSky);
		}

		public Ground getRuntimeGroundBySky(Sky sky) {
			return Ground.getByDisplayName(
					new String[] { Const.GROUND_7, Const.GROUND_8, Const.GROUND_9, Const.GROUND_9, Const.GROUND_7,
							Const.GROUND_8, Const.GROUND_7, Const.GROUND_6, Const.GROUND_5, Const.GROUND_5 }[sky
									.getIndex()])
					.get();
		}
	},
	// 文昌
	/** The minor star clever. */
	MINOR_STAR_CLEVER(Const.MINOR_STAR_CLEVER, Luck.LUCK) {
		public Ground getGround(Destiny destiny) {
			Ground bornGround = destiny.getConfig().getBornTimeGround().getGround();
			return Ground.getByDisplayName(Const.GROUND_10).get().shift(-bornGround.getIndex());
		}

		public Ground getRuntimeGroundBySky(Sky sky) {
			return Ground.getByDisplayName(
					new String[] { Const.GROUND_5, Const.GROUND_6, Const.GROUND_8, Const.GROUND_9, Const.GROUND_8,
							Const.GROUND_9, Const.GROUND_11, Const.GROUND_0, Const.GROUND_2, Const.GROUND_3 }[sky
									.getIndex()])
					.get();
		}
	},
	// 文曲
	/** The minor star skill. */
	MINOR_STAR_SKILL(Const.MINOR_STAR_SKILL, Luck.LUCK) {
		public Ground getGround(Destiny destiny) {
			Ground bornGround = destiny.getConfig().getBornTimeGround().getGround();
			return Ground.getByDisplayName(Const.GROUND_4).get().shift(bornGround.getIndex());
		}

		public Ground getRuntimeGroundBySky(Sky sky) {
			return Ground.getByDisplayName(
					new String[] { Const.GROUND_9, Const.GROUND_8, Const.GROUND_6, Const.GROUND_5, Const.GROUND_6,
							Const.GROUND_5, Const.GROUND_3, Const.GROUND_2, Const.GROUND_0, Const.GROUND_11 }[sky
									.getIndex()])
					.get();
		}
	},
	// 左輔
	/** The minor star left support. */
	MINOR_STAR_LEFT_SUPPORT(Const.MINOR_STAR_LEFT_SUPPORT, Luck.LUCK) {
		public Ground getGround(Destiny destiny) {
			int month = destiny.getConfig().getDoubleMonthLogicalMonth();
			return Ground.getByDisplayName(Const.GROUND_4).get().shift(month - 1);
		}
	},
	// 右弼
	/** The minor star right support. */
	MINOR_STAR_RIGHT_SUPPORT(Const.MINOR_STAR_RIGHT_SUPPORT, Luck.LUCK) {
		public Ground getGround(Destiny destiny) {
			int month = destiny.getConfig().getDoubleMonthLogicalMonth();
			return Ground.getByDisplayName(Const.GROUND_10).get().shift(-(month - 1));
		}
	},
	// 地空
	/** The minor star empty ground. */
	MINOR_STAR_EMPTY_GROUND(Const.MINOR_STAR_EMPTY_GROUND, Luck.BAD_LUCK) {
		public Ground getGround(Destiny destiny) {
			Ground bornGround = destiny.getConfig().getBornTimeGround().getGround();
			return Ground.getByDisplayName(Const.GROUND_11).get().shift(-bornGround.getIndex());
		}
	},
	// 地劫
	/** The minor star ground disaster. */
	MINOR_STAR_GROUND_DISASTER(Const.MINOR_STAR_GROUND_DISASTER, Luck.BAD_LUCK) {
		public Ground getGround(Destiny destiny) {
			Ground bornGround = destiny.getConfig().getBornTimeGround().getGround();
			return Ground.getByDisplayName(Const.GROUND_11).get().shift(bornGround.getIndex());
		}
	},
	// 火星
	/** The minor star fire burn. */
	MINOR_STAR_FIRE_BURN(Const.MINOR_STAR_FIRE_BURN, Luck.BAD_LUCK) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			Ground bornGround = destiny.getConfig().getBornTimeGround().getGround();

			if (yearGround == Ground.getByDisplayName(Const.GROUND_2).get()
					|| yearGround == Ground.getByDisplayName(Const.GROUND_6).get()
					|| yearGround == Ground.getByDisplayName(Const.GROUND_10).get()) {
				return Ground.getByDisplayName(Const.GROUND_1).get().shift(bornGround.getIndex());
			} else if (yearGround == Ground.getByDisplayName(Const.GROUND_8).get()
					|| yearGround == Ground.getByDisplayName(Const.GROUND_0).get()
					|| yearGround == Ground.getByDisplayName(Const.GROUND_4).get()) {
				return Ground.getByDisplayName(Const.GROUND_2).get().shift(bornGround.getIndex());
			} else if (yearGround == Ground.getByDisplayName(Const.GROUND_5).get()
					|| yearGround == Ground.getByDisplayName(Const.GROUND_9).get()
					|| yearGround == Ground.getByDisplayName(Const.GROUND_1).get()) {
				return Ground.getByDisplayName(Const.GROUND_3).get().shift(bornGround.getIndex());
			} else {
				return Ground.getByDisplayName(Const.GROUND_9).get().shift(bornGround.getIndex());
			}
		}
	},
	// 鈴星
	/** The minor star invisible problem. */
	MINOR_STAR_INVISIBLE_PROBLEM(Const.MINOR_STAR_INVISIBLE_PROBLEM, Luck.BAD_LUCK) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			Ground bornGround = destiny.getConfig().getBornTimeGround().getGround();

			if (yearGround == Ground.getByDisplayName(Const.GROUND_2).get()
					|| yearGround == Ground.getByDisplayName(Const.GROUND_6).get()
					|| yearGround == Ground.getByDisplayName(Const.GROUND_10).get()) {
				return Ground.getByDisplayName(Const.GROUND_3).get().shift(bornGround.getIndex());
			} else {
				return Ground.getByDisplayName(Const.GROUND_10).get().shift(bornGround.getIndex());
			}
		}
	},
	// 擎羊
	/** The minor star failure. */
	MINOR_STAR_FAILURE(Const.MINOR_STAR_FAILURE, Luck.BAD_LUCK) {
		public Ground getGround(Destiny destiny) {
			Sky yearSky = destiny.getConfig().getYearSky();
			return getRuntimeGroundBySky(yearSky);
		}

		public Ground getRuntimeGroundBySky(Sky sky) {
			return Ground.getByDisplayName(
					new String[] { Const.GROUND_3, Const.GROUND_4, Const.GROUND_6, Const.GROUND_7, Const.GROUND_6,
							Const.GROUND_7, Const.GROUND_9, Const.GROUND_10, Const.GROUND_0, Const.GROUND_1 }[sky
									.getIndex()])
					.get();
		}
	},
	// 陀羅
	/** The minor star hinder. */
	MINOR_STAR_HINDER(Const.MINOR_STAR_HINDER, Luck.BAD_LUCK) {
		public Ground getGround(Destiny destiny) {
			Sky yearSky = destiny.getConfig().getYearSky();
			return getRuntimeGroundBySky(yearSky);
		}

		public Ground getRuntimeGroundBySky(Sky sky) {
			return Ground.getByDisplayName(
					new String[] { Const.GROUND_1, Const.GROUND_2, Const.GROUND_4, Const.GROUND_5, Const.GROUND_4,
							Const.GROUND_5, Const.GROUND_7, Const.GROUND_8, Const.GROUND_10, Const.GROUND_11 }[sky
									.getIndex()])
					.get();
		}
	},
	// 天馬
	/** The minor star horse change. */
	MINOR_STAR_HORSE_CHANGE(Const.MINOR_STAR_HORSE_CHANGE) {
		public Ground getGround(Destiny destiny) {
			Ground yearGround = destiny.getConfig().getYearGround();
			return Ground.getByDisplayName(new String[] { Const.GROUND_2, Const.GROUND_11, Const.GROUND_8,
					Const.GROUND_5, Const.GROUND_2, Const.GROUND_11, Const.GROUND_8, Const.GROUND_5, Const.GROUND_2,
					Const.GROUND_11, Const.GROUND_8, Const.GROUND_5 }[yearGround.getIndex()]).get();
		}
	};

	/** The display name. */
	private String displayName;

	/** The display name to value map. */
	private static Map<String, MinorStar> displayNameToValueMap = new HashMap<String, MinorStar>();

	/** The luck. */
	private Luck luck;

	/** The Constant COUNT. */
	public static final int COUNT = Ground.values().length;

	static {
		for (MinorStar secondaryStar : MinorStar.values()) {
			displayNameToValueMap.put(secondaryStar.displayName, secondaryStar);
		}
	}

	/**
	 * Instantiates a new minor star.
	 *
	 * @param displayName
	 *            the display name
	 */
	private MinorStar(String displayName) {
		this.displayName = displayName;
		this.luck = Luck.NEUTRAL;
	}

	/**
	 * Instantiates a new minor star.
	 *
	 * @param displayName
	 *            the display name
	 * @param luck
	 *            the luck
	 */
	private MinorStar(String displayName, Luck luck) {
		this.displayName = displayName;
		this.luck = luck;
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
	public static Optional<MinorStar> getByDisplayName(String name) {
		return Optional.<MinorStar>of(displayNameToValueMap.get(name));
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

	/**
	 * Gets the runtime ground by sky.
	 *
	 * @param sky
	 *            the sky
	 * @return the runtime ground by sky
	 */
	public Ground getRuntimeGroundBySky(Sky sky) {
		return null;
	}

	/**
	 * Gets the luck.
	 *
	 * @return the luck
	 */
	public Luck getLuck() {
		return luck;
	}

	/**
	 * Sets the luck.
	 *
	 * @param luck
	 *            the new luck
	 */
	public void setLuck(Luck luck) {
		this.luck = luck;
	}

	/**
	 * Gets the horse change runtime ground by ground.
	 *
	 * @param ground
	 *            the ground
	 * @return the horse change runtime ground by ground
	 */
	public static Ground getHorseChangeRuntimeGroundByGround(Ground ground) {
		return new Ground[] { Ground.GROUND_2, Ground.GROUND_11, Ground.GROUND_8, Ground.GROUND_5 }[ground.getIndex()
				% 4];
	}

}