package com.airic.fortel.core.util;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.EnumSet;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * The Class CommonUtil.
 *
 * @author Eric Yu
 */
public final class CommonUtil {

	/** The Constant logger. */
	static final Logger LOGGER = Logger.getLogger(CommonUtil.class.getName());

	/**
	 * Instantiates a new common util.
	 */
	private CommonUtil() {
	}

	/**
	 * The Class MapWrapper.
	 *
	 * @param <T>
	 *            the generic type
	 * @param <U>
	 *            the generic type
	 */
	public static final class MapWrapper<T, U> {

		/** The map. */
		private Map<T, U> map;

		/**
		 * Instantiates a new map wrapper.
		 *
		 * @param map
		 *            the map
		 */
		public MapWrapper(Map<T, U> map) {
			this.map = map;
		}

		/**
		 * Put.
		 *
		 * @param key
		 *            the key
		 * @param value
		 *            the value
		 * @return the map wrapper
		 */
		public MapWrapper<T, U> put(T key, U value) {
			map.put(key, value);
			return this;
		}

		/**
		 * Gets the map.
		 *
		 * @return the map
		 */
		public Map<T, U> getMap() {
			return map;
		}
	}

	/**
	 * Mod.
	 *
	 * @param a
	 *            the a
	 * @param b
	 *            the b
	 * @return the int
	 */
	public static int mod(int a, int b) {
		return (a % b + b) % b;
	}

	/**
	 * Gets the enum by name.
	 *
	 * @param <E>
	 *            the element type
	 * @param clazz
	 *            the clazz
	 * @param s
	 *            the s
	 * @return the enum by name
	 */
	public static <E extends Enum<E>> E getEnumByName(Class<E> clazz, String s) {
		if (s != null) {
			for (E en : EnumSet.allOf(clazz)) {
				Method displayNameMethod;
				try {
					displayNameMethod = clazz.getMethod("getDisplayName", new Class[0]);
					if (String.valueOf(displayNameMethod.invoke(en)).equalsIgnoreCase(s)) {
						return en;
					}
				} catch (NoSuchMethodException | IllegalAccessException | IllegalArgumentException
						| InvocationTargetException e) {
					LOGGER.log(Level.WARNING, e.getMessage(), e);
				}
			}
		}
		return null;
	}

}
