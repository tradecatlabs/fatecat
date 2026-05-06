#pragma once
/* #import "CLunarCal.dll"
#include <comdef.h>*/
#include "math.h"

#include "ChineseCalConv.h"

// using namespace CLunarCal;

class Constants
{
public:
	enum eElements 
	{
		Undefined = -1,
		Wood = 0,
		Fire = 1,
		Earth = 2,
		Metal = 3,
		Water = 4
	};

	 static char* months[];
	 static char* animals[];
	 static char* branches[];
	 static char* stems[];
	 static char* palaces[];
	 static char* elements[];
	 static char* minorStarNames[];
	 static char* northStarNames[];
	 static char* southStarNames[];

	 static char* minorStarNamesEng[];
	 static char* northStarNamesEng[];
	 static char* southStarNamesEng[];
	
	 static char* constellations[];
	 static int northStarsNum;
	 static int	southStarsNum;
	 static int minorStarsNum;
	 static int majorStarsNum;
};

 class BirthDate
{
public:
	BirthDate()
	{
	}

	 BirthDate(int year, int month, int day, int hour, int min, int timeZone)
	{
		this->year = year;
		this->month = month;
		this->day = day;
		this->hour = hour;
		this->min = min;
		this->timeZone = timeZone;
	}

	 int year;
	 int month;
	 int day;
	 int hour;
	 int min;
	 int timeZone;
};

 class SunDate : public BirthDate
 {
 public:
	 SunDate(int year, int month, int day, int hour, int min, int timeZone) : BirthDate(year, month, day, hour, min, timeZone)
	 {
		 showYear = year;
		 showMonth = month;
		 showDay = day;
		 showHour = hour;
		 showMin = min;
	 }

 public:
	 int showYear;
	 int showMonth;
	 int showDay;
	 int showHour;
	 int showMin;
 };

 class MoonDate : public BirthDate
 {
 public:
     MoonDate()
	 {
	 }

	bool Initialize(BirthDate& sunDate, CString& errorMessage, char* resData);
 };

//////////////////////////////////////////////////////////////////////////////////////////////
class BirthCharacters
{
public:

	BirthCharacters()
	{
		yearStem = 0;
		yearBranch = 0;
		monthStem = 0;
		monthBranch = 0;
		dayStem = 0;
		dayBranch = 0;
		hourStem = 0;
		hourBranch = 0;
	}

	BirthCharacters(SunDate& sunDate, MoonDate& moonDate)
	{
		// year
		int tempYearBranch = (moonDate.year - 52) % 12;
		this->yearBranch = tempYearBranch;

		int tempYearStem = (moonDate.year - 4) % 10;
		this->yearStem = tempYearStem;

		// month (+1 because month branches start from yin)
		int tempMonthBranch = (moonDate.month + 1) % 12;
		this->monthBranch = tempMonthBranch;

		// +1 because month stems start from ping; -1 since it starts from 0
		int tempMonthStem = (tempYearStem * 12 + moonDate.month + 1) % 10;
		this->monthStem = tempMonthStem;

		// day
		// 11 jan 1924 is the first day
		// COleDateTime dtZero(1924, 2, 15, 0, 0, 0);
		COleDateTime dtZero(1884, 9, 11, 0, 0, 0);
		COleDateTime dtBirth((int) sunDate.year, (int) sunDate.month, (int) sunDate.day, 0, 0, 0);
		COleDateTimeSpan timeDif = dtBirth - dtZero;
		long tempTimeDif = timeDif.GetDays();

		long tempDayBranch = tempTimeDif % 12;
		long tempDayStem = tempTimeDif % 10;
		this->dayBranch = tempDayBranch;
		this->dayStem = tempDayStem;

		// hour 0; 
		
		int tempHour = (((moonDate.hour + 1) - ((moonDate.hour + 1) % 2)) / 2) % 12;
		int tempHourBranch = tempHour;
		this->hourBranch = tempHourBranch;

		int tempHourStem = (tempDayStem * 12 + tempHour + 0) % 10;
		this->hourStem = tempHourStem;
	}

	 int yearStem;
	 int yearBranch;
	 int monthStem;
	 int monthBranch;
	 int dayStem;
	 int dayBranch;
	 int hourStem;
	 int hourBranch;
};

//////////////////////////////////////////////////////////////////////////////////////////////
class TzuWeiCalc
{
private:
	void Initialize()
	{

	    m_ming = 0;
		m_elem = Constants::eElements::Undefined;

		int i = 0;
		
		for (i = 0; i < Constants::northStarsNum; i++)
			m_northStars[i] = 0;
		
		for (i = 0; i < Constants::southStarsNum; i++)
			m_southStars[i] = 0;
		
		for (i = 0; i < Constants::minorStarsNum; i++)
			m_minorStars[i] = 0;

		for (i = 0; i < Constants::majorStarsNum; i++)
			m_borrowedStars[i] = false;

		for (i = 0; i < 4; i++)
			m_transformingStars[i] = 0;
		
		for (i = 0; i < 5; i++)
			m_elementWeights[i] = 0;

		return;
	}

public:

	TzuWeiCalc()
	{
		this->Initialize();

	}
	
	void calcBorrowedStars();
	static void calcGreatLimits(Constants::eElements elem, int yearStem, bool bMale, int palace, int* limit);
	static void calcElementsWeight(BirthCharacters chars, int* arrWeights);
	static void calcElementsForStemBranch(int stem, int branch, int* arrWeights);

