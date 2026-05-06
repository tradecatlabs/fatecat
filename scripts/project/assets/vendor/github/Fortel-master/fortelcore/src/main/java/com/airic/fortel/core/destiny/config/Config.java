package com.airic.fortel.core.destiny.config;

import java.io.Serializable;
import java.util.List;
import java.util.Optional;

import com.airic.fortel.core.calendar.util.Lunar;
import com.airic.fortel.core.calendar.util.LunarUtil;
import com.airic.fortel.core.calendar.util.Solar;
import com.airic.fortel.core.model.Data.DoubleMonth;
import com.airic.fortel.core.model.Data.GroundTime;
import com.airic.fortel.core.model.Data.Sex;
import com.airic.fortel.core.model.Destiny;
import com.airic.fortel.core.model.Ground;
import com.airic.fortel.core.model.MajorStar;
import com.airic.fortel.core.model.Sky;
import com.airic.fortel.core.model.Temple;
import com.airic.fortel.core.util.CommonUtil;
import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonAutoDetect.Visibility;
import com.fasterxml.jackson.annotation.JsonValue;

/**
 * The Class Config.
 *
 * @author Eric Yu
 */
@JsonAutoDetect(getterVisibility = Visibility.NONE, isGetterVisibility = Visibility.NONE, setterVisibility = Visibility.NONE, creatorVisibility = Visibility.NONE, fieldVisibility = Visibility.ANY)
public class Config implements Cloneable, Serializable {

	/** The Constant serialVersionUID. */
	private static final long serialVersionUID = 6615989785197922633L;

	/** The config type. */
	private ConfigType configType;

	/** The sex. */
	private Sex sex;

	/** The year sky. */
	private Sky yearSky;

	/** The year ground. */
	private Ground yearGround;
	
	/** The month sky. */
	private Sky monthSky;

	/** The month ground. */
	private Ground monthGround;
	
	/** The day sky. */
	private Sky daySky;

	/** The day ground. */
	private Ground dayGround;

	/** The born year. */
	private int bornYear;

	/** The born month. */
	private int bornMonth;

	/** The born day. */
	private int bornDay;

	/** The born time ground. */
	private GroundTime bornTimeGround;

	/** The is double month. */
	private boolean isDoubleMonth;

	public Config() {
	}
	
	/**
	 * Instantiates a new config.
	 *
	 * @param configType
	 *            the config type
	 * @param sex
	 *            the sex
	 * @param bornYear
	 *            the born year
	 * @param bornMonth
	 *            the born month
	 * @param bornDay
	 *            the born day
	 * @param isDoubleMonth
	 *            the is double month
	 * @param bornTimeGround
	 *            the born time ground
	 */
	public Config(ConfigType configType, Sex sex, int bornYear, int bornMonth, int bornDay, boolean isDoubleMonth,
			Sky yearSky, Ground yearGround,
			Sky monthSky, Ground monthGround,
			Sky daySky, Ground dayGround,
			GroundTime bornTimeGround) {
		super();
		this.configType = configType;
		this.sex = sex;
		this.bornYear = bornYear;
		this.bornMonth = bornMonth;
		this.bornDay = bornDay;
		this.bornTimeGround = bornTimeGround;
		this.isDoubleMonth = isDoubleMonth;
		
		this.yearSky = yearSky;
		this.yearGround = yearGround;
		this.monthSky = monthSky;
		this.monthGround = monthGround;
		this.daySky = daySky;
		this.dayGround = dayGround;
	}
	
	public Config(ConfigType configType, Sex sex, int bornYear, int bornMonth, int bornDay, boolean isDoubleMonth,
			GroundTime bornTimeGround) {
		super();
		this.configType = configType;
		this.sex = sex;
		this.bornYear = bornYear;
		setupYearSkyGround();
		this.bornMonth = bornMonth;
		this.bornDay = bornDay;
		this.bornTimeGround = bornTimeGround;
		this.isDoubleMonth = isDoubleMonth;
	}
	
