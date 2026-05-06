// TzuWeiChart.cpp : implementation file
//

#include "stdafx.h"
#include "Prototype3.h"
#include "TzuWeiChart.h"
#include ".\tzuweichart.h"
#include "afxdlgs.h"

bool gl_bNonCommercial = true;
// CTzuWeiChart
int stemBitmaps[] = {IDB_STEM0, IDB_STEM1, IDB_STEM2, IDB_STEM3, IDB_STEM4, IDB_STEM5, IDB_STEM6, IDB_STEM7, IDB_STEM8, IDB_STEM9};
int branchesBitmaps[] = {IDB_BRANCH0, IDB_BRANCH1, IDB_BRANCH2, IDB_BRANCH3, IDB_BRANCH4, IDB_BRANCH5, IDB_BRANCH6, IDB_BRANCH7, IDB_BRANCH8, IDB_BRANCH9, IDB_BRANCH10, IDB_BRANCH11};

IMPLEMENT_DYNAMIC(CTzuWeiChart, CWnd)
CTzuWeiChart::CTzuWeiChart(TzuWeiFullInfo* pInfo)
{
	m_pInfo = pInfo;
}

CTzuWeiChart::~CTzuWeiChart()
{
	if (m_pInfo)
		delete m_pInfo;
}


BEGIN_MESSAGE_MAP(CTzuWeiChart, CWnd)
	ON_WM_PAINT()
	ON_WM_CHAR()
END_MESSAGE_MAP()

class CBmpDraw
{
	CBitmap m_Bitmap;
	CDC     m_dc;

public:

	CBmpDraw(UINT nBmp)
	{
		m_Bitmap.LoadBitmap(nBmp);
		CWindowDC     dc(NULL);
		m_dc.CreateCompatibleDC(&dc);
	}

	~CBmpDraw()
	{
		m_dc.DeleteDC();
	}

	void GetBitmapSize(CSize* pSize)
	{
		BITMAP bitMap;
		m_Bitmap.GetObject(sizeof(bitMap), &bitMap);
		pSize->cx = bitMap.bmWidth;
		pSize->cy = bitMap.bmHeight;
	}

	void Draw(CDC* pDC, int x, int y, int cx, int cy)
	{
		CBitmap* pb = m_dc.SelectObject(&m_Bitmap);
		
		pDC->BitBlt(x,y,cx,cy,&m_dc, 0, 0, SRCCOPY);
		m_dc.SelectObject(pb);
	}


};

