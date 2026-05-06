package com.airic.fortel.core.util;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;
import java.util.function.BiFunction;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import com.airic.fortel.core.destiny.config.Config;
import com.airic.fortel.core.destiny.config.Config.ConfigType;
import com.airic.fortel.core.model.Cell;
import com.airic.fortel.core.model.Data.GroundTime;
import com.airic.fortel.core.model.Data.Sex;
import com.airic.fortel.core.model.Destiny;
import com.airic.fortel.core.model.Ground;
import com.airic.fortel.core.model.MajorStar;
import com.airic.fortel.core.model.MiniStar;
import com.airic.fortel.core.model.MinorStar;
import com.airic.fortel.core.model.Star;
import com.airic.fortel.core.model.StarElement;
import com.airic.fortel.core.model.StarReaction;
import com.airic.fortel.core.model.Temple;

/**
 * The Class DestinyCellCriteria.
 */
public class DestinyCellCriteria {

	/** The destiny. */
	private Destiny destiny = null;

	/** The base cell. */
	private Cell baseCell = null;

	/** The opposite cell. */
	private Cell oppositeCell = null;

	/** The left meet cell. */
	private Cell leftMeetCell = null;

	/** The right meet cell. */
	private Cell rightMeetCell = null;

	/** The prev cell. */
	private Cell prevCell = null;

	/** The next cell. */
	private Cell nextCell = null;

	/** The extended base opposite cells. */
	private List<Cell> extendedBaseOppositeCells = null;

	/** The extended base cells. */
	private List<Cell> extendedBaseCells = null;

	/** The extended opposite cells. */
	private List<Cell> extendedOppositeCells = null;

	/** The four cells. */
	private List<Cell> fourCells = null;

	/** The extended four cells. */
	private List<Cell> extendedFourCells = null;

	/** The extended four cells. */
	private List<Cell> neighborCells = null;

	/** The extended four cells. */
	private List<Cell> extendedNeighborCells = null;

	/** The extended prev cell. */
	private List<Cell> extendedPrevCell = null;

	/** The extended next cell. */
	private List<Cell> extendedNextCell = null;

	/** The context stack. */
	private LinkedList<Context> contextStack = new LinkedList<Context>();

	/** The current context. */
	private Context currentContext = new Context();

	/**
	 * The main method.
	 *
	 * @param args
	 *            the arguments
	 */
	public static void main(String[] args) {
		Config destinyConfig = new Config(ConfigType.GROUND, Sex.M, 1990, 3, 11, false,
				GroundTime.getByName("午").get());
		Destiny destiny = new Destiny(destinyConfig);

		/*
		 * 檢查命盤命宮(Temple.TEMPLE_DESTINY)是否: 會見廉貞, 並且同時"天魁或天鉞同宮"或"不見化忌"
		 */
		//@formatter:off
		boolean result = new DestinyCellCriteria(destiny, Temple.TEMPLE_DESTINY) //命宮
		    .and()
		        .meetStars(MajorStar.MAJOR_STAR_HONEST) //廉貞
		        .or()
		            .sameCellSomeStars(MinorStar.MINOR_STAR_HONOR, MinorStar.MINOR_STAR_HONOR2) //天魁或天鉞同宮
		            .notMeetStars(StarReaction.STAR_TO_PROBLEM) //不見化忌
		        .endOr()
		    .endAnd()
		    .getResult();

		//@formatter:on
		System.out.println(result);
		
		/*
		 * 檢查命盤命宮是否: 會見貪狼, 並且同時"文曲及龍池同宮"或"宮位在戌"
		 */
		//@formatter:off
		boolean result2 = new DestinyCellCriteria(destiny, Temple.TEMPLE_DESTINY) //命宮
		    .and()
		        .meetStars(MajorStar.MAJOR_STAR_GREED) //貪狼
		        .or()
		            .sameCellStars(MinorStar.MINOR_STAR_SKILL, MiniStar.MINI_STAR_DRAGON_SKILL) //文曲及龍池同宮
		            .isCellGrounds(Ground.getByDisplayName("戌").get()) //宮位在戌
		        .endOr()
		    .endAnd()
		    .getResult();

		//@formatter:on
		System.out.println(result2);
	}

