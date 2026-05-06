package com.airic.fortel.core.destiny.pattern.impl;

import java.util.Collections;
import java.util.List;

import com.airic.fortel.core.destiny.pattern.Pattern;
import com.airic.fortel.core.destiny.pattern.PatternChecker;
import com.airic.fortel.core.model.Destiny;

/**
 * The Class DummyPatternChecker.
 */
public class DummyPatternChecker implements PatternChecker {

	/* (non-Javadoc)
	 * @see com.airic.fortel.core.destiny.pattern.PatternChecker#visitDestiny(com.airic.fortel.core.model.Destiny)
	 */
	public List<Pattern> visitDestiny(Destiny destiny) {
		return Collections.emptyList();
	}
}
