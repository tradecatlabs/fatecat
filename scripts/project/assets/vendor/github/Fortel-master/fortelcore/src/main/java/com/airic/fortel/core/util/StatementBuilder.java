package com.airic.fortel.core.util;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * The Class StatementBuilder.
 */
public class StatementBuilder {

	/** The statements. */
	private List<String> statements = new ArrayList<String>();

	/** The delimiter. */
	private String delimiter = "";

	/** The prefix. */
	private String prefix = "";

	/** The suffix. */
	private String suffix = "";

	/**
	 * Instantiates a new statement builder.
	 */
	public StatementBuilder() {
		super();
		this.delimiter = "；";
		this.suffix = "。";
	}

	/**
	 * Instantiates a new statement builder.
	 *
	 * @param delimiter
	 *            the delimiter
	 * @param suffix
	 *            the suffix
	 */
	public StatementBuilder(String delimiter, String suffix) {
		super();
		this.delimiter = delimiter;
		this.suffix = suffix;
	}

	/**
	 * Instantiates a new statement builder.
	 *
	 * @param prefix
	 *            the prefix
	 * @param delimiter
	 *            the delimiter
	 * @param suffix
	 *            the suffix
	 */
	public StatementBuilder(String prefix, String delimiter, String suffix) {
		super();
		this.prefix = prefix;
		this.delimiter = delimiter;
		this.suffix = suffix;
	}

	/**
	 * Sets the prefix.
	 *
	 * @param prefix
	 *            the new prefix
	 */
	public void setPrefix(String prefix) {
		this.prefix = prefix;
	}

	/**
	 * Sets the suffix.
	 *
	 * @param suffix
	 *            the new suffix
	 */
	public void setSuffix(String suffix) {
		this.suffix = suffix;
	}

	/**
	 * Adds the statement.
	 *
	 * @param statement
	 *            the statement
	 */
	public void addStatement(String statement) {
		statements.add(statement);
	}

	/**
	 * Builds the.
	 *
	 * @return the string
	 */
	public String build() {
		return this.joinStatements(delimiter, prefix, suffix, statements.<String>toArray(new String[] {}));
	}

	/**
	 * Join statements.
	 *
	 * @param delimiter
	 *            the delimiter
	 * @param prefix
	 *            the prefix
	 * @param suffix
	 *            the suffix
	 * @param statements
	 *            the statements
	 * @return the string
	 */
	private String joinStatements(String delimiter, String prefix, String suffix, String... statements) {
		if (statements.length > 0) {
			return Stream.of(statements).collect(Collectors.joining(delimiter, prefix, suffix));
		} else {
			return "";
		}
	}
}