BOOL CTzuWeiChart::PreCreateWindow(CREATESTRUCT& cs)
{
	// create fonts 
	LOGFONT logNameFont, logPillarsFont, logPalacesFont, logMajorStarsFont, logMinorStarsFont;
	LOGFONT logCopyrightFont, logCentralHeaderFont;
	memset(&logNameFont, 0, sizeof(LOGFONT));       // zero out structure
	memset(&logPillarsFont, 0, sizeof(LOGFONT));       
	memset(&logPalacesFont, 0, sizeof(LOGFONT));    
	memset(&logMajorStarsFont, 0, sizeof(LOGFONT)); 
	memset(&logMinorStarsFont, 0, sizeof(LOGFONT)); 
	memset(&logCopyrightFont, 0, sizeof(LOGFONT)); 
	memset(&logCentralHeaderFont, 0, sizeof(LOGFONT)); 

	logNameFont.lfHeight = 20;                      
	logNameFont.lfWeight = FW_BOLD;
	strcpy(logNameFont.lfFaceName, "Courier New");       

	logPillarsFont.lfHeight = 15;                      
	// logPillarsFont.lfWeight = FW_SEMIBOLD;
	strcpy(logPillarsFont.lfFaceName, "Verdana");        
	
	logCentralHeaderFont.lfHeight = 16;                      
	logCentralHeaderFont.lfItalic = TRUE;
	logCentralHeaderFont.lfWeight = FW_SEMIBOLD;
	strcpy(logCentralHeaderFont.lfFaceName, "Verdana");        
	
	logPalacesFont.lfHeight = 16;                      
	logPalacesFont.lfWeight = FW_BOLD;
	strcpy(logPalacesFont.lfFaceName, "Verdana");        
	
	logMajorStarsFont.lfHeight = 15;                      
	logMajorStarsFont.lfWeight = FW_SEMIBOLD;
	strcpy(logMajorStarsFont.lfFaceName, "Gautami");        
	
	logMinorStarsFont.lfHeight = 14;                      
	// logMinorStarsFont.lfWeight = FW_SEMIBOLD;
	strcpy(logMinorStarsFont.lfFaceName, "Gautami");        
	
	logCopyrightFont.lfHeight = 16;                      
	// logMinorStarsFont.lfWeight = FW_SEMIBOLD;
	strcpy(logCopyrightFont.lfFaceName, "Comic Sans MS");        

	VERIFY(m_fontName.CreateFontIndirect(&logNameFont));  
	VERIFY(m_fontPillars.CreateFontIndirect(&logPillarsFont));  
	VERIFY(m_fontPalaces.CreateFontIndirect(&logPalacesFont));  
	VERIFY(m_fontMajorStars.CreateFontIndirect(&logMajorStarsFont));  
	VERIFY(m_fontMinorStars.CreateFontIndirect(&logMinorStarsFont));  
	VERIFY(m_fontCopyright.CreateFontIndirect(&logCopyrightFont));  
	VERIFY(m_fontCentralHeader.CreateFontIndirect(&logCentralHeaderFont));  

	m_pen.CreatePen(PS_SOLID, 2, RGB(0, 0, 0));
	m_copyrightPen.CreatePen(PS_SOLID, 1, RGB(0, 0, 0));

	// Create a window without min/max buttons or sizable border
	// cs.style = WS_OVERLAPPED | WS_SYSMENU | WS_BORDER;
	
	cs.lpszClass = AfxRegisterWndClass(NULL, 0, (HBRUSH) (COLOR_WINDOW + 1));
	return CWnd::PreCreateWindow(cs);
}

void CTzuWeiChart::PostNcDestroy()
{
	DeleteObject(m_fontName);
	DeleteObject(m_fontPillars);
	DeleteObject(m_fontPalaces);
	DeleteObject(m_fontMajorStars);
	DeleteObject(m_fontMinorStars);
	DeleteObject(m_fontCopyright);

	DeleteObject(m_pen);
	DeleteObject(m_copyrightPen);

	delete this;
}

// CTzuWeiChart message handlers

void CTzuWeiChart::OutputStar(CDC& dc, CString& strStarName, int nBox, int cyChar, int leftCorner, int topCorner, int* starNumberInBox, COLORREF col)
{
	int textX = leftCorner;
	int textY = topCorner + (starNumberInBox[nBox]) * cyChar;
	COLORREF oldColor;

	if (col != 0)
	{
		oldColor = dc.GetTextColor();
		dc.SetTextColor(col);
	}

	dc.TextOut(textX, textY, strStarName);
	
	if (col != 0)
		dc.SetTextColor(oldColor);

	starNumberInBox[nBox]++;
}

void getSuffix(int nNumber, CString& strSuf)
{
	strSuf = "";
	int nSuf = nNumber % 10;
	if (nSuf == 1)
		strSuf = "st";
	else if (nSuf == 2) 
		strSuf = "nd";
	else if (nSuf == 3) 
		strSuf = "rd";
	else
		strSuf = "th";

	if ((nNumber % 100 > 10) && (nNumber % 100 < 20))
		strSuf = "th";
}


