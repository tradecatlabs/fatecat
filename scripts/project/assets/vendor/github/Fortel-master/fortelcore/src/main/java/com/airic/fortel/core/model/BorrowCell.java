package com.airic.fortel.core.model;

import java.io.Serializable;

/**
 * The Class BorrowCell.
 */
public class BorrowCell implements Serializable {

	/** The Constant serialVersionUID. */
	private static final long serialVersionUID = 2058275698889701929L;

	/** The cell ratio. */
	private float cellRatio = 0;

	/** The cell. */
	private Cell cell = null;

	/**
	 * Instantiates a new borrow cell.
	 *
	 * @param cellRatio
	 *            the cell ratio
	 * @param cell
	 *            the cell
	 */
	public BorrowCell(float cellRatio, Cell cell) {
		super();
		this.cellRatio = cellRatio;
		this.cell = cell;
	}

	/**
	 * Gets the cell ratio.
	 *
	 * @return the cell ratio
	 */
	public float getCellRatio() {
		return cellRatio;
	}

	/**
	 * Sets the cell ratio.
	 *
	 * @param cellRatio
	 *            the new cell ratio
	 */
	public void setCellRatio(float cellRatio) {
		this.cellRatio = cellRatio;
	}

	/**
	 * Gets the cell.
	 *
	 * @return the cell
	 */
	public Cell getCell() {
		return cell;
	}

	/**
	 * Sets the cell.
	 *
	 * @param cell
	 *            the new cell
	 */
	public void setCell(Cell cell) {
		this.cell = cell;
	}
}
