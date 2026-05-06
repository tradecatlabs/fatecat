package com.airic.fortel.core.destiny.pattern;

import java.io.Serializable;

/**
 * The Enum PatternType.
 */
public interface PatternType extends Serializable {

	/**
	 * Gets the pattern type name.
	 *
	 * @return the pattern type name
	 */
	default public String getPatternTypeName() {
		return this.getClass().getSimpleName();
	}
}