	/**
	 * To short string.
	 *
	 * @return the string
	 */
	public String toShortString() {
		StringBuilder sb = new StringBuilder();
		return sb.append(new Lunar(bornYear, bornMonth, bornDay, isDoubleMonth).toString()).append("，")
				.append(bornTimeGround.getDisplayName()).append("時").append(configType.getDisplayName())
				.append(sex.getDisplayName()).toString();
	}

	/**
	 * Gets the born time description.
	 *
	 * @return the born time description
	 */
	public String getBornTimeDescription() {
		StringBuilder sb = new StringBuilder();

		switch (configType) {
		case GROUND:
			sb.append(bornTimeGround.getStartHour() < 10 ? "0" : "").append(bornTimeGround.getStartHour())
					.append(":00-").append(bornTimeGround.getStartHour() < 10 ? "0" : "")
					.append(bornTimeGround.getStartHour()).append(":15");
			break;
		case SKY:
			sb.append(bornTimeGround.getStartHour() < 10 ? "0" : "").append(bornTimeGround.getStartHour())
					.append(":15-").append(bornTimeGround.getEndHour() - 1 < 10 ? "0" : "")
					.append(bornTimeGround.getEndHour() - 1).append(":45");
			break;
		case HUMAN:
			sb.append(bornTimeGround.getEndHour() - 1 < 10 ? "0" : "").append(bornTimeGround.getEndHour() - 1)
					.append(":45-").append(bornTimeGround.getEndHour() < 10 ? "0" : "")
					.append(bornTimeGround.getEndHour()).append(":00");
			break;
		default:
			break;
		}
		return sb.toString();
	}

	/**
	 * To short string with time.
	 *
	 * @return the string
	 */
	public String toShortStringWithTime() {
		StringBuilder sb = new StringBuilder();
		return sb.append(new Lunar(bornYear, bornMonth, bornDay, isDoubleMonth).toString()).append("，")
				.append(bornTimeGround.getDisplayName()).append("時").append(configType.getDisplayName())
				.append(sex.getDisplayName()).append(" (").append(getBornTimeDescription()).append(")").toString();
	}

	/**
	 * To date short string.
	 *
	 * @return the string
	 */
	public String toDateShortString() {
		StringBuilder sb = new StringBuilder();
		return sb.append(new Lunar(bornYear, bornMonth, bornDay, isDoubleMonth).toString()).append(sex.getDisplayName())
				.toString();
	}

	/**
	 * Gets the basic destiny type.
	 *
	 * @return the basic destiny type
	 */
	public int getBasicDestinyType() {
		Destiny destiny = new Destiny(this);
		return MajorStar.MAJOR_STAR_EMPEROR.getGround(destiny).getIndex() + 1;
	}

	/**
	 * Setup year sky ground.
	 */
	private void setupYearSkyGround() {
		int yearSeq = CommonUtil.mod(bornYear % 60 - 4, 60);
		this.yearSky = Sky.getByIndex(yearSeq % 10);
		this.yearGround = Ground.getByIndex(yearSeq % 12);
	}

	/**
	 * Gets the config type.
	 *
	 * @return the config type
	 */
	public ConfigType getConfigType() {
		return configType;
	}

	/**
	 * Sets the config type.
	 *
	 * @param configType
	 *            the new config type
	 */
	public void setConfigType(ConfigType configType) {
		this.configType = configType;
	}

	/**
	 * Gets the sex.
	 *
	 * @return the sex
	 */
	public Sex getSex() {
		return sex;
	}

	/**
	 * Sets the sex.
	 *
	 * @param sex
	 *            the new sex
	 */
	public void setSex(Sex sex) {
		this.sex = sex;
	}

	/**
	 * Gets the born year.
	 *
	 * @return the born year
	 */
	public int getBornYear() {
		return bornYear;
	}

