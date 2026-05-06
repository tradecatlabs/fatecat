package com.airic.fortel.core.calendar.util;

import java.io.Serializable;

/**
 * The Class Lunar.
 */
public class Lunar implements Serializable {

	/** The Constant serialVersionUID. */
	private static final long serialVersionUID = 4986391064617411454L;

	/** 年. */
	private int year;

	/** 月. */
	private int month;

	/** 日. */
	private int day;

	/** 該月是否為閏月. */
	private boolean leap;

	/**
	 * Instantiates a new lunar.
	 */
	public Lunar() {

	}

	/**
	 * Instantiates a new lunar.
	 *
	 * @param year
	 *            the year
	 * @param month
	 *            the month
	 * @param day
	 *            the day
	 * @param leap
	 *            the leap
	 */
	public Lunar(int year, int month, int day, boolean leap) {
		this.year = year;
		this.month = month;
		this.day = day;
		this.leap = leap;
	}

	/**
	 * Getter method for property year.
	 *
	 * @return property value of year
	 */
	public int getYear() {
		return year;
	}

	/**
	 * Setter method for property year.
	 *
	 * @param year
	 *            value to be assigned to property year
	 */
	public void setYear(int year) {
		this.year = year;
	}

	/**
	 * Getter method for property month.
	 *
	 * @return property value of month
	 */
	public int getMonth() {
		return month;
	}

	/**
	 * Gets the effective month.
	 *
	 * @return the effective month
	 */
	public int getEffectiveMonth() {
		return (leap && day > 15) ? month + 1 : month;
	}

	/**
	 * Setter method for property month.
	 *
	 * @param month
	 *            value to be assigned to property month
	 */
	public void setMonth(int month) {
		this.month = month;
	}

	/**
	 * Getter method for property day.
	 *
	 * @return property value of day
	 */
	public int getDay() {
		return day;
	}

	/**
	 * Setter method for property day.
	 *
	 * @param day
	 *            value to be assigned to property day
	 */
	public void setDay(int day) {
		this.day = day;
	}

	/**
	 * Getter method for property leap.
	 *
	 * @return property value of leap
	 */
	public boolean isLeap() {
		return leap;
	}

	/**
	 * Setter method for property leap.
	 *
	 * @param leap
	 *            value to be assigned to property leap
	 */
	public void setLeap(boolean leap) {
		this.leap = leap;
	}

	/* (non-Javadoc)
	 * @see java.lang.Object#toString()
	 */
	@Override
	public String toString() {
		return getYear() + "(" + LunarUtil.cyclical(getYear()) + ")年" + (isLeap() ? "閏" : "")
				+ LunarUtil.getChnMonth(getMonth()) + "月" + LunarUtil.getChnDay(getDay());
	}

	/**
	 * To string.
	 *
	 * @param outputYear
	 *            the output year
	 * @param outputMonth
	 *            the output month
	 * @param outputDay
	 *            the output day
	 * @return the string
	 */
	public String toString(boolean outputYear, boolean outputMonth, boolean outputDay) {
		StringBuilder sb = new StringBuilder();
		if (outputYear) {
			sb.append(getYear()).append("(").append(LunarUtil.cyclical(getYear())).append(")年");
		}
		if (outputMonth) {
			sb.append(isLeap() ? "閏" : "").append(LunarUtil.getChnMonth(getMonth())).append("月");
		}
		if (outputDay) {
			sb.append(LunarUtil.getChnDay(getDay()));
		}
		return sb.toString();
	}

	/*
	 * (non-Javadoc)
	 *
	 * @see java.lang.Object#hashCode()
	 */
	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + day;
		result = prime * result + (leap ? 1231 : 1237);
		result = prime * result + month;
		result = prime * result + year;
		return result;
	}

	/*
	 * (non-Javadoc)
	 *
	 * @see java.lang.Object#equals(java.lang.Object)
	 */
	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Lunar other = (Lunar) obj;
		if (day != other.day)
			return false;
		if (leap != other.leap)
			return false;
		if (month != other.month)
			return false;
		if (year != other.year)
			return false;
		return true;
	}

}