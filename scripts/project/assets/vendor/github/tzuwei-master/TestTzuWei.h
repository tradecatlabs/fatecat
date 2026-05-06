#include "TzuWei.h"

///////////////////////////////////////////////////////////////////////////////////////
void TestCalculations()
{
	BirthCharacters birthChars;
	TzuWeiCalc calcModule;
	
	// test ming
	CString result;
	int i, j;
	for (i = 0; i < 12; i++)
	{
		for (j = 0; j < 12; j++)
		{
			birthChars.monthBranch = j;
			birthChars.hourBranch = i;
			int ming = TzuWeiCalc::calcMing(birthChars);
			result = result + " ";
			result = result + Constants::branches[ming];
		}

		result = result += "\n";
	}

	result = "";

	// test element
	for (i = 0; i < 5; i++)
	{
		for (j = 0; j < 10; j++)
		{
			birthChars.yearStem = j;
			Constants::eElements el = TzuWeiCalc::calcElement(birthChars, i);

			result = result + " ";
			result = result + Constants::elements[el];
		}

		result = result += "\n";
	}

	result = "";

	// test tzuwei
	for (i = 0; i < 30; i++)
	{
		for (j = 0; j < 5; j++)
		{
			MoonDate md;
			md.day = i+ 1;
			int tzuWei = TzuWeiCalc::calcTzuWei((Constants::eElements) j, md);

			result = result + " ";
			result = result + Constants::branches[tzuWei];
		}

		result += "\n";
	}

	result = "";

	// north stars - DOES NOT WORK FOR NOW!
	/* for (i = 0; i < 12; i++)
	{
		int northStars[5];
		TzuWeiCalc::calcNorthStars(i, northStars);
		
		for (j = 0; j < 5; j++)
		{
			result += Constants::branches[northStars[j]];
			result += " ";
		}

		result = result + "  ";

		result += "\n";
	}*/

	result = "";
	
	// south stars
	/*for (i = 0; i < 12; i++)
	{
		int southStars[7];
		TzuWeiCalc::calcSouthStars(i, southStars);
		
		for (j = 0; j < 8; j++)
		{
			result += Constants::branches[southStars[j]];
			result += " ";
		}

		result += "\n";
	}
*/
	result = "";

	// fire star and ringing star
	int minorStars[19];
	result = Constants::minorStarNames[1/* 0 */];
	result += " location\n";

	for (i = 0; i < 12; i++)
	{
		for (j = 0; j < 12; j++)
		{
			birthChars.yearBranch = j;
			birthChars.hourBranch = i;

			TzuWeiCalc::calcMinorStars(birthChars, minorStars[0], minorStars[1], minorStars[2], minorStars[3], minorStars[4], minorStars[5], 
										  minorStars[6], minorStars[7], minorStars[8], minorStars[9], minorStars[10], minorStars[11], 
										  minorStars[12], minorStars[13], minorStars[14], minorStars[15], minorStars[16], minorStars[17],
										  minorStars[18]);

			result = result + " ";
			result = result + Constants::branches[minorStars[1 /* 0 */]];
		}

		result = result += "\n";
	}

	result = "";
	
	// literary stars

	result = Constants::minorStarNames[2];
	result += " ";
	result += Constants::minorStarNames[3];
	result += " location\n";

	for (i = 0; i < 12; i++)
	{
		birthChars.hourBranch = i;
		TzuWeiCalc::calcMinorStars(birthChars, minorStars[0], minorStars[1], minorStars[2], minorStars[3], minorStars[4], minorStars[5], 
										  minorStars[6], minorStars[7], minorStars[8], minorStars[9], minorStars[10], minorStars[11], 
										  minorStars[12], minorStars[13], minorStars[14], minorStars[15], minorStars[16], minorStars[17],
										  minorStars[18]);

		result = result + " ";
		result = result + Constants::branches[minorStars[2]];
		result = result + " ";
		result = result + Constants::branches[minorStars[3]];
		result = result += "\n";
	}

	result = "";

	// sheep-blade and hump-back and yearly stars
	result = Constants::minorStarNames[4];
	result += ", ";
	result += Constants::minorStarNames[5];
	result += ", ";
	result += Constants::minorStarNames[6];
	result += ", ";
	result += Constants::minorStarNames[7];
	result += " and ";
	result += Constants::minorStarNames[8];
	result += " location\n";

	for (i = 0; i < 10; i++)
	{
		birthChars.yearStem = i;
		TzuWeiCalc::calcMinorStars(birthChars, minorStars[0], minorStars[1], minorStars[2], minorStars[3], minorStars[4], minorStars[5], 
										  minorStars[6], minorStars[7], minorStars[8], minorStars[9], minorStars[10], minorStars[11], 
										  minorStars[12], minorStars[13], minorStars[14], minorStars[15], minorStars[16], minorStars[17],
										  minorStars[18]);

		result = result + " ";
		for (j = 4; j < 9; j++)
		{
			result = result + Constants::branches[minorStars[j]];
			result = result + ", ";
		}

		result = result += "\n";
	}

	result = "";

	result += Constants::minorStarNames[9];
	result += ", ";
	result += Constants::minorStarNames[10];
	result += ", ";
	result += Constants::minorStarNames[11];
	result += ", ";
	result += Constants::minorStarNames[17];
	result += ", ";
	result += Constants::minorStarNames[18];
	
	result += " location\n\n";

	// monthly stars and misc. monthly stars
	for (i = 0; i < 12; i++)
	{
		birthChars.monthBranch = i;
		TzuWeiCalc::calcMinorStars(birthChars, minorStars[0], minorStars[1], minorStars[2], minorStars[3], minorStars[4], minorStars[5], 
										  minorStars[6], minorStars[7], minorStars[8], minorStars[9], minorStars[10], minorStars[11], 
										  minorStars[12], minorStars[13], minorStars[14], minorStars[15], minorStars[16], minorStars[17],
										  minorStars[18]);

		for (j = 9; j < 12; j++)
		{
			result = result + Constants::branches[minorStars[j]];
			result = result + ", ";
		}

		for (j = 17; j < 19; j++)
		{
			result = result + Constants::branches[minorStars[j]];
			result = result + ", ";
		}

		result = result += "\n";
	}

	result = "";

	// hourly stars
	for (i = 0; i < 12; i++)
	{
		birthChars.hourBranch = i;
		TzuWeiCalc::calcMinorStars(birthChars, minorStars[0], minorStars[1], minorStars[2], minorStars[3], minorStars[4], minorStars[5], 
										  minorStars[6], minorStars[7], minorStars[8], minorStars[9], minorStars[10], minorStars[11], 
										  minorStars[12], minorStars[13], minorStars[14], minorStars[15], minorStars[16], minorStars[17],
										  minorStars[18]);

		for (j = 12; j < 14; j++)
		{
			result = result + Constants::branches[minorStars[j]];
			result = result + ", ";
		}
		
		result = result += "\n";
	}	

	result = "";

	// misc. yearly stars
	for (i = 0; i < 12; i++)
	{
		birthChars.yearBranch = i;
		TzuWeiCalc::calcMinorStars(birthChars, minorStars[0], minorStars[1], minorStars[2], minorStars[3], minorStars[4], minorStars[5], 
										  minorStars[6], minorStars[7], minorStars[8], minorStars[9], minorStars[10], minorStars[11], 
										  minorStars[12], minorStars[13], minorStars[14], minorStars[15], minorStars[16], minorStars[17],
										  minorStars[18]);

		for (j = 14; j < 17; j++)
		{
			result = result + Constants::branches[minorStars[j]];
			result = result + ", ";
		}
		
		result = result += "\n";
	}	

	result = "";
	
	// test elements weight
	int* arrWeights;
	CString strTemp;

	for (i = 0; i < 60; i++)
	{
		int stem = i % 10;
		int branch = i % 12;
		arrWeights = new int[5];
		for (j = 0; j < 5; j++) 
			arrWeights[j] = 0;

		TzuWeiCalc::calcElementsForStemBranch(stem, branch, arrWeights);
		for (j = 0; j < 5; j++) 
		{
			if (arrWeights[j] > 0)
			{
				strTemp.Format("%d %s: %d; ", i, Constants::elements[j], arrWeights[j]);
				result += strTemp;
			}
		}

		delete arrWeights;

		result += "\n";
	}

	AfxMessageBox(result);
}