	/**
	 * Sets the born year.
	 *
	 * @param bornYear
	 *            the new born year
	 */
	public void setBornYear(int bornYear) {
		this.bornYear = bornYear;
		setupYearSkyGround();
	}

	/**
	 * Gets the year sky.
	 *
	 * @return the year sky
	 */
	public Sky getYearSky() {
		return yearSky;
	}


	public void setYearSky(Sky yearSky) {
		this.yearSky = yearSky;
	}
	
	/**
	 * Gets the year ground.
	 *
	 * @return the year ground
	 */
	public Ground getYearGround() {
		return yearGround;
	}

	public void setYearGround(Ground yearGround) {
		this.yearGround = yearGround;
	}
	
	public Sky getMonthSky() {
		return monthSky;
	}

	public void setMonthSky(Sky monthSky) {
		this.monthSky = monthSky;
	}

	public Ground getMonthGround() {
		return monthGround;
	}

	public void setMonthGround(Ground monthGround) {
		this.monthGround = monthGround;
	}

	public Sky getDaySky() {
		return daySky;
	}

	public void setDaySky(Sky daySky) {
		this.daySky = daySky;
	}

	public Ground getDayGround() {
		return dayGround;
	}

	public void setDayGround(Ground dayGround) {
		this.dayGround = dayGround;
	}

	/**
	 * Gets the born month.
	 *
	 * @return the born month
	 */
	public int getBornMonth() {
		return bornMonth;
	}

	/**
	 * Gets the checked double month valid month.
	 *
	 * @return the checked double month valid month
	 */
	public int getDoubleMonthLogicalMonth() {
		
		if (this.isDoubleMonth && this.getBornDay() > 15) {
			return this.bornMonth + 1;
		} else {
			return this.bornMonth;
		}
		
	}
	
	/**
	 * Sets the born month.
	 *
	 * @param bornMonth
	 *            the new born month
	 */
	public void setBornMonth(int bornMonth) {
		this.bornMonth = bornMonth;
	}

	/**
	 * Gets the born day.
	 *
	 * @return the born day
	 */
	public int getBornDay() {
		return bornDay;
	}

	/**
	 * Sets the born day.
	 *
	 * @param bornDay
	 *            the new born day
	 */
	public void setBornDay(int bornDay) {
		this.bornDay = bornDay;
	}

	/**
	 * Gets the born time ground.
	 *
	 * @return the born time ground
	 */
	public GroundTime getBornTimeGround() {
		return bornTimeGround;
	}

	/**
	 * Sets the born time ground.
	 *
	 * @param bornTimeGround
	 *            the new born time ground
	 */
	public void setBornTimeGround(GroundTime bornTimeGround) {
		this.bornTimeGround = bornTimeGround;
	}

	/**
	 * Checks if is double month.
	 *
	 * @return true, if is double month
	 */
	public boolean isDoubleMonth() {
		return isDoubleMonth;
	}

	/**
	 * Sets the double month.
	 *
	 * @param isDoubleMonth
	 *            the new double month
	 */
	public void setDoubleMonth(boolean isDoubleMonth) {
		this.isDoubleMonth = isDoubleMonth;
	}

	/**
	 * Gets the lunar date.
	 *
	 * @return the lunar date
	 */
	public Lunar getLunarDate() {
		return new Lunar(bornYear, bornMonth, bornDay, isDoubleMonth);
	}

	/**
	 * The Enum ConfigType.
	 */
	public static enum ConfigType {

		/** The ground. */
		GROUND("地盤", "(出生時間為該時辰頭15分鐘)", "00", "15"),
		/** The sky. */
		SKY("天盤", "(出生時間為該時辰15分至1小時45分之間)", "15", "45"),
		/** The human. */
		HUMAN("人盤", "(出生時間為該時辰最尾15分鐘)", "45", "00");

		/** The display name. */
		private String displayName;

		/** The start minute. */
		private String startMinute;

		/** The end minute. */
		private String endMinute;

		/** The remarks. */
		private String remarks;