	/**
	 * Instantiates a new destiny cell criteria.
	 *
	 * @param destiny
	 *            the destiny
	 */
	public DestinyCellCriteria(Destiny destiny) {
		this.destiny = destiny;
		this.setBaseTempleCell(Temple.TEMPLE_DESTINY);
	}

	/**
	 * Instantiates a new destiny cell criteria.
	 *
	 * @param destiny
	 *            the destiny
	 * @param cell
	 *            the cell
	 */
	public DestinyCellCriteria(Destiny destiny, Cell cell) {
		this.destiny = destiny;
		this.setBaseCell(cell);
	}

	/**
	 * Instantiates a new destiny cell criteria.
	 *
	 * @param destiny
	 *            the destiny
	 * @param temple
	 *            the temple
	 */
	public DestinyCellCriteria(Destiny destiny, Temple temple) {
		this.destiny = destiny;
		this.setBaseTempleCell(temple);
	}

	/**
	 * Instantiates a new destiny cell criteria.
	 *
	 * @param destiny
	 *            the destiny
	 * @param star
	 *            the star
	 */
	public DestinyCellCriteria(Destiny destiny, Star star) {
		this.destiny = destiny;
		this.setBaseStarCell(star);
	}

	/**
	 * Sets the base cell.
	 *
	 * @param baseCell
	 *            the base cell
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria setBaseCell(Cell baseCell) {
		if (this.baseCell != baseCell) {
			this.baseCell = baseCell;
			this.oppositeCell = baseCell.getNextICell(6).get();
			this.leftMeetCell = baseCell.getNextICell(4).get();
			this.rightMeetCell = baseCell.getPrevICell(4).get();
			this.prevCell = baseCell.getPrevCell();
			this.nextCell = baseCell.getNextCell();
			this.neighborCells = Arrays.asList(baseCell.getPrevCell(), baseCell.getNextCell());
			fourCells = Arrays.asList(this.baseCell, this.oppositeCell, this.leftMeetCell, this.rightMeetCell);

			Function<Cell, Stream<Cell>> extendedBaseCellMapper = cell -> {
				List<Cell> cells = new ArrayList<Cell>();
				cells.add(cell);
				List<Cell> extendedCells = cell.getBorrowCells().stream().map(borrowCell -> borrowCell.getCell())
						.collect(Collectors.toList());
				cells.addAll(extendedCells);
				return cells.stream();
			};

			extendedBaseCells = extendedBaseCellMapper.apply(baseCell).collect(Collectors.toList());
			extendedOppositeCells = extendedBaseCellMapper.apply(oppositeCell).collect(Collectors.toList());

			extendedBaseOppositeCells = Stream.concat(extendedBaseCells.stream(), extendedOppositeCells.stream())
					.collect(Collectors.toList());

			extendedFourCells = fourCells.stream().flatMap(extendedBaseCellMapper).collect(Collectors.toList());
			extendedPrevCell = extendedBaseCellMapper.apply(prevCell).collect(Collectors.toList());
			extendedNextCell = extendedBaseCellMapper.apply(nextCell).collect(Collectors.toList());
			extendedNeighborCells = neighborCells.stream().flatMap(extendedBaseCellMapper).collect(Collectors.toList());
		}
		return this;
	}

	/**
	 * Sets the base temple cell.
	 *
	 * @param temple
	 *            the temple
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria setBaseTempleCell(Temple temple) {
		return this.setBaseCell(destiny.getTempleCell(temple));
	}

	/**
	 * Sets the base star cell.
	 *
	 * @param star
	 *            the star
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria setBaseStarCell(Star star) {
		return this.setBaseCell(destiny.getStarCell(star));
	}

	/**
	 * Temple criteria.
	 *
	 * @param destiny
	 *            the destiny
	 * @param temple
	 *            the temple
	 * @return the destiny cell criteria
	 */
	public static DestinyCellCriteria templeCriteria(Destiny destiny, Temple temple) {
		return new DestinyCellCriteria(destiny, temple);
	}

	/**
	 * Star criteria.
	 *
	 * @param destiny
	 *            the destiny
	 * @param star
	 *            the star
	 * @return the destiny cell criteria
	 */
	public static DestinyCellCriteria starCriteria(Destiny destiny, Star star) {
		return new DestinyCellCriteria(destiny, star);
	}

	/**
	 * The Class Context.
	 */
	public static class Context {

