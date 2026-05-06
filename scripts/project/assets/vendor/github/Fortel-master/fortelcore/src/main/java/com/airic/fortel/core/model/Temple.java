package com.airic.fortel.core.model;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

import com.airic.fortel.core.util.CommonUtil;
import com.fasterxml.jackson.annotation.JsonValue;

/**
 * The Enum Temple.
 *
 * @author Eric Yu
 */
public enum Temple {

	/** The temple body. */
	TEMPLE_BODY("身宮", "身宮", "body", 0),

	/** The temple destiny. */
	TEMPLE_DESTINY("命宮", "命宮", "destiny", 1),

	/** The temple brother. */
	TEMPLE_BROTHER("兄弟", "兄弟宮", "brother", 2),

	/** The temple marriage. */
	TEMPLE_MARRIAGE("夫妻", "夫妻宮", "marriage", 3),

	/** The temple children. */
	TEMPLE_CHILDREN("子女", "子女宮", "children", 4),

	/** The temple money. */
	TEMPLE_MONEY("財帛", "財帛宮", "money", 5),

	/** The temple sick. */
	TEMPLE_SICK("疾厄", "疾厄宮", "sick", 6),

	/** The temple move. */
	TEMPLE_MOVE("遷移", "遷移宮", "move", 7),

	/** The temple friend. */
	TEMPLE_FRIEND("交友", "交友宮", "friend", 8),

	/** The temple career. */
	TEMPLE_CAREER("事業", "事業宮", "career", 9),

	/** The temple house. */
	TEMPLE_HOUSE("田宅", "田宅宮", "house", 10),

	/** The temple happiness. */
	TEMPLE_HAPPINESS("福德", "福德宮", "happiness", 11),

	/** The temple parent. */
	TEMPLE_PARENT("父母", "父母宮", "parent", 12);

	/** The Constant COUNT. */
	public static final int COUNT = Temple.values().length;

	/** The display name. */
	private String displayName;

	/** The full name. */
	private String fullName;

	/** The alias. */
	private String alias;

	/** The index. */
	private int index;

	/** The display name to value map. */
	private static Map<String, Temple> displayNameToValueMap = new HashMap<String, Temple>();

	static {
		for (Temple temple : Temple.values()) {
			displayNameToValueMap.put(temple.displayName, temple);
		}
	}

	/**
	 * Instantiates a new temple.
	 *
	 * @param displayName
	 *            the display name
	 * @param fullName
	 *            the full name
	 * @param alias
	 *            the alias
	 * @param index
	 *            the index
	 */
	Temple(String displayName, String fullName, String alias, int index) {
		this.displayName = displayName;
		this.fullName = fullName;
		this.alias = alias;
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
	 * Gets the full name.
	 *
	 * @return the full name
	 */
	public String getFullName() {
		return fullName;
	}

	/**
	 * Gets the alias.
	 *
	 * @return the alias
	 */
	public String getAlias() {
		return this.alias;
	}

	/**
	 * Gets the index.
	 *
	 * @return the index
	 */
	public int getIndex() {
		return index;
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
	@JsonValue
	public String toString() {
		return this.displayName;
	}

	/**
	 * Gets the by index.
	 *
	 * @param index
	 *            the index
	 * @return the by index
	 */
	public static Temple getByIndex(int index) {
		return Temple.values()[CommonUtil.mod(index, Temple.values().length)];
	}

	/**
	 * Gets the by display name.
	 *
	 * @param name
	 *            the name
	 * @return the by display name
	 */
	public static Optional<Temple> getByDisplayName(String name) {
		return Optional.<Temple>of(displayNameToValueMap.get(name));
	}

	/**
	 * Shift.
	 *
	 * @param i
	 *            the i
	 * @return the temple
	 */
	public Temple shift(int i) {
		return getByIndex(this.index + i);
	}

}
