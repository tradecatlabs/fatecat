package com.airic.fortel.core.destiny.pattern.impl;

import com.airic.fortel.core.destiny.pattern.PatternType;

/**
 * The Class FormationPatternType.
 */
public class FormationPatternType implements PatternType {

	/** The Constant serialVersionUID. */
	private static final long serialVersionUID = 7429142038813570321L;

	/** The Constant INSTANCE. */
	public static final PatternType INSTANCE = new FormationPatternType();

	/**
	 * Instantiates a new formation pattern type.
	 */
	private FormationPatternType() {
	}

	/**
	 * Gets the single instance of FormationPatternType.
	 *
	 * @return single instance of FormationPatternType
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
		return FormationPatternType.class.getCanonicalName();
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see java.lang.Object#toString()
	 */
	public String toString() {
		return FormationPatternType.class.getCanonicalName();
	}
}