		/** The results. */
		private List<Boolean> results = new ArrayList<Boolean>();

		/** The Collector function. */
		private Function<List<Boolean>, Boolean> CollectorFunction = null;

		/** The check skip function. */
		private Function<List<Boolean>, Boolean> checkSkipFunction = null;

		/**
		 * Instantiates a new context.
		 */
		public Context() {
			setCollectResultFunction(results -> {
				for (boolean result : results) {
					if (!result) {
						return false;
					}
				}
				return true;
			});

			setCheckSkipFunction(results -> {
				for (boolean result : results) {
					if (!result) {
						return true;
					}
				}
				return false;
			});
		}

		/**
		 * Adds the result.
		 *
		 * @param result
		 *            the result
		 * @return the context
		 */
		public Context addResult(boolean result) {
			this.results.add(result);
			return this;
		}

		/**
		 * Sets the collect result function.
		 *
		 * @param CollectorFunction
		 *            the collector function
		 */
		public void setCollectResultFunction(Function<List<Boolean>, Boolean> CollectorFunction) {
			this.CollectorFunction = CollectorFunction;
		}

		/**
		 * Sets the check skip function.
		 *
		 * @param checkSkipFunction
		 *            the check skip function
		 */
		public void setCheckSkipFunction(Function<List<Boolean>, Boolean> checkSkipFunction) {
			this.checkSkipFunction = checkSkipFunction;
		}

		/**
		 * Check skip.
		 *
		 * @return true, if successful
		 */
		public boolean checkSkip() {
			return checkSkipFunction.apply(results);
		}

		/**
		 * Evaluate.
		 *
		 * @return true, if successful
		 */
		public boolean evaluate() {
			return CollectorFunction.apply(results);
		}
	}

	/**
	 * And.
	 *
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria and() {
		contextStack.add(currentContext);
		currentContext = new Context();
		return this;
	}

	/**
	 * End and.
	 *
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria endAnd() {
		boolean collectedResult = currentContext.evaluate();
		currentContext = contextStack.pollLast();
		currentContext.addResult(collectedResult);
		return this;
	}

	/**
	 * Or.
	 *
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria or() {
		contextStack.add(currentContext);
		currentContext = new Context();
		currentContext.setCollectResultFunction(results -> {
			for (boolean result : results) {
				if (result) {
					return true;
				}
			}
			return false;
		});
		currentContext.setCheckSkipFunction(results -> {
			for (boolean result : results) {
				if (result) {
					return true;
				}
			}
			return false;
		});
		return this;
	}

	/**
	 * End or.
	 *
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria endOr() {
		boolean collectedResult = currentContext.evaluate();
		currentContext = contextStack.pollLast();
		currentContext.addResult(collectedResult);
		return this;
	}

	/**
	 * And functions.
	 *
	 * @param <T>
	 *            the generic type
	 * @param function
	 *            the function
	 * @param objects
	 *            the objects
	 * @return true, if successful
	 */
	private static <T> boolean andFunctions(Function<T, Boolean> function,
			@SuppressWarnings("unchecked") T... objects) {
		boolean match = true;
		for (T object : objects) {
			match = match && function.apply(object);
			if (!match) {
				return false;
			}
		}
		return match;
	}

	/**
	 * Or functions.
	 *
	 * @param <T>
	 *            the generic type
	 * @param function
	 *            the function
	 * @param objects
	 *            the objects
	 * @return true, if successful
	 */
	private static <T> boolean orFunctions(Function<T, Boolean> function, @SuppressWarnings("unchecked") T... objects) {
		for (T object : objects) {
			if (function.apply(object)) {
				return true;
			}
		}
		return false;
	}

	/**
	 * Gets the check function.
	 *
	 * @param <T>
	 *            the generic type
	 * @param <S>
	 *            the generic type
	 * @param evalFunction
	 *            the eval function
	 * @param ss
	 *            the ss
	 * @return the check function
	 */
	private static <T, S> Function<T, Boolean> getCheckFunction(BiFunction<T, S, Boolean> evalFunction, List<S> ss) {
		Function<T, Boolean> checkFunction = t -> {
			for (S s : ss) {
				if (evalFunction.apply(t, s)) {
					return true;
				}
			}
			return false;
		};
		return checkFunction;
	}