		/**
		 * Instantiates a new config type.
		 *
		 * @param displayName
		 *            the display name
		 * @param remarks
		 *            the remarks
		 * @param startMinute
		 *            the start minute
		 * @param endMinute
		 *            the end minute
		 */
		private ConfigType(String displayName, String remarks, String startMinute, String endMinute) {
			this.displayName = displayName;
			this.remarks = remarks;
			this.startMinute = startMinute;
			this.endMinute = endMinute;
		}

		/**
		 * Gets the display name.
		 *
		 * @return the display name
		 */
		@JsonValue
		public String getDisplayName() {
			return this.displayName;
		}

		/**
		 * Gets the remarks.
		 *
		 * @return the remarks
		 */
		public String getRemarks() {
			return remarks;
		}

		/**
		 * Gets the start minute.
		 *
		 * @return the start minute
		 */
		public String getStartMinute() {
			return startMinute;
		}

		/**
		 * Gets the end minute.
		 *
		 * @return the end minute
		 */
		public String getEndMinute() {
			return endMinute;
		}

		/**
		 * Gets the by name.
		 *
		 * @param name
		 *            the name
		 * @return the by name
		 */
		public static Optional<ConfigType> getByName(String name) {
			return Optional.ofNullable(name).flatMap(name_ -> {
				for (ConfigType configType : ConfigType.values()) {
					if (configType.name().equalsIgnoreCase(name_)) {
						return Optional.of(configType);
					}
				}
				return Optional.<ConfigType>empty();
			});
		}
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see java.lang.Object#clone()
	 */
	@Override
	public Config clone() {
		return new Config(this.configType, this.sex, this.bornYear, this.bornMonth, this.bornDay, this.isDoubleMonth,
				this.yearSky, this.yearGround,
				this.monthSky, this.monthGround,
				this.daySky, this.dayGround,
				this.bornTimeGround);
	}

	/**
	 * Gets the prev config.
	 *
	 * @return the prev config
	 */
	public Optional<Config> getPrevConfig() {
		Config newConfig = this.clone();

		if (this.getConfigType() == ConfigType.GROUND) {
			newConfig.setConfigType(ConfigType.HUMAN);
			newConfig.setBornTimeGround(this.getBornTimeGround().shift(-1));
			if (this.getBornTimeGround() == GroundTime.GROUND_0) {
				if (this.getBornDay() == 1) {
					Optional<Lunar> prevLunarDateOptional = LunarUtil.getPrevLunar(this.bornYear, this.bornMonth,
							this.bornDay, this.isDoubleMonth);
					if (!prevLunarDateOptional.isPresent()) {
						return Optional.empty();
					}
					Lunar prevLunarDate = prevLunarDateOptional.get();
					newConfig.setBornYear(prevLunarDate.getYear());
					newConfig.setBornMonth(prevLunarDate.getMonth());
					newConfig.setBornDay(prevLunarDate.getDay());
					newConfig.setDoubleMonth(prevLunarDate.isLeap());

				} else {
					newConfig.setBornDay(this.getBornDay() - 1);
				}
			}
		} else if (this.getConfigType() == ConfigType.SKY) {
			newConfig.setConfigType(ConfigType.GROUND);
		} else if (this.getConfigType() == ConfigType.HUMAN) {
			newConfig.setConfigType(ConfigType.SKY);
		}

		if (testConfigDateInRange(newConfig)) {
			return Optional.of(newConfig);
		} else {
			return Optional.empty();
		}
	}

