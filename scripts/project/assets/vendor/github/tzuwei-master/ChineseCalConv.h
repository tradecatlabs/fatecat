#pragma once

class ChineseDatesConv
{
	static double Date2J(int d, int m, int y)
	{
		int k;
  
		double JD;// ' Julian day number starting at noon
	 
		k = (int) (14 - m) / 12;
		JD = d + (int) (367 * (m + (k * 12) - 2) / 12) + (int)(1461 * (y + 4800 - k) / 4) - 32113;

		if (JD > 2299160)
		{
			JD = JD - (int)(3 * (int)(((y + 100 - k) / 100) / 4) - 2);
		}

		JD = JD - 0.5;

		return JD;
	}

	static int GetAmmendedDate(CString& line, int tz)
	{
		int nIntStart = 0;
		CString token = line.Tokenize(",", nIntStart);
		int nFirstColumn = atoi(token);
		// ignore the second column
		token = line.Tokenize(",", nIntStart);
		// ignore the third column
		token = line.Tokenize(",", nIntStart);
		int readHour = atoi(line.Tokenize(",", nIntStart));
		int readMin = atoi(line.Tokenize(",", nIntStart));
		
		// calculate
		if ((readHour + tz) < -1)
			nFirstColumn--;
		else if ((readHour + tz) >= 23)
			nFirstColumn++;

		return nFirstColumn;
	}

public:
	static bool GetChineseDate(int year, int month, int day, int tz, int* lunarYear, int* lunarMonth, int* lunarDay)
	{
		*lunarYear = 0;
		*lunarMonth = 0;
		*lunarDay = 0;

		double dblVal = Date2J(day, month, year);
		FILE* stream;
		char line1[100] = "";
		char line2[100] = "";
		bool bFound = false;
		// this is external file

		if( (stream  = fopen("t02.txt", "r" )) == NULL )
		{
			return false;
		}
		
		if (fgets(line1, 100, stream) == NULL)
		{
			return false;
		}
		
		while (true)
		{
			if (fgets(line2, 100, stream) == NULL)
			{
				bFound = false;
				break;
			}

			CString readLine2 = line2;
			int nFirstColumn2 = GetAmmendedDate(readLine2, tz);

			// if the first column date is already bigger than the birthdate, get the previous line
			if ((int) nFirstColumn2 > (int) (dblVal + 0.6))
			{
				// get the previous line, pull out all dates
				CString readLine1 = line1;
				*lunarDay = 1 + (int) (dblVal + 0.6 - GetAmmendedDate(readLine1, tz));

				int nStart = 0;
				// get the first column
				CString token = readLine1.Tokenize(",", nStart);
				
				// get the second column
				token = readLine1.Tokenize(",", nStart);
				*lunarMonth = atoi(token) % 100;
				*lunarYear = atoi(token) / 100;

				bFound = true;

				break;
			}

			strcpy(line1, line2);
		}
		
		return bFound;
	}

	static bool GetChineseDateFromRes(int year, int month, int day, int tz, int* lunarYear, int* lunarMonth, int* lunarDay, char* resourceData)
	{
		*lunarYear = 0;
		*lunarMonth = 0;
		*lunarDay = 0;

		double dblVal = Date2J(day, month, year);
		bool bFound = false;
		
		if (resourceData == 0)
		{
			AfxMessageBox("Error. Cannot obtain resources! Exiting!");

			return false;
		}
		
		char* line1 = (char*) resourceData;
		char* line2;
		int i = 0;

		while (true)
		{ 
			i++;

			line2 = line1 + strlen(line1) + 1;
			// go find the next line
			
			// check if we reached the end of the resource
			if ((line2 == NULL) || (strstr(line2, "-end") != NULL))
			{
				bFound = false;
				break;
			}
			
			CString readLine2 = line2;

			int nFirstColumn2 = GetAmmendedDate(readLine2, tz);

			// if the first column date is already bigger than the birthdate, get the previous line
			if ((int) nFirstColumn2 > (int) (dblVal + 0.6))
			{
				// get the previous line, pull out all dates
				CString readLine1 = line1;
				*lunarDay = 1 + (int) (dblVal + 0.6 - GetAmmendedDate(readLine1, tz));

				int nStart = 0;
				// get the first column
				CString token = readLine1.Tokenize(",", nStart);
				
				// get the second column
				token = readLine1.Tokenize(",", nStart);
				*lunarMonth = atoi(token) % 100;
				*lunarYear = atoi(token) / 100;

				bFound = true;

				break;
			}

			line1 = line2;
		}
		
		return bFound;
	}
};