	/**
	 * Gets the check not function.
	 *
	 * @param <T>
	 *            the generic type
	 * @param <S>
	 *            the generic type
	 * @param evalFunction
	 *            the eval function
	 * @param ss
	 *            the ss
	 * @return the check not function
	 */
	private static <T, S> Function<T, Boolean> getCheckNotFunction(BiFunction<T, S, Boolean> evalFunction, List<S> ss) {
		Function<T, Boolean> checkFunction = t -> {
			for (S s : ss) {
				if (evalFunction.apply(t, s)) {
					return false;
				}
			}
			return true;
		};
		return checkFunction;
	}

	/**
	 * Gets the star cell eval function.
	 *
	 * @param destiny
	 *            the destiny
	 * @return the star cell eval function
	 */
	private static BiFunction<StarElement, Cell, Boolean> getStarCellEvalFunction(final Destiny destiny) {
		return (elem, cell) -> {
			if (elem instanceof Star) {
				return destiny.getStarCell((Star) elem) == cell;
			} else if (elem instanceof StarReaction) {
				return destiny.getReactionCell((StarReaction) elem) == cell;
			} else {
				return false;
			}
		};
	}

	/**
	 * Gets the temple cell eval function.
	 *
	 * @param destiny
	 *            the destiny
	 * @return the temple cell eval function
	 */
	private static BiFunction<Temple, Cell, Boolean> getTempleCellEvalFunction(final Destiny destiny) {
		return (temple, cell) -> {
			return destiny.getTempleCell(temple) == cell;
		};
	}