	/**
	 * Gets the next config.
	 *
	 * @return the next config
	 */
	public Optional<Config> getNextConfig() {
		Config newConfig = this.clone();

		if (this.getConfigType() == ConfigType.GROUND) {
			newConfig.setConfigType(ConfigType.SKY);
		} else if (this.getConfigType() == ConfigType.SKY) {
			newConfig.setConfigType(ConfigType.HUMAN);
		} else if (this.getConfigType() == ConfigType.HUMAN) {
			newConfig.setConfigType(ConfigType.GROUND);
			newConfig.setBornTimeGround(this.getBornTimeGround().shift(1));

			if (this.getBornTimeGround() == GroundTime.GROUND_12) {
				Optional<Lunar> nextLunarDateOptional = LunarUtil.getNextLunar(this.bornYear, this.bornMonth,
						this.bornDay, this.isDoubleMonth);
				if (!nextLunarDateOptional.isPresent()) {
					return Optional.empty();
				}
				Lunar nextLunarDate = nextLunarDateOptional.get();
				if (nextLunarDate.getDay() == 1) {// next day is 初一=>today is
													// end of month
					newConfig.setBornYear(nextLunarDate.getYear());
					newConfig.setBornMonth(nextLunarDate.getMonth());
					newConfig.setBornDay(nextLunarDate.getDay());
					newConfig.setDoubleMonth(nextLunarDate.isLeap());
				} else {
					newConfig.setBornDay(this.getBornDay() + 1);
				}

			}
		}

		if (testConfigDateInRange(newConfig)) {
			return Optional.of(newConfig);
		} else {
			return Optional.empty();
		}
	}

	/**
	 * Gets the prev day config.
	 *
	 * @return the prev day config
	 */
	public Optional<Config> getPrevDayConfig() {
		Config newConfig = this.clone();
		Optional<Lunar> prevLunarDateOptional = LunarUtil.getPrevLunar(this.bornYear, this.bornMonth, this.bornDay,
				this.isDoubleMonth);
		if (prevLunarDateOptional.isPresent()) {
			Lunar prevLunarDate = prevLunarDateOptional.get();
			newConfig.setBornYear(prevLunarDate.getYear());
			newConfig.setBornMonth(prevLunarDate.getMonth());
			newConfig.setBornDay(prevLunarDate.getDay());
			newConfig.setDoubleMonth(prevLunarDate.isLeap());

			if (testConfigDateInRange(newConfig)) {
				return Optional.of(newConfig);
			}
		}

		return Optional.empty();
	}

	/**
	 * Gets the next day config.
	 *
	 * @return the next day config
	 */
	public Optional<Config> getNextDayConfig() {
		Config newConfig = this.clone();
		Optional<Lunar> nextLunarDateOptional = LunarUtil.getNextLunar(this.bornYear, this.bornMonth, this.bornDay,
				this.isDoubleMonth);
		if (nextLunarDateOptional.isPresent()) {
			Lunar nextLunarDate = nextLunarDateOptional.get();
			newConfig.setBornYear(nextLunarDate.getYear());
			newConfig.setBornMonth(nextLunarDate.getMonth());
			newConfig.setBornDay(nextLunarDate.getDay());
			newConfig.setDoubleMonth(nextLunarDate.isLeap());

			if (testConfigDateInRange(newConfig)) {
				return Optional.of(newConfig);
			}
		}

		return Optional.empty();
	}

	/**
	 * Find prev config filter by major.
	 *
	 * @param target
	 *            the target
	 * @return the optional
	 */
	public Optional<Config> findPrevConfigFilterByMajor(MajorStar target) {
		Optional<Config> temp = this.getPrevConfig();
		if (!temp.isPresent()) {
			return Optional.<Config>empty();
		}

		boolean found = false;
		while (!found) {
			Destiny destiny = new Destiny(temp.get());
			List<MajorStar> majorStars = destiny.getTempleCell(Temple.TEMPLE_DESTINY).getMajorStars();
			if (!majorStars.isEmpty()) {
				for (MajorStar majorStar : majorStars) {
					if (majorStar == target) {
						found = true;
						return temp;
					}
				}
			} else {
				majorStars = destiny.getTempleCell(Temple.TEMPLE_MOVE).getMajorStars();
				for (MajorStar majorStar : majorStars) {
					if (majorStar == target) {
						found = true;
						return temp;
					}
				}
			}

			temp = temp.get().getPrevConfig();
			if (!temp.isPresent() || !testConfigDateInRange(temp.get())) {
				return Optional.<Config>empty();
			}
		}

		return Optional.<Config>empty();
	}