void CTzuWeiChart::DrawChart(CDC& dc, bool bPrinter)
{
	// get the text height
	TEXTMETRIC tm;
	GetTextMetrics(dc, &tm);
	int cyCharSystem = tm.tmHeight + tm.tmExternalLeading;

	// get client area size and shifts
	CRect windowRect;
	int bottomAreaHeight;
	int horShift = 0;
	int vertShift = 0;

	if (!bPrinter)
	{
		GetClientRect(&windowRect);
		bottomAreaHeight = /*windowRect.Height() / 8*/3 * cyCharSystem;
	}
	else
	{
		dc.GetClipBox(&windowRect);
		bottomAreaHeight = windowRect.bottom / 8;
		horShift = windowRect.right / 32;
		windowRect.bottom = windowRect.bottom * 3 / 4;
		windowRect.right = windowRect.right * 15 / 16;
	}

	dc.SelectObject(m_pen);

	// draw the boxes
	int boxWidth = (windowRect.Width() - 2 * horShift) / 4;
	int boxHeight = (windowRect.Height() - 2 * vertShift - bottomAreaHeight) / 4;
	int i, j;
	for (i = 0; i < 4; i++)
	{
		for (j = 0; j < 4; j++)
		{
            if (!((i == 1 || i == 2) && (j == 1 || j == 2)))
			{
				dc.Rectangle(horShift + boxWidth * i + 1, vertShift + j * boxHeight, horShift + boxWidth * (i + 1) + 2, vertShift + boxHeight * (j+1) + 1);
			}
		}
	}

	// Write name a in the central large box
	dc.SelectObject(m_fontName);
	GetTextMetrics(dc, &tm);
	
	CString strTemp = m_pInfo->m_name;
	int cyCharName = tm.tmHeight + tm.tmExternalLeading;
	int cxCharName = tm.tmAveCharWidth;
	int lenX = strTemp.GetLength() * cxCharName;

	int textX = 2 * boxWidth + horShift - lenX / 2;
	int textY = boxHeight + 10;

	dc.TextOut(textX, textY, strTemp);
	
	textY += 3 * cyCharName / 2;

	// Write the dates
	dc.SelectObject(m_fontCentralHeader);
	GetTextMetrics(dc, &tm);
	int cyCharCentralHeader = tm.tmHeight + tm.tmExternalLeading;
	int cxCharCentralHeader = tm.tmAveCharWidth;

	dc.SelectObject(m_fontPillars);
	GetTextMetrics(dc, &tm);
	int cyCharCentralText = tm.tmHeight + tm.tmExternalLeading;
	int cxCharCentralText = tm.tmAveCharWidth;

	textX = boxWidth + boxWidth / 8 + horShift;
	strTemp = "Birth Date";
	dc.TextOut(textX, textY, strTemp);

	textX = boxWidth + boxWidth / 2 + horShift;
	strTemp = ":";
	dc.TextOut(textX, textY, strTemp);

	textX = boxWidth + boxWidth / 2 + horShift + cxCharCentralText * 3;
	CString strSuffix, strSuffix2;
	getSuffix(m_pInfo->m_sunDate->showDay, strSuffix);

	CString strFormat = "%s the %d%s, %d; %.2d:%.2d GMT%+d";
	strTemp.Format(strFormat, Constants::months[m_pInfo->m_sunDate->showMonth - 1],
					m_pInfo->m_sunDate->showDay, strSuffix, m_pInfo->m_sunDate->showYear, 
					m_pInfo->m_sunDate->showHour, m_pInfo->m_sunDate->showMin, m_pInfo->m_sunDate->timeZone);
	dc.TextOut(textX, textY, strTemp);

	textY += cyCharCentralText;
	textX = boxWidth + boxWidth / 8 + horShift;
	strTemp = "Lunar Date";
	dc.TextOut(textX, textY, strTemp);

	textX = boxWidth + boxWidth / 2 + horShift;
	strTemp = ":";
	dc.TextOut(textX, textY, strTemp);

	textX = boxWidth + boxWidth / 2 + horShift + cxCharCentralText * 3;
	
	getSuffix(m_pInfo->m_moonDate->month, strSuffix);
	getSuffix(m_pInfo->m_moonDate->day, strSuffix2);

	strFormat = "%d%s month, %d%s day, %d";
	strTemp.Format(strFormat, m_pInfo->m_moonDate->month, strSuffix,
					m_pInfo->m_moonDate->day, strSuffix2, m_pInfo->m_moonDate->year);
	dc.TextOut(textX, textY, strTemp);

	// FOUR PILLARS
	dc.SelectObject(m_fontCentralHeader);

	strTemp = "Four Pillars :";
	lenX = strTemp.GetLength() * cxCharCentralHeader;
	textY += 2 * cyCharCentralHeader;
	int innerElemTextX = boxWidth + horShift + boxWidth / 8;
	dc.TextOut(innerElemTextX, textY, strTemp);
	textY += cyCharCentralHeader * 3 / 2;

	dc.SelectObject(m_fontPillars);

	textX = boxWidth + boxWidth / 2 + horShift;
	strTemp = "Year";
	dc.TextOut(textX, textY, strTemp);

	textX = boxWidth + 3 * boxWidth / 4 + horShift;
	strTemp = ":";
	dc.TextOut(textX, textY, strTemp);
	
	textX += cxCharCentralText * 2;
	CBmpDraw* pDraw = new CBmpDraw(stemBitmaps[m_pInfo->m_birthChars->yearStem]);	
	CSize bitmapSize;
	pDraw->GetBitmapSize(&bitmapSize);
	pDraw->Draw(&dc, textX, textY, bitmapSize.cx, bitmapSize.cy);
	textX += bitmapSize.cx;
	delete pDraw;

	pDraw = new CBmpDraw(branchesBitmaps[m_pInfo->m_birthChars->yearBranch]);	
	pDraw->GetBitmapSize(&bitmapSize);
	pDraw->Draw(&dc, textX, textY, bitmapSize.cx, bitmapSize.cy);
	textX += bitmapSize.cx;
	delete pDraw;

	// textX = textX + cxCharCentralText * 4;
	strFormat = "- %s %s (%s %s)";
	strTemp.Format(strFormat, Constants::stems[m_pInfo->m_birthChars->yearStem],
				Constants::branches[m_pInfo->m_birthChars->yearBranch],
				Constants::elements[(m_pInfo->m_birthChars->yearStem / 2)], 
				Constants::animals[m_pInfo->m_birthChars->yearBranch]);
	dc.TextOut(textX, textY, strTemp);

	textY += cyCharCentralText;
	textX = boxWidth + boxWidth / 2 + horShift;
	strTemp = "Month";
	dc.TextOut(textX, textY, strTemp);

	textX = boxWidth + 3 * boxWidth / 4 + horShift;
	strTemp = ":";
	dc.TextOut(textX, textY, strTemp);
	
	textX += cxCharCentralText * 2;
	pDraw = new CBmpDraw(stemBitmaps[m_pInfo->m_birthChars->monthStem]);	
	pDraw->GetBitmapSize(&bitmapSize);
	pDraw->Draw(&dc, textX, textY, bitmapSize.cx, bitmapSize.cy);
	textX += bitmapSize.cx;
	delete pDraw;

	pDraw = new CBmpDraw(branchesBitmaps[m_pInfo->m_birthChars->monthBranch]);	
	pDraw->GetBitmapSize(&bitmapSize);
	pDraw->Draw(&dc, textX, textY, bitmapSize.cx, bitmapSize.cy);
	textX += bitmapSize.cx;
	delete pDraw;

	// textX = textX + cxCharCentralText * 4;
	strFormat = "- %s %s (%s %s)";
	strTemp.Format(strFormat, Constants::stems[m_pInfo->m_birthChars->monthStem],
				Constants::branches[m_pInfo->m_birthChars->monthBranch],
				Constants::elements[(m_pInfo->m_birthChars->monthStem / 2)], 
				Constants::animals[m_pInfo->m_birthChars->monthBranch]);

	dc.TextOut(textX, textY, strTemp);
	textY += cyCharCentralText;

	textX = boxWidth + boxWidth / 2 + horShift;
	strTemp = "Day";
	dc.TextOut(textX, textY, strTemp);

	textX = boxWidth + 3 * boxWidth / 4 + horShift;
	strTemp = ":";
	dc.TextOut(textX, textY, strTemp);
	
	textX += cxCharCentralText * 2;
	pDraw = new CBmpDraw(stemBitmaps[m_pInfo->m_birthChars->dayStem]);	
	pDraw->GetBitmapSize(&bitmapSize);
	pDraw->Draw(&dc, textX, textY, bitmapSize.cx, bitmapSize.cy);
	textX += bitmapSize.cx;
	delete pDraw;

	pDraw = new CBmpDraw(branchesBitmaps[m_pInfo->m_birthChars->dayBranch]);	
	pDraw->GetBitmapSize(&bitmapSize);
	pDraw->Draw(&dc, textX, textY, bitmapSize.cx, bitmapSize.cy);
	textX += bitmapSize.cx;
	delete pDraw;

	// textX = textX + cxCharCentralText * 4;
	strFormat = "- %s %s (%s %s)";
	strTemp.Format(strFormat, Constants::stems[m_pInfo->m_birthChars->dayStem],
				Constants::branches[m_pInfo->m_birthChars->dayBranch],
				Constants::elements[(m_pInfo->m_birthChars->dayStem / 2)], 
				Constants::animals[m_pInfo->m_birthChars->dayBranch]);

	dc.TextOut(textX, textY, strTemp);

	textY += cyCharCentralText;
	textX = boxWidth + boxWidth / 2 + horShift;
	strTemp = "Hour";
	dc.TextOut(textX, textY, strTemp);

	textX = boxWidth + 3 * boxWidth / 4 + horShift;
	strTemp = ":";
	dc.TextOut(textX, textY, strTemp);
	
	textX += cxCharCentralText * 2;
	pDraw = new CBmpDraw(stemBitmaps[m_pInfo->m_birthChars->hourStem]);	
	pDraw->GetBitmapSize(&bitmapSize);
	pDraw->Draw(&dc, textX, textY, bitmapSize.cx, bitmapSize.cy);
	textX += bitmapSize.cx;
	delete pDraw;

	pDraw = new CBmpDraw(branchesBitmaps[m_pInfo->m_birthChars->hourBranch]);	
	pDraw->GetBitmapSize(&bitmapSize);
	pDraw->Draw(&dc, textX, textY, bitmapSize.cx, bitmapSize.cy);
	textX += bitmapSize.cx;
	delete pDraw;

	// textX = textX + cxCharCentralText * 4;
	strFormat = "- %s %s (%s %s)";
	strTemp.Format(strFormat, Constants::stems[m_pInfo->m_birthChars->hourStem],
				Constants::branches[m_pInfo->m_birthChars->hourBranch],
				Constants::elements[(m_pInfo->m_birthChars->hourStem / 2)], 
				Constants::animals[m_pInfo->m_birthChars->hourBranch]);

	dc.TextOut(textX, textY, strTemp);
	textY += cyCharCentralText * 2;

	// INNER ELEMENT
	dc.SelectObject(m_fontCentralHeader);
	strTemp = "Inner Element :";
	dc.TextOut(innerElemTextX, textY, strTemp);

	lenX = strTemp.GetLength() * cxCharCentralHeader;
	textX = innerElemTextX + lenX + cxCharCentralHeader;

	dc.SelectObject(m_fontPillars);
	textY += (cyCharCentralHeader - cyCharCentralText) / 2;
	strTemp = Constants::elements[(int) m_pInfo->m_tzuWeiCalc->getElement()];
	dc.TextOut(textX, textY, strTemp);
	textY -= (cyCharCentralHeader - cyCharCentralText) / 2;

	// CONSTELLATION
	dc.SelectObject(m_fontCentralHeader);

	strTemp = "Constellation :";
	lenX = strTemp.GetLength() * cxCharCentralHeader;
	textX = 2 * boxWidth + horShift + boxWidth / 4 - lenX / 2;
	dc.TextOut(textX, textY, strTemp);

	dc.SelectObject(m_fontPillars);
	textX = textX + lenX + cxCharCentralHeader;
	textY += (cyCharCentralHeader - cyCharCentralText) / 2;

	strTemp = Constants::constellations[m_pInfo->m_tzuWeiCalc->m_constellation];
	dc.TextOut(textX, textY, strTemp);
	textY -= (cyCharCentralHeader - cyCharCentralText) / 2;

	// ELEMENT WEIGHTS
	textY += cyCharCentralHeader * 2;
	strTemp = "Elements :";
	dc.SelectObject(m_fontCentralHeader);
	
	dc.TextOut(innerElemTextX, textY, strTemp);

	lenX = strTemp.GetLength() * cxCharCentralHeader;
	textX = innerElemTextX + lenX + cxCharCentralHeader;

	dc.SelectObject(m_fontPillars);
	
	strTemp = "";
	CString strTemp2;
	for (int j = 0; j < 5; j++)
	{
		strTemp2.Format("%s/%d  ", Constants::elements[j], m_pInfo->m_tzuWeiCalc->m_elementWeights[j]); 
		strTemp += strTemp2;
	}

	dc.TextOut(textX, textY, strTemp);

	// write the branches names to the boxes	
	dc.SelectObject(m_fontPillars);

	int boxCornersX[12] = {0, boxWidth, boxWidth * 2, boxWidth * 3, boxWidth * 3, boxWidth * 3, boxWidth * 3, boxWidth * 2, boxWidth, 0, 0, 0};
	int boxCornersY[12] = {0,0,0,0, boxHeight, boxHeight * 2, boxHeight * 3, boxHeight * 3, boxHeight * 3, boxHeight * 3, boxHeight * 2, boxHeight};
	
	for (i = 0; i < 12; i++)
	{
		textX = boxCornersX[i] + boxWidth / 2 + horShift - 3 * cxCharCentralText;
		textY = boxCornersY[i] + boxHeight - cyCharCentralText - cyCharCentralText / 2;
		
		pDraw = new CBmpDraw(branchesBitmaps[i]);	
		pDraw->GetBitmapSize(&bitmapSize);
		pDraw->Draw(&dc, textX, textY, bitmapSize.cx, bitmapSize.cy);
		textX += bitmapSize.cx;
		delete pDraw;

		textY += cyCharCentralText / 10;

		strTemp.Format(" - %s (%s)", Constants::branches[i], Constants::animals[i]);
		dc.TextOut(textX, textY, strTemp);
	}

	dc.SelectObject(m_fontPalaces);
	GetTextMetrics(dc, &tm);
	int cyCharPalaces = tm.tmHeight + tm.tmExternalLeading;

	// write PALACES 
	int nBox;
	int nHorShiftPalaces = boxWidth / 4 + horShift;
	int nHorShiftLimits = 3 * boxWidth / 4 + horShift;
	int nVertShiftPalaces = 3;
	for (i = 0; i < 12; i++)
	{
		dc.SelectObject(m_fontPalaces);

		nBox = m_pInfo->m_tzuWeiCalc->getPalace(i);
		strTemp = Constants::palaces[i];
		textX = boxCornersX[nBox] + nHorShiftPalaces;
		textY = boxCornersY[nBox] + nVertShiftPalaces;
		
		dc.TextOut(textX, textY, strTemp);

		dc.SelectObject(m_fontMinorStars);
		textX = boxCornersX[nBox] + nHorShiftLimits;
		int limit = m_pInfo->m_tzuWeiCalc->m_limits[i];
		strTemp.Format("[%d-%d]", limit, limit + 9);
		dc.TextOut(textX, textY, strTemp);
	}

	nVertShiftPalaces += 2;
	nVertShiftPalaces += cyCharPalaces;

	// output stars
	dc.SelectObject(m_fontMajorStars);
	GetTextMetrics(dc, &tm);
	int cyCharMajStars = tm.tmHeight + tm.tmExternalLeading;

	int starNumberInBox[12];
	
	for (i = 0; i < 12; i++)
		starNumberInBox[i] = 0;

	// output Tzu Wei and Tien Fu
	/* nBox = m_pInfo->m_tzuWeiCalc->getTzuWei();	
	OutputStar(dc, Constants::tzuWei, nBox, cyChar, boxCornersX[nBox] + 10, boxCornersY[nBox] + nVertShiftPalaces, starNumberInBox, RGB(0, 0, 255));
	nBox = m_pInfo->m_tzuWeiCalc->getTienFu();	
	OutputStar(dc, Constants::tienFu, nBox, cyChar, boxCornersX[nBox] + 10, boxCornersY[nBox] + nVertShiftPalaces, starNumberInBox, RGB(0, 0, 255));
	*/

	for (i = 0; i < Constants::northStarsNum; i++)
	{
		nBox = m_pInfo->m_tzuWeiCalc->m_northStars[i];
		strTemp = Constants::northStarNames[i];
		strTemp += " [";
		strTemp += Constants::northStarNamesEng[i];
		strTemp += "]";
		textX = boxCornersX[nBox] + boxWidth / 16 + horShift;
		OutputStar(dc, strTemp, nBox, cyCharMajStars, textX, boxCornersY[nBox] + nVertShiftPalaces, starNumberInBox);
	}

	for (i = 0; i < Constants::southStarsNum; i++)
	{
		nBox = m_pInfo->m_tzuWeiCalc->m_southStars[i];
		strTemp = Constants::southStarNames[i];
		strTemp += " [";
		strTemp += Constants::southStarNamesEng[i];
		strTemp += "]";
		textX = boxCornersX[nBox] + boxWidth / 16 + horShift;
		OutputStar(dc, strTemp, nBox, cyCharMajStars, textX, boxCornersY[nBox] + nVertShiftPalaces, starNumberInBox);
	}

	// show the borrowed stars
	for (i = 0; i < Constants::majorStarsNum; i++)
	{
		// if the star is borrowed
		if (m_pInfo->m_tzuWeiCalc->m_borrowedStars[i] == true)
		{
			// output it in the opposite palace
			if (i < Constants::northStarsNum)
			{
				nBox = (m_pInfo->m_tzuWeiCalc->m_northStars[i] + 6) % 12;
				textX = boxCornersX[nBox] + boxWidth / 16 + horShift;

				strTemp.Format("(%s)", Constants::northStarNames[i]);
				OutputStar(dc, strTemp, nBox, cyCharMajStars, textX, boxCornersY[nBox] + nVertShiftPalaces, starNumberInBox, RGB(112, 128, 144));
			}
			else
			{
				nBox = (m_pInfo->m_tzuWeiCalc->m_southStars[i - Constants::northStarsNum] + 6) % 12;
				strTemp.Format("(%s)", Constants::southStarNames[i - Constants::northStarsNum]);
				textX = boxCornersX[nBox] + boxWidth / 16 + horShift;
				OutputStar(dc, strTemp, nBox, cyCharMajStars, textX, boxCornersY[nBox] + nVertShiftPalaces, starNumberInBox, RGB(112, 128, 144));
			}
		}
	}
	
	dc.SelectObject(m_fontMinorStars);
	GetTextMetrics(dc, &tm);
	int cyCharMinStars = tm.tmHeight + tm.tmExternalLeading;

	for (i = 0; i < Constants::minorStarsNum; i++)
	{
		nBox = m_pInfo->m_tzuWeiCalc->m_minorStars[i];
		strTemp = Constants::minorStarNames[i];
		strTemp += " [";
		strTemp += Constants::minorStarNamesEng[i];
		strTemp += "]";
		textX = boxCornersX[nBox] + boxWidth / 16 + horShift;
		OutputStar(dc, strTemp, nBox, cyCharMajStars, textX, boxCornersY[nBox] + nVertShiftPalaces, starNumberInBox);
	}

	// write 'created by Steve and Boris (c) 2005
	dc.SelectObject(m_fontCopyright);
	dc.SelectObject(m_copyrightPen);
	GetTextMetrics(dc, &tm);
	int cxCharCopyright = tm.tmAveCharWidth;
	int cyCharCopyright = tm.tmHeight + tm.tmExternalLeading;
	char* pszCopyright = "Created by Steve Kirby and Boris Mazniker (c) 2006. Non-commercial use only.";
	int copX = strlen(pszCopyright) * cxCharCopyright;
	
	dc.Ellipse((windowRect.Width() - copX) / 2 - copX /2 , windowRect.Height() - bottomAreaHeight / 2 - cyCharCopyright, (windowRect.Width() + copX) / 2 + copX /2, windowRect.Height() - bottomAreaHeight / 2 + cyCharCopyright);
	dc.TextOut((windowRect.Width() - copX) / 2, windowRect.Height() - bottomAreaHeight / 2 - cyCharCopyright / 2, pszCopyright);
	dc.SelectObject(m_pen);
}

