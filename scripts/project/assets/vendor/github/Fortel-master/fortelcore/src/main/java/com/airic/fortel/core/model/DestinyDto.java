package com.airic.fortel.core.model;

import java.io.Serializable;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.stream.Collectors;

import com.airic.fortel.core.destiny.config.Config.ConfigType;
import com.airic.fortel.core.model.Data.FiveElement;
import com.airic.fortel.core.model.Data.GroundTime;
import com.airic.fortel.core.model.Data.Sex;
import com.airic.fortel.core.model.Data.ShadowLight;
import com.airic.fortel.core.model.Data.StarEnergyLevel;
import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonAutoDetect.Visibility;

/**
 * The Class DestinyDto.
 */
@JsonAutoDetect(getterVisibility = Visibility.NONE, isGetterVisibility = Visibility.NONE, setterVisibility = Visibility.NONE, creatorVisibility = Visibility.NONE, fieldVisibility = Visibility.PUBLIC_ONLY)
public class DestinyDto implements Serializable {

	/** The Constant serialVersionUID. */
	private static final long serialVersionUID = 5610707686978177923L;

	/** The config type. */
	public final ConfigType configType;

	/** The sex. */
	public final Sex sex;

	/** The year sky. */
	public final Sky yearSky;

	/** The year ground. */
	public final Ground yearGround;

	/** The born year. */
	public final int bornYear;

	/** The born month. */
	public final int bornMonth;

	/** The born day. */
	public final int bornDay;

	/** The born time ground. */
	public final GroundTime bornTimeGround;

	/** The is double month. */
	public final boolean isDoubleMonth;

	/** The shadow light. */
	public final ShadowLight shadowLight;

	/** The five element. */
	public final FiveElement fiveElement;

	/** The five element number. */
	public final int fiveElementNumber;

	/** The cells. */
	public final List<Cell> cells;

	/** The destiny master. */
	public final Star destinyMaster;

	/** The body master. */
	public final Star bodyMaster;

	/** The son dou. */
	public final Ground sonDou;

	/** The star reaction map. */
	public final Map<String, Star> starReactionMap;

	/** The major star energy. */
	public final Map<MajorStar, StarEnergyLevel> majorStarEnergy;

	/** The path clockwise. */
	public final boolean pathClockwise;

	/** The destiny ground. */
	public final Ground destinyGround;

	/**
	 * Instantiates a new destiny dto.
	 *
	 * @param destiny
	 *            the destiny
	 */
	public DestinyDto(Destiny destiny) {
		this.configType = destiny.getConfig().getConfigType();
		this.sex = destiny.getConfig().getSex();
		this.yearSky = destiny.getConfig().getYearSky();
		this.yearGround = destiny.getConfig().getYearGround();
		this.bornYear = destiny.getConfig().getBornYear();
		this.bornMonth = destiny.getConfig().getBornMonth();
		this.bornDay = destiny.getConfig().getBornDay();
		this.bornTimeGround = destiny.getConfig().getBornTimeGround();
		this.isDoubleMonth = destiny.getConfig().isDoubleMonth();
		this.shadowLight = destiny.getShadowLight();
		this.fiveElement = destiny.getFiveElement();
		this.fiveElementNumber = destiny.getFiveElement().getNumber();
		this.cells = destiny.getCells();
		this.bodyMaster = destiny.getBodyMaster();
		this.destinyMaster = destiny.getDestinyMaster();
		this.destinyGround = destiny.getTempleCell(Temple.TEMPLE_BODY).getGround();

		this.starReactionMap = destiny.getStarReactionMap().entrySet().stream().collect(
				Collectors.<Entry<StarReaction, Star>, String, Star>toMap(entry -> entry.getKey().getDisplayName(),
						entry -> entry.getValue()));
		this.majorStarEnergy = destiny.getMajorStarEnergy();
		this.sonDou = destiny.getSonDou();

		this.pathClockwise = destiny.isPathClockwise();
	}
}
