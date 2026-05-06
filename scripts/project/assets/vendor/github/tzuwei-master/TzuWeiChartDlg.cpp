// TzuWeiChartDlg.cpp : implementation file
//

#include "stdafx.h"
#include "Prototype3.h"
#include "TzuWeiChartDlg.h"
#include ".\tzuweichartdlg.h"
#include "TzuWeiChart.h"

// TzuWeiChartDlg dialog

IMPLEMENT_DYNAMIC(TzuWeiChartDlg, CDialog)
TzuWeiChartDlg::TzuWeiChartDlg(CWnd* pParent /*=NULL*/)
	: CDialog(TzuWeiChartDlg::IDD, pParent)
{
	m_pInfo = NULL;
	m_pChartWnd = NULL;
	m_pBrush = new CBrush(RGB(220, 220, 220));
}

TzuWeiChartDlg::~TzuWeiChartDlg()
{
	delete m_pBrush;
}

void TzuWeiChartDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
}


BEGIN_MESSAGE_MAP(TzuWeiChartDlg, CDialog)
	ON_BN_CLICKED(IDOK, OnBnClickedOk)
	ON_WM_ERASEBKGND()
	ON_WM_SHOWWINDOW()
END_MESSAGE_MAP()


// TzuWeiChartDlg message handlers
BOOL TzuWeiChartDlg::OnInitDialog()
{
	CDialog::OnInitDialog();

	/* FINISH IT!
	int nLeft = 10;
	int nUp = 10;
	
	CRect rc(nLeft, nUp, nLeft + GetSystemMetrics(SM_CXSCREEN) / 4 * 3, nUp + GetSystemMetrics(SM_CYSCREEN) / 10 * 9);
	this->MoveWindow(rc);*/

	CRect rect;
	GetClientRect(&rect);
	rect.top = 10;
	rect.left = 10;
	rect.right = rect.right - 10;
	rect.bottom = rect.bottom - rect.Height() / 12;

	// cs.x = nLeft;
	// cs.y = nUp;
	// cs.cx = GetSystemMetrics(SM_CXSCREEN) / 4 * 3;
	// cs.cy = GetSystemMetrics(SM_CYSCREEN) / 4 * 3;

	m_pChartWnd = new CTzuWeiChart(m_pInfo);
	CString strTitle = _T("Zi Wei Chart");
	if (m_pInfo->m_name.GetLength() != 0)
	{
		strTitle += _T(" of ");
		strTitle += m_pInfo->m_name;
	}

	this->SetWindowText(strTitle);

	m_pChartWnd->Create(NULL, _T(""), WS_CHILD | WS_VISIBLE,
		rect, this, 0, 0);

	m_pInfo = NULL;

	return TRUE;  // return TRUE unless you set the focus to a control
	// EXCEPTION: OCX Property Pages should return FALSE
}

void TzuWeiChartDlg::OnBnClickedOk()
{
	// print here
	m_pChartWnd->DoPrint();
	// OnOK();
}

BOOL TzuWeiChartDlg::OnEraseBkgnd(CDC* pDC)
{
	// TODO: Add your message handler code here and/or call default
	ASSERT_VALID(pDC);

	CBrush* pOldBrush = pDC->SelectObject(m_pBrush);

    CRect rect;
    pDC->GetClipBox(&rect);     // Erase the area needed
    pDC->PatBlt(rect.left, rect.top, rect.Width(), rect.Height(), PATCOPY);
    pDC->SelectObject(pOldBrush);

    return TRUE;
	// return CDialog::OnEraseBkgnd(pDC);
}


void TzuWeiChartDlg::OnShowWindow(BOOL bShow, UINT nStatus)
{
	CDialog::OnShowWindow(bShow, nStatus);

	// TODO: Add your message handler code here
}
