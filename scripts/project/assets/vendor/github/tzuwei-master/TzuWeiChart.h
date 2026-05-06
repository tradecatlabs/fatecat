#pragma once


// CTzuWeiChart
#include "TzuWei.h"

class CTzuWeiChart : public CWnd
{
	DECLARE_DYNAMIC(CTzuWeiChart)

private:
	void OutputStar(CDC& dc, CString& strStarName, int nBox, int cyChar, int leftCorner, int topCorner, int* starNumberInBox, COLORREF col = 0);
private:
	TzuWeiFullInfo* m_pInfo;
	CFont m_fontName, m_fontPillars, m_fontPalaces, m_fontMajorStars, m_fontMinorStars, m_fontCentralHeader;
	CFont m_fontCopyright;
	CPen m_pen, m_copyrightPen;
public:

	CTzuWeiChart(TzuWeiFullInfo* pInfo);
	virtual ~CTzuWeiChart();

	BOOL PreCreateWindow(CREATESTRUCT& cs);
	
	virtual void PostNcDestroy();
	void DoPrint();
	void DrawChart(CDC& dc, bool bPrinter);
protected:
	DECLARE_MESSAGE_MAP()
public:
	afx_msg void OnPaint();
	afx_msg void OnChar(UINT nChar, UINT nRepCnt, UINT nFlags);
};