	// initiates the tzu-wei class
	TzuWeiCalc(BirthCharacters& chars, BirthDate& sunDate, BirthDate& moonDate, bool bMale) 
	{
		this->Initialize();

		m_ming = TzuWeiCalc::calcMing(chars);

		Constants::eElements tempElem = TzuWeiCalc::calcElement(chars, m_ming);
		m_elem = tempElem;

		// m_tzuWeiLoc = tempTzuWeiLoc;
		TzuWeiCalc::calcNorthStars(tempElem, moonDate, m_northStars);
		TzuWeiCalc::calcSouthStars(m_northStars[0], m_southStars);

		TzuWeiCalc::calcMinorStars(chars, m_minorStars[0], m_minorStars[1], m_minorStars[2], m_minorStars[3], m_minorStars[4], m_minorStars[5], 
										  m_minorStars[6], m_minorStars[7], m_minorStars[8], m_minorStars[9], m_minorStars[10], m_minorStars[11], 
										  m_minorStars[12], m_minorStars[13], m_minorStars[14], m_minorStars[15], m_minorStars[16], m_minorStars[17],
										  m_minorStars[18]);

		// removed for now
		// TzuWeiCalc::calcTransformingStars(chars, m_northStars, m_southStars, m_minorStars[2], m_minorStars[3], m_transformingStars);

		calcBorrowedStars();
		calcElementsWeight(chars, m_elementWeights);
		for (int i = 0; i < 12; i++)
		{
			calcGreatLimits(tempElem, chars.yearStem, bMale, i, &(m_limits[i]));
		}

		calcConstellation(sunDate, &m_constellation);
	}

	// returns the location (earthly branch) of a specific palace
	 int getPalace(int palace)
	{
		int tempPalaceLocation = (m_ming + palace + 1) % 12;
		return tempPalaceLocation;
	}

	Constants::eElements getElement()
	{
		return m_elem;
	}
	
	// start calculations
	static int calcMing(BirthCharacters& chars)
	{
		return (12 + chars.monthBranch - chars.hourBranch) % 12;
	}

	static Constants::eElements calcElement(BirthCharacters& chars, int mingLoc);
	static int calcTzuWei(Constants::eElements elem, BirthDate& myMoonDate);

	// calculate Tzu Wei and 5 north stars
	static void calcNorthStars(Constants::eElements elem, BirthDate& moonDate, int* northStars)
	{
		// calculate Tzu Wei Loc
		int tzuWeiLoc = TzuWeiCalc::calcTzuWei(elem, moonDate);
		northStars[0] = tzuWeiLoc;

		const int northStarShift[] = {11, 9, 8, 7, 4};
		for (int i = 1; i < 6; i++)
			northStars[i] = (tzuWeiLoc + northStarShift[i - 1]) % 12;
	}

	// calculate Tien Fu and 7 south stars
	static void calcSouthStars(int tzuWeiLoc, int* southStars)
	{
		int tienFu = ((11 - tzuWeiLoc) + 5) % 12;
		southStars[0] = tienFu;

		const int southStarShift[] = {1, 2, 3, 4, 5, 6, 10};
		
		for (int i = 1; i < 8; i++)
			southStars[i] = (tienFu + southStarShift[i - 1]) % 12;
	}

	static void calcMinorStars(BirthCharacters& birthChars, 
					int& fireStar, int& ringingStar, int& literaryStar1, int& literaryStar2,
					int& sheepBladeStar, int& humpBackStar, 
					int& yearlyStar1, int& yearlyStar2, int& yearlyStar3,
					int& monthlyStar1, int& monthlyStar2, int& monthlyStar3,
					int& hourlyStar1, int& hourlyStar2,
					int& miscYearlyStar1, int& miscYearlyStar2, int& miscYearlyStar3,
					int& miscMonthlyStar1, int& miscMonthlyStar2
					);
	
	static void calcTransformingStars(BirthCharacters& birthChars, int* northStars, int* southStars, 
									  int literary1, int literary2,	int* transStars);
	
	static void calcConstellation(BirthDate sunDate, int* constellation)
	{
		// this is the first crocodile day
		// COleDateTime dtZero(1924, 2, 21, 0, 0, 0);
		COleDateTime dtZero(1864, 1, 14, 0, 0, 0);
		COleDateTime dtBirth((int) sunDate.year, (int) sunDate.month, (int) sunDate.day, 0, 0, 0);
		COleDateTimeSpan timeDif = dtBirth - dtZero;
		long tempTimeDif = timeDif.GetDays();

		*constellation = tempTimeDif % 28;
	}
	// end calculations
	
	//members
	 int					m_ming;
	 Constants::eElements	m_elem;
	 int					m_northStars[6];
	 int					m_southStars[8];
	 int					m_minorStars[19];
	 int					m_transformingStars[4];
	 // for now - north and south stars are included
	 bool					m_borrowedStars[14];
	 int					m_elementWeights[5];
	 int					m_limits[12];
	 int					m_constellation;
};

// designed to hold all classes that contain information on a person
class TzuWeiFullInfo
{
public:
	TzuWeiFullInfo(CString name, bool gender,
				    SunDate* sunDate, MoonDate* moonDate, 
					BirthCharacters* birthChars, TzuWeiCalc* tzuWeiCalc)
	{
		m_name = name;
		m_male = gender;
		m_sunDate = sunDate;
		m_moonDate = moonDate;
		m_birthChars = birthChars;
		m_tzuWeiCalc = tzuWeiCalc;
	}

	~TzuWeiFullInfo()
	{
		if (m_sunDate)
			delete m_sunDate;

		if (m_moonDate)
			delete m_moonDate;

		if (m_birthChars)
			delete m_birthChars;

		if (m_tzuWeiCalc)
			delete m_tzuWeiCalc;
	}
public:
	CString m_name;
	bool    m_male;
	SunDate* m_sunDate;
	MoonDate* m_moonDate;
	BirthCharacters* m_birthChars;
	TzuWeiCalc* m_tzuWeiCalc;
};
