package com.airic.fortel.core.model;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import org.apache.commons.lang3.builder.ReflectionToStringBuilder;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonAutoDetect.Visibility;
import com.fasterxml.jackson.annotation.JsonIgnore;

/**
 * The Class Cell.
 *
 * @author Eric Yu
 */
@JsonAutoDetect(getterVisibility = Visibility.NONE, isGetterVisibility = Visibility.NONE, setterVisibility = Visibility.NONE, creatorVisibility = Visibility.NONE, fieldVisibility = Visibility.ANY)
public final class Cell implements Serializable {

	/** The Constant serialVersionUID. */
	private static final long serialVersionUID = -2179393850461100703L;

	/** The sky. */
	private Sky sky;

	/** The ground. */
	private Ground ground;

	/** The temples. */
	private List<Temple> temples = new ArrayList<Temple>();

	/** The major stars. */
	private List<MajorStar> majorStars = new ArrayList<MajorStar>();

	/** The minor stars. */
	private List<MinorStar> minorStars = new ArrayList<MinorStar>();

	/** The mini stars. */
	private List<MiniStar> miniStars = new ArrayList<MiniStar>();

	/** The borrow cells. */
	@JsonIgnore
	private List<BorrowCell> borrowCells = new ArrayList<BorrowCell>();

	/** The pre general star. */
	private MiniStar preGeneralStar = null;

	/** The pre age star. */
	private MiniStar preAgeStar = null;

	/** The pre doctor star. */
	private MiniStar preDoctorStar = null;

	/** The age start. */
	private int ageStart;

	/** The age end. */
	private int ageEnd;

	/** The persist12. */
	private Persist12 persist12;

	/** The metadata. */
	private Map<String, String> metadata = new HashMap<String, String>();

	/** The prev cell. */
	@JsonIgnore
	private transient Cell prevCell = null;

	/** The next cell. */
	@JsonIgnore
	private transient Cell nextCell = null;

	/**
	 * Gets the sky.
	 *
	 * @return the sky
	 */
	public Sky getSky() {
		return sky;
	}

	/**
	 * Sets the sky.
	 *
	 * @param sky
	 *            the new sky
	 */
	public void setSky(Sky sky) {
		this.sky = sky;
	}

	/**
	 * Gets the ground.
	 *
	 * @return the ground
	 */
	public Ground getGround() {
		return ground;
	}

	/**
	 * Sets the ground.
	 *
	 * @param ground
	 *            the new ground
	 */
	public void setGround(Ground ground) {
		this.ground = ground;
	}

	/**
	 * Gets the temples.
	 *
	 * @return the temples
	 */
	public List<Temple> getTemples() {
		return temples;
	}

	/**
	 * Gets the major stars.
	 *
	 * @return the major stars
	 */
	public List<MajorStar> getMajorStars() {
		return majorStars;
	}

	/**
	 * Gets the minor stars.
	 *
	 * @return the minor stars
	 */
	public List<MinorStar> getMinorStars() {
		return minorStars;
	}

	/**
	 * Gets the mini stars.
	 *
	 * @return the mini stars
	 */
	public List<MiniStar> getMiniStars() {
		return miniStars;
	}

	/**
	 * Gets the pre general star.
	 *
	 * @return the pre general star
	 */
	public MiniStar getPreGeneralStar() {
		return preGeneralStar;
	}

	/**
	 * Sets the pre general star.
	 *
	 * @param preGeneralStar
	 *            the new pre general star
	 */
	public void setPreGeneralStar(MiniStar preGeneralStar) {
		this.preGeneralStar = preGeneralStar;
	}

	/**
	 * Gets the pre age star.
	 *
	 * @return the pre age star
	 */
	public MiniStar getPreAgeStar() {
		return preAgeStar;
	}

	/**
	 * Sets the pre age star.
	 *
	 * @param preAgeStar
	 *            the new pre age star
	 */
	public void setPreAgeStar(MiniStar preAgeStar) {
		this.preAgeStar = preAgeStar;
	}

	/**
	 * Gets the pre doctor star.
	 *
	 * @return the pre doctor star
	 */
	public MiniStar getPreDoctorStar() {
		return preDoctorStar;
	}

	/**
	 * Sets the pre doctor star.
	 *
	 * @param preDoctorStar
	 *            the new pre doctor star
	 */
	public void setPreDoctorStar(MiniStar preDoctorStar) {
		this.preDoctorStar = preDoctorStar;
	}

	/**
	 * Adds the star.
	 *
	 * @param star
	 *            the star
	 */
	public void addStar(Star star) {
		if (star instanceof MajorStar) {
			this.majorStars.add((MajorStar) star);
		} else if (star instanceof MinorStar) {
			this.minorStars.add((MinorStar) star);
		} else if (star instanceof MiniStar) {
			this.miniStars.add((MiniStar) star);
		}
	}

	/**
	 * Gets the borrow cells.
	 *
	 * @return the borrow cells
	 */
	public List<BorrowCell> getBorrowCells() {
		return borrowCells;
	}

