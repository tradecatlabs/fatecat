#include "StdAfx.h"
#include ".\tzuwei.h"

char* Constants::months[] = {"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};
char* Constants::animals[] = {"Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"};
char* Constants::branches[] = {"Zi", "Chou", "Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "Yu", "Xu", "Hai"};
char* Constants::stems[] = {"Jia", "Yi", "Bing", "Ding", "Mou", "Ji", "Geng", "Xin", "Ren", "Guei"};
char* Constants::palaces[] = {"Ancestor", "Pleasure", "Property", "Officials", "Assistants", "Actions", "Health", "Wealth", "Offspring", "Marriage", "Youth", "Ming"};
char* Constants::elements[] = {"Wood", "Fire", "Earth", "Metal", "Water"};
char* Constants::minorStarNames[] = {"Huo Xing", "Ling Xing", "Wen Qu", "Wen Chang", "Yang Ren", "Tuo Luo",
									 "Tian Cun", "Tian Guei", "Tian Yui", "Zuo Fu", "You Bi", "Yi Ma",
									 "Tian Gong", "Di Jie", "Tian Hao", "Hong Luan", "Tian Xi", "Tian Yao", "Tian Xing"};
char* Constants::minorStarNamesEng[] = {"Fire Star", "Ringing Star", "Music Master", "Protocol Master", "Goat Blade", "Hump Back",
									 "Heavenly Store", "Heavenly Leader", "Heavenly Halberd", "Right Assistant", "Left Assistant", "Travelling Star",
									 "Celestial Void", "Earthly Loss", "Destroyer", "Red Phoenix", "Happiness", "Heavenly Beauty", "Heavenly Punishment"};
char* Constants::northStarNames[] = {"Zi Wei", "Tian Ji", "Tai Yang", "Wu Qu", "Tian Tong", "Lian Zhen"};
char* Constants::northStarNamesEng[] = {"Emperor", "State Oracle", "Secretary", "Generalissimo", "Vassal", "Young Bride"};
char* Constants::southStarNames[] = {"Tian Fu", "Tai Yin", "Tan Lang", "Ju Men", "Tian Xiang", "Tian Liang", "Qi Sha", "Po Jun"};
char* Constants::southStarNamesEng[] = {"Empress", "Moon Lady", "Greedy Wolf", "Great Gate", "Tutor", "Roofbeam", "Seven Killings", "Rebel"};
char* Constants::constellations[] = {"Crocodile", "Dragon", "Badger", "Hare", "Fox", "Tiger", "Leopard", "Griffon", "Ox", "Bat", "Rat", "Swallow", "Pig", "Porcupine",
									 "Wolf", "Dog", "Pheasant", "Cock", "Crow", "Monkey", "Gibbon", "Tapir", "Sheep", "Deer", "Horse", "Stag", "Serpent", "Earthworm"};

int   Constants::northStarsNum = 6;
int	  Constants::southStarsNum = 8;
int	  Constants::minorStarsNum = 19;
int	  Constants::majorStarsNum = 14;

void TzuWeiCalc::calcMinorStars(BirthCharacters& birthChars, 
					int& fireStar, int& ringingStar, int& literaryStar1, int& literaryStar2,
					int& sheepBladeStar, int& humpBackStar, 
					int& yearlyStar1, int& yearlyStar2, int& yearlyStar3,
					int& monthlyStar1, int& monthlyStar2, int& monthlyStar3,
					int& hourlyStar1, int& hourlyStar2,
					int& miscYearlyStar1, int& miscYearlyStar2, int& miscYearlyStar3,
					int& miscMonthlyStar1, int& miscMonthlyStar2
					)
	{
		const int fireStarShift[] = {2, 3, 1, 9};

		fireStar = (fireStarShift[birthChars.yearBranch % 4] + birthChars.hourBranch) % 12;

		const int ringingStarShift[] = {10, 10, 3, 10};

		ringingStar = (ringingStarShift[birthChars.yearBranch % 4] + birthChars.hourBranch) % 12;

		// Wen Chu (Literary Music)
		literaryStar1 = (birthChars.hourBranch + 4) % 12;

		// Wen Ch'ang (Literary Prosperity)
		literaryStar2 = (12 + 10 - birthChars.hourBranch) % 12;

		// Yang Jen (Sheep-blade Star)
		const int yangjenLoc[] = {3, 4, 6, 7, 6, 7, 9, 10, 0, 1};
		sheepBladeStar = yangjenLoc[birthChars.yearStem];

		// T'o Lo (Hump-back Star)
		const int toloLoc[] = {1, 2, 4, 5, 4, 5, 7, 8, 10, 11};
		humpBackStar = toloLoc[birthChars.yearStem];

		// yearly stars
		// 1 - T'ien Ts'un - Heavenly Store
		// 2 - T'ien K'uei - Heavenly Leader
		// 3 - T'ien Yueh  - Heavenly Halberd
		const int yearly1Loc[] = {2, 3, 5, 6, 5, 6, 8, 9, 11, 0};
		const int yearly2Loc[] = {1, 0, 11, 9, 7, 8, 7, 6, 5, 3};
		const int yearly3Loc[] = {7, 8, 9, 11, 1, 0, 1, 2, 3, 5};

		yearlyStar1 = yearly1Loc[birthChars.yearStem];
		yearlyStar2 = yearly2Loc[birthChars.yearStem];
		yearlyStar3 = yearly3Loc[birthChars.yearStem];

		// monthly stars
		// 1 - Tso Fu - Right Assistant
		// 2 - Yu Pi - Left Assistant
		// 3 - I-ma - Travelling Star
		monthlyStar1 = (birthChars.monthBranch + 2) % 12;
		monthlyStar2 = (12 - birthChars.monthBranch) % 12;
		
		const int monthly3Shift[] = {2, 11, 8, 5};
		monthlyStar3 = monthly3Shift[(birthChars.monthBranch % 4)];

		// hourly stars
		// 1 - T'ien K'ung - Heavenly Void
		// 2 - Ti Chieh - Earthly Robbery
		hourlyStar1 = (12 + 11 - birthChars.hourBranch) % 12;
		hourlyStar2 = (11 + birthChars.hourBranch) % 12;

		// miscellaneous yearly stars
		// 1 - T'ien Hao - Heavenly Destroyer
		// 2 - Hung Luan - Red Phoenix
		// 3 - T'ien Hsi - Heavenly Happiness
		miscYearlyStar1 = (1 + birthChars.yearBranch) % 12;
		miscYearlyStar2 = (12 + 3 - birthChars.yearBranch) % 12;
		miscYearlyStar3 = (12 + 9 - birthChars.yearBranch) % 12;

		// miscellaneous monthly stars
		// 1 - T'ien Yao - Heavenly Beauty
		// 2 - T'ien Hsing - Heavenly Punishment
		miscMonthlyStar1 = (11 + birthChars.monthBranch) % 12;
		miscMonthlyStar2 = (7 + birthChars.monthBranch) % 12;
	}
	

	Constants::eElements TzuWeiCalc::calcElement(BirthCharacters& chars, int mingLoc)
	{
		int tempMing = mingLoc / 2;
		int offset = 0;
		switch (tempMing)
		{
			case 0:
				offset = 0;
				break;
			case 1:
				offset = 1;
				break;
			case 2:
				offset = 3;
				break;
			case 3:
				offset = 2;
				break;
			case 4:
				offset = 4;
				break;
			case 5:
				offset = 1;
				break;
		}

		int elem = (chars.yearStem + offset) % 5;

		if (elem == 0)
            return Constants::eElements::Water;
		else if (elem == 1)
			return Constants::eElements::Fire;
		else if (elem == 2)
			return Constants::eElements::Earth;
		else if (elem == 3)
			return Constants::eElements::Wood;
		else 
			return Constants::eElements::Metal;
	}

	int TzuWeiCalc::calcTzuWei(Constants::eElements elem, BirthDate& myMoonDate)
	{
		int tzuWeiLoc;
		int divider = 0;
		int offset = 0;
		if (elem == Constants::eElements::Water)
		{
			divider = 2;
			
			int ost = myMoonDate.day % divider;
			
			if (ost == 1)
				offset = 1;
			else 
				offset = 2;
		} 
		else if (elem == Constants::eElements::Wood)
		{
			divider = 3;
			int ost = myMoonDate.day % divider;
			
			if (ost == 1)
				offset = 4;
			else if (ost == 2)
				offset = 1;
			else 
				offset = 2;
		}
		else if (elem == Constants::eElements::Metal)
		{
			divider = 4;
			int ost = myMoonDate.day % divider;
			if (ost == 1)
				offset = 11;
			else if (ost == 2)
				offset = 4;
			else if (ost == 3)
				offset = 1;
			else 
				offset = 2;
		}
		else if (elem == Constants::eElements::Earth)
		{
			divider = 5;
			int ost = myMoonDate.day % divider;
			if (ost == 1)
				offset = 6;
			else if (ost == 2)
				offset = 11;
			else if (ost == 3)
				offset = 4;
			else if (ost == 4)
				offset = 1;
			else 
				offset = 2;
		}
		else // fire
		{
			divider = 6;
			int ost = myMoonDate.day % divider;
			
			if (ost == 1)
				offset = 9;
			else if (ost == 2)
				offset = 6;
			else if (ost == 3)
				offset = 11;
			else if (ost == 4)
				offset = 4;
			else if (ost == 5)
				offset = 1;
			else
				offset = 2;
		}

		tzuWeiLoc = ((myMoonDate.day - 1 - ((myMoonDate.day - 1) % divider)) / divider + offset) % 12;
		
		return tzuWeiLoc;
	}

	void TzuWeiCalc::calcTransformingStars(BirthCharacters& birthChars, int* northStars, int* southStars, 
									  int literary1, int literary2,	int* transStars)
	{
		// transforming stars
		// 1 - Hua Lu - Transforming Salary
		// 2 - Hua Ch'uan - Transforming Authority
		// 3 - Hua K'o - Transforming Examination Class
		// 4 - Hua Chi - Transforming Jealousy
		switch (birthChars.monthStem)
		{
		case 0:
			transStars[0] = northStars[5];
			transStars[1] = southStars[7];
			transStars[2] = northStars[3]; 
			transStars[3] = northStars[2];
			break;
		case 1:
			transStars[0] = northStars[1];
			transStars[1] = southStars[2];
			transStars[2] = northStars[0];
			transStars[3] = southStars[1];
			break;
		case 2:
			transStars[0] = northStars[4];
			transStars[1] = northStars[1];
			transStars[2] = literary2; 
			transStars[3] = northStars[5];
			break;
		case 3:
			transStars[0] = southStars[1];
			transStars[1] = northStars[4];
			transStars[2] = northStars[1];
			transStars[3] = southStars[3];
			break;
		case 4:
			transStars[0] = southStars[2];
			transStars[1] = southStars[1];
			transStars[2] = northStars[2];
			transStars[3] = northStars[1];
			break;
		case 5:
			transStars[0] = northStars[3];
			transStars[1] = southStars[2];
			transStars[2] = southStars[5];
			transStars[3] = literary1;
			break;
		case 6:
			transStars[0] = northStars[2];
			transStars[1] = northStars[3];
			transStars[2] = southStars[0];
			transStars[3] = northStars[4];
			break;
		case 7:
			transStars[0] = southStars[3];
			transStars[1] = northStars[2];
			transStars[2] = literary1;
			transStars[3] = literary2;
			break;
		case 8:
			transStars[0] = southStars[5];
			transStars[1] = northStars[0];
			transStars[2] = southStars[0];
			transStars[3] = northStars[3];
			break;
		case 9:
			transStars[0] = southStars[7];
			transStars[1] = southStars[3];
			transStars[2] = southStars[1];
			transStars[3] = southStars[2];
			break;
		}
	}

// borowed stars are taken from the opposite palace if none are present in the palace
void TzuWeiCalc::calcBorrowedStars()
{
	int arrPalaceStars[12];
	// number of major stars
	int i;

	for (i = 0; i < 12; i++)
		arrPalaceStars[i] = 0;
	
	for (i = 0; i < Constants::northStarsNum; i++)
		arrPalaceStars[m_northStars[i]]++;

	for (i = 0; i < Constants::southStarsNum; i++)
		arrPalaceStars[m_southStars[i]]++;

	for (i = 0; i < Constants::northStarsNum; i++)
	{
		// if in the opposite house
		if (arrPalaceStars[(m_northStars[i] + 6) % 12] == 0)
		{
			m_borrowedStars[i] = true;
		}
	}
	
	for (i = 0; i < Constants::southStarsNum; i++)
	{
		// if in the opposite house
		if (arrPalaceStars[(m_southStars[i] + 6) % 12] == 0)
		{
			m_borrowedStars[i + Constants::northStarsNum] = true;
		}
	}	
}

void TzuWeiCalc::calcGreatLimits(Constants::eElements elem, int yearStem, bool bMale, int palace, int* limit)
{
	// wood, fire, earth, metal, water
	int arrShift[5] = {3, 6, 5, 4, 2};

	// calculate clockwise/counter-clockwise
	int nMale = bMale ? 0:1;
	// yang year + male; yin year + female - clockwise. Otherwise, anticlockwise
	int clockwise = (((yearStem % 2) + nMale) % 2) * -2 + 1;
		
	*limit = arrShift[(int) elem] + 10 * ((12 + (palace + 1) % 12 * clockwise) % 12) ;

	return;
}

void TzuWeiCalc::calcElementsForStemBranch(int stem, int branch, int* arrWeights)
{
	int arrBranchWeights[] = {4, 2, 0, 0, 2, 1, 1, 2, 3, 3, 2, 4};
	// 1,2 Stem, branch
	int fiveStem = (stem - (stem % 2)) / 2;
	arrWeights[fiveStem]++;
	arrWeights[arrBranchWeights[branch]]++;
	// 3 - stem and branch
	int arrStemElements[] = {3, 4, 1, 2, 0};
	// int arrBranchShifts[] = {3, 4, 1};
	int miniBranch = (branch - (branch % 2)) / 2;
	miniBranch = miniBranch % 3;
	arrWeights[arrStemElements[(fiveStem + miniBranch) % 5]]++; 
}

void TzuWeiCalc::calcElementsWeight(BirthCharacters chars, int* arrWeights)
{
	calcElementsForStemBranch(chars.yearStem, chars.yearBranch, arrWeights);
	calcElementsForStemBranch(chars.monthStem, chars.monthBranch, arrWeights);
	calcElementsForStemBranch(chars.dayStem, chars.dayBranch, arrWeights);
	calcElementsForStemBranch(chars.hourStem, chars.hourBranch, arrWeights);
}

/* old version, using external component. Now all the calculations are inside 
bool MoonDate::Initialize(BirthDate& sunDate, CString& errorMessage, bool bTestLocalTZ)
{
	try
	{
		// if the time is past 11 p.m., this is the next day. Decided to remove for now.
		// This issue needs additional consideration
		if (sunDate.hour >= 23)
		{
			COleDateTime dtBirth((int) sunDate.year, (int) sunDate.month, (int) sunDate.day, (int) sunDate.hour, (int) sunDate.min, 0);
			COleDateTimeSpan oneHour(0, 1, 0, 0);
			dtBirth += oneHour;
			
			sunDate.year = dtBirth.GetYear();
			sunDate.month = dtBirth.GetMonth();
			sunDate.day = dtBirth.GetDay();
			sunDate.hour = dtBirth.GetHour();
			sunDate.min = dtBirth.GetMinute();
		}

		// this is a old using of Chinese Calendar dll
		CComPtr<_clsCLunarCAL> pComp;
		HRESULT hr = pComp.CoCreateInstance(__uuidof(clsCLunarCAL));
		if (hr != S_OK)
		{
			// error happened. Return false;
			errorMessage.Format(_T("Could not use external dll; hr = %1!#lx!"), hr);

			return false;
		}

		pComp->SunYear = (short) sunDate.year;
		pComp->SunMonth = (short) sunDate.month;
		pComp->SunDay = (short) sunDate.day;
		pComp->SunHour = (short) sunDate.hour;
		pComp->SunMinute = (short) sunDate.min;
		if (!bTestLocalTZ)
			pComp->TimeZone = (short) sunDate.timeZone;
		else
			pComp->LocalTimeZone = (short) sunDate.timeZone;
		pComp->LocalLongitude = ((short) sunDate.timeZone * 15);

		pComp->UseCivicCalendar = false;

		// cls.AppPath = @"..\MDB\";
		// pComp->SUN2LOCALTIME();

		pComp->SUN2MOON();
		CComBSTR errorMsg;
		pComp->get_ErrorMsg(&errorMsg);
		
		if (errorMsg.Length() != 0)
		{
			// error happened;
			return false;
		}

		this->year = pComp->MoonYear;
		this->month = pComp->MoonMonth;
		this->day = pComp->MoonDay;
		this->hour = sunDate.hour;
		this->min = sunDate.min;

		return true;
	}	
	catch (_com_error ex)
	{
		errorMessage.Format(_T("Using external dll led to an error. Probably, it was not registered correctly. \nError message is '%s'!"), ex.ErrorMessage());
		// errorMessage = ex.ErrorMessage();
		return false;
	}
}
*/

bool MoonDate::Initialize(BirthDate& sunDate, CString& errorMessage, char* resData)
{
	// if the time is past 11 p.m., this is the next day. Decided to remove for now.
	// This issue needs additional consideration
	if (sunDate.hour >= 23)
	{
		COleDateTime dtBirth((int) sunDate.year, (int) sunDate.month, (int) sunDate.day, (int) sunDate.hour, (int) sunDate.min, 0);
		COleDateTimeSpan oneHour(0, 1, 0, 0);
		dtBirth += oneHour;
		
		sunDate.year = dtBirth.GetYear();
		sunDate.month = dtBirth.GetMonth();
		sunDate.day = dtBirth.GetDay();
		sunDate.hour = dtBirth.GetHour();
		sunDate.min = dtBirth.GetMinute();
	}

	int tempYear, tempMonth, tempDay;
	bool bRes = ChineseDatesConv::GetChineseDateFromRes(sunDate.year, sunDate.month, sunDate.day, sunDate.timeZone, 
														&tempYear, &tempMonth, &tempDay,
														resData);
	if (bRes)
	{
		this->year = tempYear;
		this->month = tempMonth;
		this->day = tempDay;
		this->hour = sunDate.hour;
		this->min = sunDate.min;
		this->timeZone = sunDate.timeZone;
	}
	else
	{
		errorMessage.Format(_T("Conversion to the Chinese date lead to an error!"));
	}
	
	return bRes;
}