	/**
	 * Meet stars.
	 *
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria meetStars(StarElement... stars) {
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedFourCells);
		currentContext.addResult(andFunctions(checkFunction, stars));
		return this;
	}

	/**
	 * Meet some stars.
	 *
	 * @param starElements
	 *            the star elements
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria meetSomeStars(StarElement... starElements) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedFourCells);
		currentContext.addResult(orFunctions(checkFunction, starElements));
		return this;
	}

	/**
	 * Meet stars count gt.
	 *
	 * @param countThershold
	 *            the count thershold
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria meetStarsCountGt(int countThershold, StarElement... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		int count = 0;
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedFourCells);
		for (StarElement star : stars) {
			if (checkFunction.apply(star)) {
				count++;
			}
		}
		currentContext.addResult(count >= countThershold);
		return this;
	}

	/**
	 * Meet stars count lt.
	 *
	 * @param countThershold
	 *            the count thershold
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria meetStarsCountLt(int countThershold, StarElement... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		int count = 0;
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedFourCells);
		for (StarElement star : stars) {
			if (checkFunction.apply(star)) {
				count++;
			}
		}
		currentContext.addResult(count <= countThershold);
		return this;
	}

	/**
	 * Not meet stars count gt.
	 *
	 * @param countThershold
	 *            the count thershold
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria notMeetStarsCountGt(int countThershold, StarElement... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		int count = 0;
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedFourCells);
		for (StarElement star : stars) {
			if (!checkFunction.apply(star)) {
				count++;
			}
		}
		currentContext.addResult(count >= countThershold);
		return this;
	}

	/**
	 * Not meet stars count lt.
	 *
	 * @param countThershold
	 *            the count thershold
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria notMeetStarsCountLt(int countThershold, StarElement... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		int count = 0;
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedFourCells);
		for (StarElement star : stars) {
			if (!checkFunction.apply(star)) {
				count++;
			}
		}
		currentContext.addResult(count <= countThershold);
		return this;
	}

	/**
	 * Same cell stars count gt.
	 *
	 * @param countThershold
	 *            the count thershold
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria sameCellStarsCountGt(int countThershold, Star... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		int count = 0;
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedBaseCells);
		for (Star star : stars) {
			if (checkFunction.apply(star)) {
				count++;
			}
		}
		currentContext.addResult(count >= countThershold);
		return this;
	}

	/**
	 * Same cell stars count lt.
	 *
	 * @param countThershold
	 *            the count thershold
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria sameCellStarsCountLt(int countThershold, Star... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		int count = 0;
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedBaseCells);
		for (Star star : stars) {
			if (checkFunction.apply(star)) {
				count++;
			}
		}
		currentContext.addResult(count <= countThershold);
		return this;
	}

	/**
	 * Not same cell stars count gt.
	 *
	 * @param countThershold
	 *            the count thershold
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria notSameCellStarsCountGt(int countThershold, Star... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		int count = 0;
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedBaseCells);
		for (Star star : stars) {
			if (!checkFunction.apply(star)) {
				count++;
			}
		}
		currentContext.addResult(count >= countThershold);
		return this;
	}

	/**
	 * Not same cell stars count lt.
	 *
	 * @param countThershold
	 *            the count thershold
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria notSameCellStarsCountLt(int countThershold, Star... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		int count = 0;
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedBaseCells);
		for (Star star : stars) {
			if (!checkFunction.apply(star)) {
				count++;
			}
		}
		currentContext.addResult(count <= countThershold);
		return this;
	}

	/**
	 * Same cell stars count gt.
	 *
	 * @param countThershold
	 *            the count thershold
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria sameOrOppositeCellStarsCountGt(int countThershold, Star... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		int count = 0;
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedOppositeCells);
		for (Star star : stars) {
			if (checkFunction.apply(star)) {
				count++;
			}
		}
		currentContext.addResult(count >= countThershold);
		return this;
	}

	/**
	 * Same cell stars count lt.
	 *
	 * @param countThershold
	 *            the count thershold
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria sameOrOppositeCellStarsCountLt(int countThershold, Star... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		int count = 0;
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedOppositeCells);
		for (Star star : stars) {
			if (checkFunction.apply(star)) {
				count++;
			}
		}
		currentContext.addResult(count <= countThershold);
		return this;
	}

	/**
	 * Not same cell stars count gt.
	 *
	 * @param countThershold
	 *            the count thershold
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria notSameOrOppositeCellStarsCountGt(int countThershold, Star... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		int count = 0;
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedOppositeCells);
		for (Star star : stars) {
			if (!checkFunction.apply(star)) {
				count++;
			}
		}
		currentContext.addResult(count >= countThershold);
		return this;
	}

	/**
	 * Not same cell stars count lt.
	 *
	 * @param countThershold
	 *            the count thershold
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria notSameOrOppositeCellStarsCountLt(int countThershold, Star... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		int count = 0;
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedOppositeCells);
		for (Star star : stars) {
			if (!checkFunction.apply(star)) {
				count++;
			}
		}
		currentContext.addResult(count <= countThershold);
		return this;
	}

	/**
	 * Meet temples.
	 *
	 * @param temples
	 *            the temples
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria meetTemples(Temple... temples) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<Temple, Boolean> checkFunction = getCheckFunction(getTempleCellEvalFunction(destiny),
				extendedFourCells);
		currentContext.addResult(andFunctions(checkFunction, temples));
		return this;
	}

	/**
	 * Meet some temples.
	 *
	 * @param temples
	 *            the temples
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria meetSomeTemples(Temple... temples) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<Temple, Boolean> checkFunction = getCheckFunction(getTempleCellEvalFunction(destiny),
				extendedFourCells);
		currentContext.addResult(orFunctions(checkFunction, temples));
		return this;
	}

	/**
	 * Same or opposite cell stars.
	 *
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria sameOrOppositeCellStars(StarElement... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedBaseOppositeCells);
		currentContext.addResult(andFunctions(checkFunction, stars));
		return this;
	}

	/**
	 * Same or opposite cell some stars.
	 *
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria sameOrOppositeCellSomeStars(StarElement... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedBaseOppositeCells);
		currentContext.addResult(orFunctions(checkFunction, stars));
		return this;
	}

	/**
	 * Same or opposite cell temples.
	 *
	 * @param temples
	 *            the temples
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria sameOrOppositeCellTemples(Temple... temples) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<Temple, Boolean> checkFunction = getCheckFunction(getTempleCellEvalFunction(destiny),
				extendedBaseOppositeCells);
		currentContext.addResult(andFunctions(checkFunction, temples));
		return this;
	}

	/**
	 * Same or opposite cell some temples.
	 *
	 * @param temples
	 *            the temples
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria sameOrOppositeCellSomeTemples(Temple... temples) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<Temple, Boolean> checkFunction = getCheckFunction(getTempleCellEvalFunction(destiny),
				extendedBaseOppositeCells);
		currentContext.addResult(orFunctions(checkFunction, temples));
		return this;
	}

	/**
	 * Same cell stars.
	 *
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria sameCellStars(StarElement... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedBaseCells);
		currentContext.addResult(andFunctions(checkFunction, stars));
		return this;
	}

	/**
	 * Same cell some stars.
	 *
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria sameCellSomeStars(StarElement... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedBaseCells);
		currentContext.addResult(orFunctions(checkFunction, stars));
		return this;
	}

	/**
	 * Same cell temples.
	 *
	 * @param temples
	 *            the temples
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria sameCellTemples(Temple... temples) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<Temple, Boolean> checkFunction = getCheckFunction(getTempleCellEvalFunction(destiny),
				extendedBaseCells);
		currentContext.addResult(andFunctions(checkFunction, temples));
		return this;
	}

	/**
	 * Same cell some temples.
	 *
	 * @param temples
	 *            the temples
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria sameCellSomeTemples(Temple... temples) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<Temple, Boolean> checkFunction = getCheckFunction(getTempleCellEvalFunction(destiny),
				extendedBaseCells);
		currentContext.addResult(orFunctions(checkFunction, temples));
		return this;
	}

	/**
	 * Not meet stars.
	 *
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria notMeetStars(StarElement... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<StarElement, Boolean> checkFunction = getCheckNotFunction(getStarCellEvalFunction(destiny),
				extendedFourCells);
		currentContext.addResult(andFunctions(checkFunction, stars));
		return this;
	}

	/**
	 * Not meet some stars.
	 *
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria notMeetSomeStars(StarElement... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<StarElement, Boolean> checkFunction = getCheckNotFunction(getStarCellEvalFunction(destiny),
				extendedFourCells);
		currentContext.addResult(orFunctions(checkFunction, stars));
		return this;
	}

	/**
	 * Not meet temples.
	 *
	 * @param temples
	 *            the temples
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria notMeetTemples(Temple... temples) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<Temple, Boolean> checkFunction = getCheckNotFunction(getTempleCellEvalFunction(destiny),
				extendedFourCells);
		currentContext.addResult(andFunctions(checkFunction, temples));
		return this;
	}

	/**
	 * Not meet some temples.
	 *
	 * @param temples
	 *            the temples
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria notMeetSomeTemples(Temple... temples) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<Temple, Boolean> checkFunction = getCheckNotFunction(getTempleCellEvalFunction(destiny),
				extendedFourCells);
		currentContext.addResult(orFunctions(checkFunction, temples));
		return this;
	}

	/**
	 * Not same or opposite cell stars.
	 *
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria notSameOrOppositeCellStars(StarElement... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<StarElement, Boolean> checkFunction = getCheckNotFunction(getStarCellEvalFunction(destiny),
				extendedBaseOppositeCells);
		currentContext.addResult(andFunctions(checkFunction, stars));
		return this;
	}

	/**
	 * Not same or opposite cell some stars.
	 *
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria notSameOrOppositeCellSomeStars(StarElement... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<StarElement, Boolean> checkFunction = getCheckNotFunction(getStarCellEvalFunction(destiny),
				extendedBaseOppositeCells);
		currentContext.addResult(orFunctions(checkFunction, stars));
		return this;
	}

	/**
	 * Not same or opposite cell temples.
	 *
	 * @param temples
	 *            the temples
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria notSameOrOppositeCellTemples(Temple... temples) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<Temple, Boolean> checkFunction = getCheckNotFunction(getTempleCellEvalFunction(destiny),
				extendedBaseOppositeCells);
		currentContext.addResult(andFunctions(checkFunction, temples));
		return this;
	}

	/**
	 * Not same or opposite cell some temples.
	 *
	 * @param temples
	 *            the temples
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria notSameOrOppositeCellSomeTemples(Temple... temples) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<Temple, Boolean> checkFunction = getCheckNotFunction(getTempleCellEvalFunction(destiny),
				extendedBaseOppositeCells);
		currentContext.addResult(orFunctions(checkFunction, temples));
		return this;
	}

	/**
	 * Not same cell stars.
	 *
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria notSameCellStars(StarElement... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<StarElement, Boolean> checkFunction = getCheckNotFunction(getStarCellEvalFunction(destiny),
				extendedBaseCells);
		currentContext.addResult(andFunctions(checkFunction, stars));
		return this;
	}

	/**
	 * Not same cell some stars.
	 *
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria notSameCellSomeStars(StarElement... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<StarElement, Boolean> checkFunction = getCheckNotFunction(getStarCellEvalFunction(destiny),
				extendedBaseCells);
		currentContext.addResult(orFunctions(checkFunction, stars));
		return this;
	}

	/**
	 * Not same cell temples.
	 *
	 * @param temples
	 *            the temples
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria notSameCellTemples(Temple... temples) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<Temple, Boolean> checkFunction = getCheckNotFunction(getTempleCellEvalFunction(destiny),
				extendedBaseCells);
		currentContext.addResult(andFunctions(checkFunction, temples));
		return this;
	}

	/**
	 * Not same cell some temples.
	 *
	 * @param temples
	 *            the temples
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria notSameCellSomeTemples(Temple... temples) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<Temple, Boolean> checkFunction = getCheckNotFunction(getTempleCellEvalFunction(destiny),
				extendedBaseCells);
		currentContext.addResult(orFunctions(checkFunction, temples));
		return this;
	}

	/**
	 * Trapped by stars.
	 *
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria trappedByStars(StarElement... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<StarElement, Boolean> checkPrevCellFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedPrevCell);
		Function<StarElement, Boolean> checkNextCellFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedNextCell);
		for (StarElement star : stars) {
			if (!checkPrevCellFunction.apply(star) && !checkNextCellFunction.apply(star)) {
				currentContext.addResult(false);
			}
		}
		currentContext.addResult(true);
		return this;
	}

	/**
	 * Trapped by some stars.
	 *
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria trappedBySomeStars(StarElement... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<StarElement, Boolean> checkPrevCellFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedPrevCell);
		Function<StarElement, Boolean> checkNextCellFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedNextCell);
		boolean prevCellfound = false;
		boolean nextCellfound = false;
		for (StarElement star : stars) {
			if (checkPrevCellFunction.apply(star)) {
				prevCellfound = true;
				continue;
			}
			if (checkNextCellFunction.apply(star)) {
				nextCellfound = true;
				continue;
			}
			if (prevCellfound && nextCellfound) {
				break;
			}
		}
		currentContext.addResult(prevCellfound && nextCellfound);
		return this;
	}

	/**
	 * Besides stars.
	 *
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria besidesStars(StarElement... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedNeighborCells);
		currentContext.addResult(andFunctions(checkFunction, stars));
		return this;
	}

	/**
	 * Besides some stars.
	 *
	 * @param stars
	 *            the stars
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria besidesSomeStars(StarElement... stars) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedNeighborCells);
		currentContext.addResult(orFunctions(checkFunction, stars));
		return this;
	}

	/**
	 * Checks if is cell ground.
	 *
	 * @param grounds
	 *            the grounds
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria isCellGrounds(Ground... grounds) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<Ground, Boolean> checkFunction = (ground_) -> {
			return baseCell.getGround() == ground_;
		};
		currentContext.addResult(orFunctions(checkFunction, grounds));
		return this;
	}

	/**
	 * Checks if is not cell grounds.
	 *
	 * @param grounds
	 *            the grounds
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria isNotCellGrounds(Ground... grounds) {
		if (currentContext.checkSkip()) {
			return this;
		}
		Function<Ground, Boolean> checkFunction = (ground_) -> {
			return baseCell.getGround() != ground_;
		};
		currentContext.addResult(andFunctions(checkFunction, grounds));
		return this;
	}

	/**
	 * Checks if is not cell ground.
	 *
	 * @param ground
	 *            the ground
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria isNotCellGround(Ground ground) {
		if (currentContext.checkSkip()) {
			return this;
		}
		currentContext.addResult(baseCell.getGround() != ground);
		return this;
	}

	/**
	 * Adds the condition.
	 *
	 * @param result
	 *            the result
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria addCondition(boolean result) {
		if (currentContext.checkSkip()) {
			return this;
		}
		currentContext.addResult(result);
		return this;
	}

	/**
	 * Peek result.
	 *
	 * @return true, if successful
	 */
	public boolean peekResult() {
		if (!contextStack.isEmpty()) {
			throw new RuntimeException(
					"DestinyCellCriteria context stack is not empty. Please check correct usage of endAnd() and endOr().");
		}
		return currentContext.evaluate();
	}

