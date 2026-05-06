package com.airic.fortel.core.calendar.util;

import java.io.Serializable;

/**
 * The Class Solar.
 */
public class Solar implements Serializable {

	/** The Constant serialVersionUID. */
	private static final long serialVersionUID = -7844327858760821161L;

	/** 年. */
	private int year;

	/** 月. */
	private int month;

	/** 日. */
	private int day;

	/**
	 * Instantiates a new solar.
	 */
	public Solar() {
	}

	/**
	 * Instantiates a new solar.
	 *
	 * @param year
	 *            the year
	 * @param month
	 *            the month
	 * @param day
	 *            the day
	 */
	public Solar(int year, int month, int day) {
		this.year = year;
		this.month = month;
		this.day = day;
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

	/*
	 * (non-Javadoc)
	 * 
	 * @see java.lang.Object#toString()
	 */
	@Override
	public String toString() {
		return year + "-" + month + "-" + day;
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
		Solar other = (Solar) obj;
		if (day != other.day)
			return false;
		if (month != other.month)
			return false;
		if (year != other.year)
			return false;
		return true;
	}

}