void CTzuWeiChart::OnPaint()
{
	CPaintDC dc(this); // device context for painting
	// Do not call CWnd::OnPaint() for painting messages
	DrawChart(dc, false);
}

void CTzuWeiChart::DoPrint()
{
	CPrintDialog dlg(FALSE);
	
	// set printer to landscape mode 
	dlg.m_pd.hDevMode = ::GlobalAlloc(GMEM_MOVEABLE, sizeof(DEVMODE));
	LPDEVMODE lp = (LPDEVMODE) ::GlobalLock(dlg.m_pd.hDevMode);
	ZeroMemory(lp, sizeof(DEVMODE));
	lp->dmSize = sizeof(DEVMODE);
	lp->dmFields = DM_ORIENTATION;
	lp->dmOrientation = DMORIENT_LANDSCAPE;
	// pDC->ResetDC( pDV );

	INT_PTR nRC = dlg.DoModal();
		
	BOOL bRes = ::GlobalUnlock( dlg.m_pd.hDevMode );		

	if (nRC != IDOK)
	{
		HGLOBAL hGl = NULL;
		if (dlg.m_pd.hDevMode)
			hGl = ::GlobalFree(dlg.m_pd.hDevMode);

		return;
	}

	// print here
	HDC hdcPrinter = dlg.GetPrinterDC();
	CDC dcPrinter;
	dcPrinter.Attach(hdcPrinter);

	DOCINFO docinfo;
	memset(&docinfo, 0, sizeof(docinfo));
	docinfo.cbSize = sizeof(docinfo);
	docinfo.lpszDocName = _T("Zi Wei Chart");

	// if it fails, complain and exit gracefully
	if (dcPrinter.StartDoc(&docinfo) < 0)
	{
		if (dlg.m_pd.hDevMode)
			::GlobalFree(dlg.m_pd.hDevMode);
		
		AfxMessageBox("The printer could not start printing.");
		
		return;
	}

	// start a page
	if (dcPrinter.StartPage() < 0)
	{
		if (dlg.m_pd.hDevMode)
			::GlobalFree(dlg.m_pd.hDevMode);

		AfxMessageBox("The printer could not start printing the page.");
		
		return;
	}

	CRect rect;
	GetClientRect (&rect);

	CWindowDC dcWindow(NULL);
	CSize logXWin(dcWindow.GetDeviceCaps(LOGPIXELSX), dcWindow.GetDeviceCaps(LOGPIXELSY));
	CSize logXPrn(dcPrinter.GetDeviceCaps(LOGPIXELSX), dcPrinter.GetDeviceCaps(LOGPIXELSY));
	
	dcPrinter.SetMapMode(MM_ANISOTROPIC);
	dcPrinter.SetViewportExt(logXPrn);
	dcPrinter.SetWindowExt(logXWin);
	
	CRect rect2;
	dcPrinter.GetClipBox(&rect2);
	dcPrinter.SetViewportOrg(0, 0);
	dcPrinter.SetWindowOrg(0, -rect2.Height() / 8);

	DrawChart(dcPrinter, true);

	// dcPrinter.TextOut(windowRect.Width() / 4, windowRect.Height() - bottomAreaHeight, "Created by Steve Kirby and Boris Mazniker (c) 2005");
	
	dcPrinter.EndPage();
	dcPrinter.EndDoc();

	DeleteDC(hdcPrinter);

	HGLOBAL hGl = NULL;
	if (dlg.m_pd.hDevMode)
		hGl = ::GlobalFree(dlg.m_pd.hDevMode);
}

void CTzuWeiChart::OnChar(UINT nChar, UINT nRepCnt, UINT nFlags)
{
	// TODO: Add your message handler code here and/or call default
	if ((nChar == 80/*P*/) || (nChar == 112/*p*/))
	{
		DoPrint();
	}

	CWnd::OnChar(nChar, nRepCnt, nFlags);
}
