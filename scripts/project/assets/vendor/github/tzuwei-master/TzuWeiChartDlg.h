#pragma once

#include "TzuWei.h"
#include "TzuWeiChart.h"

// TzuWeiChartDlg dialog

class TzuWeiChartDlg : public CDialog
{
	DECLARE_DYNAMIC(TzuWeiChartDlg)

public:
	TzuWeiChartDlg(CWnd* pParent = NULL);   // standard constructor
	virtual ~TzuWeiChartDlg();
	void SetInfo(TzuWeiFullInfo* pInfo)
	{
		m_pInfo = pInfo;
	}
private:
	TzuWeiFullInfo* m_pInfo;
	CTzuWeiChart* m_pChartWnd;
	CBrush*		  m_pBrush;
// Dialog Data
	enum { IDD = IDD_TZUWEICHARTDLG };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

	DECLARE_MESSAGE_MAP()
public:
	virtual BOOL OnInitDialog();
	afx_msg void OnBnClickedOk();
	afx_msg BOOL OnEraseBkgnd(CDC* pDC);
	afx_msg void OnShowWindow(BOOL bShow, UINT nStatus);
};
