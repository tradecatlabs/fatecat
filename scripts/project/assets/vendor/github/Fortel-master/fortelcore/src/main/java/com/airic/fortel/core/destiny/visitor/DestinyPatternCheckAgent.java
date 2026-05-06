package com.airic.fortel.core.destiny.visitor;

import java.util.List;
import java.util.stream.Collectors;

import com.airic.fortel.core.destiny.pattern.Pattern;
import com.airic.fortel.core.destiny.pattern.PatternChecker;
import com.airic.fortel.core.model.Destiny;

/**
 * The Class DestinyPatternCheckAgent.
 */
public class DestinyPatternCheckAgent {

	/**
	 * Instantiates a new destiny pattern check agent.
	 */
	public DestinyPatternCheckAgent() {
	}

	// 命盤格局檢查
	/**
	 * Check destiny.
	 *
	 * @param destiny
	 *            the destiny
	 * @param patternCheckers
	 *            the pattern checkers
	 * @return the destiny patterns
	 */
	public static DestinyPatterns checkDestiny(Destiny destiny, List<PatternChecker> patternCheckers) {
		final DestinyPatterns destinyPatterns = new DestinyPatterns();

		if (patternCheckers != null) {
			List<Pattern> patterns = patternCheckers.stream().flatMap(checker -> checker.visitDestiny(destiny).stream())
					.collect(Collectors.toList());

			destinyPatterns.addPatterns(patterns);
		}
		return destinyPatterns;
	}

}