	/**
	 * Find next config filter by major.
	 *
	 * @param target
	 *            the target
	 * @return the optional
	 */
	public Optional<Config> findNextConfigFilterByMajor(MajorStar target) {
		Optional<Config> temp = this.getNextConfig();
		if (!temp.isPresent()) {
			return Optional.<Config>empty();
		}

		boolean found = false;
		while (!found) {
			Destiny destiny = new Destiny(temp.get());
			List<MajorStar> majorStars = destiny.getTempleCell(Temple.TEMPLE_DESTINY).getMajorStars();
			if (!majorStars.isEmpty()) {
				for (MajorStar majorStar : majorStars) {
					if (majorStar == target) {
						found = true;
						return temp;
					}
				}
			} else {
				majorStars = destiny.getTempleCell(Temple.TEMPLE_MOVE).getMajorStars();
				for (MajorStar majorStar : majorStars) {
					if (majorStar == target) {
						found = true;
						return temp;
					}
				}
			}

			temp = temp.get().getNextConfig();
			if (!temp.isPresent() || !testConfigDateInRange(temp.get())) {
				return Optional.<Config>empty();
			}
		}

		return Optional.<Config>empty();
	}

	/**
	 * Test config date in range.
	 *
	 * @param solar
	 *            the solar
	 * @return true, if successful
	 */
	public static boolean testConfigDateInRange(Solar solar) {
		return LunarUtil.testDateInputValidRange(solar);
	}

	/**
	 * Test config date in range.
	 *
	 * @param lunar
	 *            the lunar
	 * @return true, if successful
	 */
	public static boolean testConfigDateInRange(Lunar lunar) {
		return LunarUtil.testDateInputValidRange(lunar);
	}

	/**
	 * Test config date in range.
	 *
	 * @param config
	 *            the config
	 * @return true, if successful
	 */
	public static boolean testConfigDateInRange(Config config) {
		return LunarUtil.testDateInputValidRange(
				new Lunar(config.getBornYear(), config.getBornMonth(), config.getBornDay(), config.isDoubleMonth()));
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + bornDay;
		result = prime * result + bornMonth;
		result = prime * result + ((bornTimeGround == null) ? 0 : bornTimeGround.hashCode());
		result = prime * result + bornYear;
		result = prime * result + ((configType == null) ? 0 : configType.hashCode());
		result = prime * result + ((dayGround == null) ? 0 : dayGround.hashCode());
		result = prime * result + ((daySky == null) ? 0 : daySky.hashCode());
		result = prime * result + (isDoubleMonth ? 1231 : 1237);
		result = prime * result + ((monthGround == null) ? 0 : monthGround.hashCode());
		result = prime * result + ((monthSky == null) ? 0 : monthSky.hashCode());
		result = prime * result + ((sex == null) ? 0 : sex.hashCode());
		result = prime * result + ((yearGround == null) ? 0 : yearGround.hashCode());
		result = prime * result + ((yearSky == null) ? 0 : yearSky.hashCode());
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Config other = (Config) obj;
		if (bornDay != other.bornDay)
			return false;
		if (bornMonth != other.bornMonth)
			return false;
		if (bornTimeGround != other.bornTimeGround)
			return false;
		if (bornYear != other.bornYear)
			return false;
		if (configType != other.configType)
			return false;
		if (dayGround != other.dayGround)
			return false;
		if (daySky != other.daySky)
			return false;
		if (isDoubleMonth != other.isDoubleMonth)
			return false;
		if (monthGround != other.monthGround)
			return false;
		if (monthSky != other.monthSky)
			return false;
		if (sex != other.sex)
			return false;
		if (yearGround != other.yearGround)
			return false;
		if (yearSky != other.yearSky)
			return false;
		return true;
	}

}