	/**
	 * Sets the borrow cells.
	 *
	 * @param borrowCells
	 *            the new borrow cells
	 */
	public void setBorrowCells(List<BorrowCell> borrowCells) {
		this.borrowCells = borrowCells;
	}

	/**
	 * Gets the age begin.
	 *
	 * @return the age begin
	 */
	public int getAgeBegin() {
		return ageStart;
	}

	/**
	 * Sets the age start.
	 *
	 * @param ageStart
	 *            the new age start
	 */
	public void setAgeStart(int ageStart) {
		this.ageStart = ageStart;
	}

	/**
	 * Gets the age end.
	 *
	 * @return the age end
	 */
	public int getAgeEnd() {
		return ageEnd;
	}

	/**
	 * Sets the age end.
	 *
	 * @param ageEnd
	 *            the new age end
	 */
	public void setAgeEnd(int ageEnd) {
		this.ageEnd = ageEnd;
	}

	/**
	 * Gets the persist12.
	 *
	 * @return the persist12
	 */
	public Persist12 getPersist12() {
		return persist12;
	}

	/**
	 * Sets the persist12.
	 *
	 * @param periodLevel
	 *            the new persist12
	 */
	public void setPersist12(Persist12 periodLevel) {
		this.persist12 = periodLevel;
	}

	/**
	 * Gets the prev cell.
	 *
	 * @return the prev cell
	 */
	public Cell getPrevCell() {
		return prevCell;
	}

	/**
	 * Sets the prev cell.
	 *
	 * @param prevCell
	 *            the new prev cell
	 */
	public void setPrevCell(Cell prevCell) {
		this.prevCell = prevCell;
	}

	/**
	 * Gets the next cell.
	 *
	 * @return the next cell
	 */
	public Cell getNextCell() {
		return nextCell;
	}

	/**
	 * Sets the next cell.
	 *
	 * @param nextCell
	 *            the new next cell
	 */
	public void setNextCell(Cell nextCell) {
		this.nextCell = nextCell;
	}

	/**
	 * Gets the prev i cell.
	 *
	 * @param i
	 *            the i
	 * @return the prev i cell
	 */
	public Optional<Cell> getPrevICell(int i) {
		Cell pointer = this;
		for (int j = 0; j * j < i * i; j++) {
			Cell tempPointer = i > 0 ? pointer.prevCell : pointer.nextCell;
			if (tempPointer != null) {
				pointer = tempPointer;
			} else {
				return Optional.<Cell>empty();
			}
		}
		return Optional.ofNullable(pointer);
	}

	/**
	 * Gets the next i cell.
	 *
	 * @param i
	 *            the i
	 * @return the next i cell
	 */
	public Optional<Cell> getNextICell(int i) {
		Cell pointer = this;
		for (int j = 0; j * j < i * i; j++) {
			Cell tempPointer = i > 0 ? pointer.nextCell : pointer.prevCell;
			if (tempPointer != null) {
				pointer = tempPointer;
			} else {
				return Optional.<Cell>empty();
			}
		}
		return Optional.ofNullable(pointer);
	}

	/**
	 * Count cell prev dist.
	 *
	 * @param cell
	 *            the cell
	 * @return the int
	 */
	public int countCellPrevDist(Cell cell) {
		Cell pointer = this;
		for (int i = 0; i < Ground.COUNT; i++) {
			if (pointer.getGround() == cell.ground) {
				return i;
			} else {
				pointer = pointer.prevCell;
			}
		}
		return -1;
	}

	/**
	 * Count cell next dist.
	 *
	 * @param cell
	 *            the cell
	 * @return the int
	 */
	public int countCellNextDist(Cell cell) {
		Cell pointer = this;
		for (int i = 0; i < Ground.COUNT; i++) {
			if (pointer.getGround() == cell.ground) {
				return i;
			} else {
				pointer = pointer.nextCell;
			}
		}
		return -1;
	}

	/**
	 * Count cell closest dist.
	 *
	 * @param cell
	 *            the cell
	 * @return the int
	 */
	public int countCellClosestDist(Cell cell) {
		Cell pointer = this;
		for (int i = 0; i < Ground.COUNT; i++) {
			if (pointer.getGround() == cell.ground) {
				if (i <= 6) {
					return i;
				} else {
					return Ground.COUNT - i;
				}
			} else {
				pointer = pointer.nextCell;
			}
		}
		return -1;
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

	/**
	 * Gets the metadata.
	 *
	 * @return the metadata
	 */
	public Map<String, String> getMetadata() {
		return metadata;
	}

	/**
	 * Sets the metadata entry.
	 *
	 * @param key
	 *            the key
	 * @param value
	 *            the value
	 */
	public void setMetadataEntry(String key, String value) {
		this.metadata.put(key, value);
	}

	/**
	 * Gets the metadata value.
	 *
	 * @param key
	 *            the key
	 * @return the metadata value
	 */
	public Optional<String> getMetadataValue(String key) {
		return Optional.ofNullable(this.metadata.get(key));
	}
}