void CalcZeroDay()
{
	// COleDateTime dtZero(1924, 2, 15, 0, 0, 0);
	COleDateTime dtZero(1924, 2, 21, 0, 0, 0);
	COleDateTimeSpan manyDays(28 * 28 * 28, 0, 0, 0);
	dtZero -= manyDays;
	CString strTemp;
	strTemp.Format("%d-%d-%d", dtZero.GetYear(), dtZero.GetMonth(), dtZero.GetDay()); 
	AfxMessageBox(strTemp);
}

/* CString TestChineseCalendarComp(bool bLocalTZ, int year, int month, int day, int hour, int min, int tz)
{
	CComPtr<_clsCLunarCAL> pComp;
	HRESULT hr = pComp.CoCreateInstance(__uuidof(clsCLunarCAL));
	if (hr != S_OK)
	{
		return "";
	}

		pComp->SunYear = (short) year;
		pComp->SunMonth = (short) month;
		pComp->SunDay = (short) day;
		pComp->SunHour = (short) hour;
		pComp->SunMinute = (short) min;
		if (!bLocalTZ)
			pComp->TimeZone = (short) tz;
		else
			pComp->LocalTimeZone = (short) tz;
		pComp->LocalLongitude = ((short) tz * 15);

		pComp->UseCivicCalendar = false;

		pComp->SUN2MOON();
		CComBSTR errorMsg;
		pComp->get_ErrorMsg(&errorMsg);

		CString strTemp;
		strTemp.Format("%d-%d-%d %d:%d tz=%d", pComp->MoonYear,
			pComp->MoonMonth,
			pComp->MoonDay,
			hour,
			min,
			tz);

		return strTemp;
}

void FullTestChineseCalendarComp()
{
	CString strTemp3;

	for (int i = -12; i < 12; i++)
	{
		int day = 18;
		int tz = i;
		int hour = 5;
		CString strTemp1 = TestChineseCalendarComp(true, 1977, 2, day, hour, 30, tz);
		CString strTemp2 = TestChineseCalendarComp(false, 1977, 2, day, hour, 30, tz);

		strTemp3 += "local:";
		strTemp3 += strTemp1;
		strTemp3 += "; timezone:";
		strTemp3 += strTemp2;
		strTemp3 += "\n";
	}

	AfxMessageBox(strTemp3);
}*/