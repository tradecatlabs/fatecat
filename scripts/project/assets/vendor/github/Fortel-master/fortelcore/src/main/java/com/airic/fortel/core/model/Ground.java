package com.airic.fortel.core.model;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

import com.airic.fortel.core.util.CommonUtil;
import com.airic.fortel.core.util.Const;
import com.fasterxml.jackson.annotation.JsonValue;

//地支
/**
 * The Enum Ground.
 */
public enum Ground {

	/** The GROUN d_0. */
	GROUND_0(Const.GROUND_0, 0), // 子
	/** The GROUN d_1. */
	GROUND_1(Const.GROUND_1, 1), // 丑
	/** The GROUN d_2. */
	GROUND_2(Const.GROUND_2, 2), // 寅
	/** The GROUN d_3. */
	GROUND_3(Const.GROUND_3, 3), // 卯
	/** The GROUN d_4. */
	GROUND_4(Const.GROUND_4, 4), // 辰
	/** The GROUN d_5. */
	GROUND_5(Const.GROUND_5, 5), // 巳
	/** The GROUN d_6. */
	GROUND_6(Const.GROUND_6, 6), // 午
	/** The GROUN d_7. */
	GROUND_7(Const.GROUND_7, 7), // 未
	/** The GROUN d_8. */
	GROUND_8(Const.GROUND_8, 8), // 申
	/** The GROUN d_9. */
	GROUND_9(Const.GROUND_9, 9), // 酉
	/** The GROUN d_10. */
	GROUND_10(Const.GROUND_10, 10), // 戌
	/** The GROUN d_11. */
	GROUND_11(Const.GROUND_11, 11);// 亥

	/** The display name. */
	private String displayName;

	/** The index. */
	private int index;

	/** The display name to value map. */
	private static Map<String, Ground> displayNameToValueMap = new HashMap<String, Ground>();

	/** The Constant COUNT. */
	public static final int COUNT = Ground.values().length;

	static {
		for (Ground ground : Ground.values()) {
			displayNameToValueMap.put(ground.displayName, ground);
		}
	}

	/**
	 * Instantiates a new ground.
	 *
	 * @param displayName
	 *            the display name
	 * @param index
	 *            the index
	 */
	private Ground(String displayName, int index) {
		this.displayName = displayName;
		this.index = index;
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

	/*
	 * (non-Javadoc)
	 * 
	 * @see java.lang.Enum#toString()
	 */
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
	public static Optional<Ground> getByDisplayName(String name) {
		return Optional.of(displayNameToValueMap.get(name));
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
	 * Gets the by index.
	 *
	 * @param index
	 *            the index
	 * @return the by index
	 */
	public static Ground getByIndex(int index) {
		return Ground.values()[CommonUtil.mod(index, Ground.values().length)];
	}

	/**
	 * Shift.
	 *
	 * @param i
	 *            the i
	 * @return the ground
	 */
	public Ground shift(int i) {
		return getByIndex(this.index + i);
	}

}
