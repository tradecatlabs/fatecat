package com.airic.fortel.core.destiny.pattern;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;

import org.apache.commons.lang3.builder.ReflectionToStringBuilder;

/**
 * The Class Pattern.
 */
public class Pattern implements Serializable {

	/** The Constant serialVersionUID. */
	private static final long serialVersionUID = -1031246820215014948L;

	/** The pattern type. */
	protected PatternType patternType = null;

	/** The category. */
	protected String category = "";

	/** The name. */
	protected String name = "";

	/** The description. */
	protected String description = "";// short summary

	/** The explaination. */
	protected String explaination = "";// detail explaination

	/** The metadata. */
	protected Map<String, String> metadata = new HashMap<String, String>();

	/**
	 * Instantiates a new pattern.
	 */
	public Pattern() {
	}

	/**
	 * Instantiates a new pattern.
	 *
	 * @param name
	 *            the name
	 * @param description
	 *            the description
	 */
	public Pattern(String name, String description) {
		this();
		this.name = name;
		this.description = description;
	}

	/**
	 * Instantiates a new pattern.
	 *
	 * @param name
	 *            the name
	 * @param description
	 *            the description
	 * @param explaination
	 *            the explaination
	 */
	public Pattern(String name, String description, String explaination) {
		this();
		this.name = name;
		this.description = description;
		this.explaination = explaination;
	}

	/**
	 * Gets the pattern type.
	 *
	 * @return the pattern type
	 */
	public PatternType getPatternType() {
		return patternType;
	}

	/**
	 * Sets the pattern type.
	 *
	 * @param patternType
	 *            the new pattern type
	 */
	public void setPatternType(PatternType patternType) {
		this.patternType = patternType;
	}

	/**
	 * Gets the category.
	 *
	 * @return the category
	 */
	public String getCategory() {
		return category;
	}

	/**
	 * Sets the category.
	 *
	 * @param category
	 *            the new category
	 */
	public void setCategory(String category) {
		this.category = category;
	}

	/**
	 * Gets the name.
	 *
	 * @return the name
	 */
	public String getName() {
		return name;
	}

	/**
	 * Sets the name.
	 *
	 * @param name
	 *            the new name
	 */
	public void setName(String name) {
		this.name = name;
	}

	/**
	 * Gets the description.
	 *
	 * @return the description
	 */
	public String getDescription() {
		return description;
	}

	/**
	 * Sets the description.
	 *
	 * @param description
	 *            the new description
	 */
	public void setDescription(String description) {
		this.description = description;
	}

	/**
	 * Gets the explaination.
	 *
	 * @return the explaination
	 */
	public String getExplaination() {
		return explaination;
	}

	/**
	 * Sets the explaination.
	 *
	 * @param explaination
	 *            the new explaination
	 */
	public void setExplaination(String explaination) {
		this.explaination = explaination;
	}

	/**
	 * Gets the attribute.
	 *
	 * @param key
	 *            the key
	 * @return the attribute
	 */
	public String getAttribute(String key) {
		return metadata.get(key);
	}

	/**
	 * Sets the attribute.
	 *
	 * @param key
	 *            the key
	 * @param value
	 *            the value
	 */
	public void setAttribute(String key, String value) {
		metadata.put(key, value);
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see java.lang.Object#toString()
	 */
	@Override
	public String toString() {
		return ReflectionToStringBuilder.toString(this);
	}
}
