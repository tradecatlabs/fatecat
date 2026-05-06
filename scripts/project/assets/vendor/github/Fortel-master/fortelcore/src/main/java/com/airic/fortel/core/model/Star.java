package com.airic.fortel.core.model;

/**
 * The Interface Star.
 *
 * @author Eric Yu
 */
public interface Star extends StarElement {

	/**
	 * Gets the ground.
	 *
	 * @param destiny
	 *            the destiny
	 * @return the ground
	 */
	public Ground getGround(Destiny destiny);

	/**
	 * Gets the display name.
	 *
	 * @return the display name
	 */
	public String getDisplayName();
}
