package com.airic.fortel.core.destiny.pattern.impl;

import com.airic.fortel.core.destiny.pattern.PatternType;

/**
 * The Class GeneralCharacteristicPatternType.
 */
public class GeneralCharacteristicPatternType implements PatternType {

	/** The Constant serialVersionUID. */
	private static final long serialVersionUID = 5819242798228437905L;

	/** The Constant INSTANCE. */
	public static final PatternType INSTANCE = new GeneralCharacteristicPatternType();

	/**
	 * Instantiates a new general characteristic pattern type.
	 */
	private GeneralCharacteristicPatternType() {
	}

	/**
	 * Gets the single instance of GeneralCharacteristicPatternType.
	 *
	 * @return single instance of GeneralCharacteristicPatternType
	 */
	public static PatternType getInstance() {
		return INSTANCE;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see com.airic.fortel.core.destiny.pattern.PatternType#getPatternTypeName()
	 */
	public String getPatternTypeName() {
		return GeneralCharacteristicPatternType.class.getCanonicalName();
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see java.lang.Object#toString()
	 */
	public String toString() {
		return GeneralCharacteristicPatternType.class.getCanonicalName();
	}
}