	/**
	 * Gets the result.
	 *
	 * @return the result
	 */
	public boolean getResult() {
		boolean result = peekResult();
		resetCriteria();
		return result;
	}

	/**
	 * Clear criteria.
	 *
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria clearCriteria() {
		contextStack.clear();
		currentContext = new Context();
		return this;
	}

	/**
	 * Reset criteria.
	 *
	 * @return the destiny cell criteria
	 */
	public DestinyCellCriteria resetCriteria() {
		contextStack.clear();
		currentContext = new Context();
		this.setBaseTempleCell(Temple.TEMPLE_DESTINY);
		return this;
	}

	/*
	 * Below are some simple check functions which just for quick look up checking but no rebuilding criteria
	 */

	/**
	 * Check is meet stars.
	 *
	 * @param stars
	 *            the stars
	 * @return true, if successful
	 */
	public boolean checkIsMeetStars(StarElement... stars) {
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedFourCells);
		return andFunctions(checkFunction, stars);
	}

	/**
	 * Check is meet some stars.
	 *
	 * @param stars
	 *            the stars
	 * @return true, if successful
	 */
	public boolean checkIsMeetSomeStars(StarElement... stars) {
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedFourCells);
		return orFunctions(checkFunction, stars);
	}

	/**
	 * Check is not meet stars.
	 *
	 * @param stars
	 *            the stars
	 * @return true, if successful
	 */
	public boolean checkIsNotMeetStars(StarElement... stars) {
		return !checkIsMeetSomeStars(stars);
	}

	/**
	 * Check is not meet some stars.
	 *
	 * @param stars
	 *            the stars
	 * @return true, if successful
	 */
	public boolean checkIsNotMeetSomeStars(StarElement... stars) {
		return !checkIsMeetStars(stars);
	}

	/**
	 * Check is same cell stars.
	 *
	 * @param stars
	 *            the stars
	 * @return true, if successful
	 */
	public boolean checkIsSameCellStars(StarElement... stars) {
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedBaseCells);
		return andFunctions(checkFunction, stars);
	}

	/**
	 * Check is same cell some stars.
	 *
	 * @param stars
	 *            the stars
	 * @return true, if successful
	 */
	public boolean checkIsSameCellSomeStars(StarElement... stars) {
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedBaseCells);
		return orFunctions(checkFunction, stars);
	}

	/**
	 * Check is not same cell stars.
	 *
	 * @param stars
	 *            the stars
	 * @return true, if successful
	 */
	public boolean checkIsNotSameCellStars(StarElement... stars) {
		return !checkIsSameCellSomeStars(stars);
	}

	/**
	 * Check is not same cell some stars.
	 *
	 * @param stars
	 *            the stars
	 * @return true, if successful
	 */
	public boolean checkIsNotSameCellSomeStars(StarElement... stars) {
		return !checkIsSameCellStars(stars);
	}

	/**
	 * Check is same or opposite cell stars.
	 *
	 * @param stars
	 *            the stars
	 * @return true, if successful
	 */
	public boolean checkIsSameOrOppositeCellStars(StarElement... stars) {
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedOppositeCells);
		return andFunctions(checkFunction, stars);
	}

	/**
	 * Check is same or opposite cell some stars.
	 *
	 * @param stars
	 *            the stars
	 * @return true, if successful
	 */
	public boolean checkIsSameOrOppositeCellSomeStars(StarElement... stars) {
		Function<StarElement, Boolean> checkFunction = getCheckFunction(getStarCellEvalFunction(destiny),
				extendedOppositeCells);
		return orFunctions(checkFunction, stars);
	}

	/**
	 * Check is not same or opposite cell stars.
	 *
	 * @param stars
	 *            the stars
	 * @return true, if successful
	 */
	public boolean checkIsNotSameOrOppositeCellStars(StarElement... stars) {
		return !checkIsSameOrOppositeCellSomeStars(stars);
	}

	/**
	 * Check is not same or opposite cell some stars.
	 *
	 * @param stars
	 *            the stars
	 * @return true, if successful
	 */
	public boolean checkIsNotSameOrOppositeCellSomeStars(StarElement... stars) {
		return !checkIsSameOrOppositeCellStars(stars);
	}
}
