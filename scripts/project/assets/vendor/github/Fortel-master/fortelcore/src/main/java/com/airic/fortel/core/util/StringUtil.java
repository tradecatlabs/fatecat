package com.airic.fortel.core.util;

import org.apache.commons.lang3.StringUtils;

/**
 * The Class StringUtil.
 */
/**
 * @author Eric Yu
 *
 */
public final class StringUtil {

	/**
	 * Instantiates a new string util.
	 */
	private StringUtil() {
	}

	/**
	 * Object to empty string.
	 *
	 * @param object
	 *            the object
	 * @return the string
	 */
	public static String objectToEmptyString(Object object) {
		if (object == null) {
			return "";
		} else {
			return StringUtils.trimToEmpty(object.toString());
		}
	}

	/**
	 * Object to null string.
	 *
	 * @param object
	 *            the object
	 * @return the string
	 */
	public static String objectToNullString(Object object) {
		if (object == null) {
			return null;
		} else {
			return StringUtils.trimToNull(object.toString());
		}
	}

}
