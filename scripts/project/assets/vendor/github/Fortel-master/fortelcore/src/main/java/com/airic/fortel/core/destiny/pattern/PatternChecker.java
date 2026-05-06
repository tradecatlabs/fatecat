package com.airic.fortel.core.destiny.pattern;

import java.util.List;

import com.airic.fortel.core.model.Destiny;

/**
 * The Interface PatternChecker.
 */
public interface PatternChecker {

	/**
	 * Visit destiny.
	 *
	 * @param destiny
	 *            the destiny
	 * @return the list
	 */
	List<Pattern> visitDestiny(Destiny destiny);
}
