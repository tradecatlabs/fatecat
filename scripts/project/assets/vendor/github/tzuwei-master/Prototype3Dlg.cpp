// Prototype3Dlg.cpp : implementation file
//

#include "stdafx.h"
#include "Prototype3.h"
#include "Prototype3Dlg.h"
#include ".\prototype3dlg.h"
#include "TzuWei.h"
#include "TestTzuWei.h"
#include "TzuWeiChartDlg.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif

const TCHAR* profileDelimiter = _T(":");
// CAboutDlg dialog used for App About

class CAboutDlg : public CDialog
{
public:
	CAboutDlg();

// Dialog Data
	enum { IDD = IDD_ABOUTBOX };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

// Implementation
protected:
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialog(CAboutDlg::IDD)
{
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialog)
END_MESSAGE_MAP()


// CPrototype3Dlg dialog



CPrototype3Dlg::CPrototype3Dlg(CWnd* pParent /*=NULL*/)
	: CDialog(CPrototype3Dlg::IDD, pParent)
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CPrototype3Dlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	DDX_Control(pDX, IDC_YEAR, m_ctrlYear);
	DDX_Control(pDX, IDC_MONTH, m_ctrlMonth);
	DDX_Control(pDX, IDC_DAY, m_ctrlDay);
	DDX_Control(pDX, IDC_HOUR, m_ctrlHour);
	DDX_Control(pDX, IDC_MIN, m_ctrlMin);
	DDX_Control(pDX, IDC_TZ, m_ctrlTZ);
	DDX_Control(pDX, IDC_NAME, m_ctrlName);
	DDX_Control(pDX, IDC_GRBOX_GENDER, m_grBoxGender);
	DDX_Control(pDX, IDC_GENDER_MALE, m_genderMale);
	DDX_Control(pDX, IDC_GENDER_FEMALE, m_genderFemale);
	DDX_Control(pDX, IDOK, m_btnBuildChart);
	DDX_Control(pDX, IDSAVEPROFILE, m_btnSaveProfile);
	DDX_Control(pDX, IDCANCEL, m_genderFemale);
}

BEGIN_MESSAGE_MAP(CPrototype3Dlg, CDialog)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	//}}AFX_MSG_MAP
	ON_BN_CLICKED(IDOK, OnBnClickedOk)
	ON_BN_CLICKED(IDC_BUTTON1, OnBnClickedButton1)
	ON_EN_CHANGE(IDC_NAME, OnEnChangeName)
	ON_BN_CLICKED(IDSAVEPROFILE, OnBnClickedSaveprofile)
	ON_BN_CLICKED(IDLOADPROFILE, OnBnClickedLoadprofile)
END_MESSAGE_MAP()


// CPrototype3Dlg message handlers

BOOL CPrototype3Dlg::OnInitDialog()
{
	CDialog::OnInitDialog();

	// Add "About..." menu item to system menu.

	// IDM_ABOUTBOX must be in the system command range.
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	ASSERT((IDM_LOCALTZ & 0xFFF0) == IDM_LOCALTZ);
	ASSERT(IDM_LOCALTZ < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != NULL)
	{
		CString strAboutMenu;
		strAboutMenu.LoadString(IDS_ABOUTBOX);

		/* CString strLocalTZ;
		strLocalTZ.LoadString(IDS_LOCALTZ);

		pSysMenu->AppendMenu(MF_SEPARATOR);
		pSysMenu->AppendMenu(MF_STRING, IDM_LOCALTZ, strLocalTZ);
		pSysMenu->CheckMenuItem(IDM_LOCALTZ, MF_CHECKED | MF_BYCOMMAND);*/

		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// Set the icon for this dialog.  The framework does this automatically
	//  when the application's main window is not a dialog
	SetIcon(m_hIcon, TRUE);			// Set big icon
	SetIcon(m_hIcon, FALSE);		// Set small icon

	CString tempString;
	int i;

	for (i = 0; i < 150; i++)
	{
		tempString.Format(_T("%d"), i + 1885);
		this->m_ctrlYear.InsertString(i, tempString);
	}

	/* for (map< int, _tstring >::iterator itr = m_months.begin(); itr != m_months.end(); itr++)
	{
		int temp = (*itr).first;
		const TCHAR* pszTemp = (*itr).second.c_str();
		this->m_ctrlMonth.InsertString(temp - 1, pszTemp);
	}*/
	for (i = 0; i < 12; i++)
	{
		tempString = Constants::months[i];
		this->m_ctrlMonth.InsertString(i, tempString);
	}

	for (i = 1; i <= 31; i++)
	{
		tempString.Format(_T("%d"), i);
		this->m_ctrlDay.InsertString(i-1, tempString);
	}
	
	for (i = 0; i < 24; i++)
	{
		int tempInt = i % 12;
		
		if (tempInt == 0)
			tempInt = 12;

		tempString.Format(_T("%d"), tempInt);
		if (i < 12)
			tempString += _T(" a.m.");
		else
			tempString += _T(" p.m.");

		this->m_ctrlHour.InsertString(i, tempString);
	}
	
	for (i = 0; i <= 59; i++)
	{
		tempString.Format(_T("%d"), i);
		this->m_ctrlMin.InsertString(i, tempString);
	}

	for (i = -12; i <= 12; i++)
	{
		if (i == 0)
			tempString = _T("GMT");
		else
			tempString.Format(_T("GMT %s%d"), i > 0 ? "+":"", i);

		this->m_ctrlTZ.InsertString(i + 12, tempString);
	}

	this->m_ctrlYear.SetCurSel(85);
	this->m_ctrlMonth.SetCurSel(0);
	this->m_ctrlDay.SetCurSel(0);
	this->m_ctrlHour.SetCurSel(12);
	this->m_ctrlMin.SetCurSel(0);
	this->m_ctrlTZ.SetCurSel(4);

	this->m_ctrlName.SetWindowText(_T(""));
	
	this->CheckRadioButton(IDC_GENDER_MALE, IDC_GENDER_FEMALE, IDC_GENDER_FEMALE);
	this->m_btnBuildChart.EnableWindow(FALSE);
	this->m_btnSaveProfile.EnableWindow(FALSE);
	
	return TRUE;  // return TRUE  unless you set the focus to a control
}

void CPrototype3Dlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else 	/* if ((nID & 0xFFF0) == IDM_LOCALTZ)
	{
		CMenu* pSysMenu = GetSystemMenu(FALSE);
		if (pSysMenu != NULL)
		{
			UINT state = pSysMenu->GetMenuState(IDM_LOCALTZ, MF_BYCOMMAND);
		    ASSERT(state != 0xFFFFFFFF);

			if (state & MF_CHECKED)
				pSysMenu->CheckMenuItem(IDM_LOCALTZ, MF_UNCHECKED | MF_BYCOMMAND);
			else
				pSysMenu->CheckMenuItem(IDM_LOCALTZ, MF_CHECKED | MF_BYCOMMAND);
		}
	}
	else */
	{
		CDialog::OnSysCommand(nID, lParam);
	}
}

// If you add a minimize button to your dialog, you will need the code below
//  to draw the icon.  For MFC applications using the document/view model,
//  this is automatically done for you by the framework.

void CPrototype3Dlg::OnPaint() 
{
	if (IsIconic())
	{
		CPaintDC dc(this); // device context for painting

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// Center icon in client rectangle
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// Draw the icon
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialog::OnPaint();
	}
}

// The system calls this function to obtain the cursor to display while the user drags
//  the minimized window.
HCURSOR CPrototype3Dlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}

void CPrototype3Dlg::OnBnClickedOk()
{
	CString yearText, monthText, dayText, hourText, minText, tzText, nameText;

	CString name;
	m_ctrlName.GetWindowText(name);
	if (name.GetLength() == 0)
	{
		AfxMessageBox("Please, type a valid name!");
		
		return;
	}

	m_ctrlYear.GetWindowText(yearText); 
	m_ctrlMonth.GetWindowText(monthText); 
	m_ctrlDay.GetWindowText(dayText); 
	m_ctrlHour.GetWindowText(hourText); 
	m_ctrlMin.GetWindowText(minText); 
	m_ctrlTZ.GetWindowText(tzText); 
	m_ctrlName.GetWindowText(nameText);

	int curYear, curMonth, curDay, curHour, curMin, curTZ;

	curYear = _ttoi(yearText);
	if (curYear < 1885)
	{
		AfxMessageBox("For now, this program only works for dates later than 1884. Please, try again");
		
		return;
	}

	curMonth = -1;

	for (int i = 0; i < 12; i++)
	{
		if (monthText.CompareNoCase(Constants::months[i]) == 0)
		{
			curMonth = i + 1;

			break;
		}
	}
	/* for (map< int, _tstring >::iterator itr = m_months.begin(); itr != m_months.end(); itr++)
	{
		if (monthText.CompareNoCase((*itr).second.c_str()) == 0)
		{
			curMonth = (*itr).first;

			break;
		}
	}*/
	
	if (curMonth == -1)
	{
		// this month is not a valid month
		AfxMessageBox("This month is not a valid month. Please, try again");
		
		return;
	}

	curDay = _ttoi(dayText);
	if (curDay < 1 || curDay > 31)
	{
		AfxMessageBox("Invalid day entry. Please, try again");
		
		return;
	}

	// get hour 
	curHour = _ttoi(hourText);
	if (curHour == 12)
		curHour = 0;

	if ((hourText.GetLength() > 4) && (hourText.GetAt(hourText.GetLength() - 4) == 'p'))
		curHour = curHour + 12;

	if (curHour < 0 || curHour > 23)
	{
		AfxMessageBox("Invalid hour entry. Please, try again");
		
		return;
	}

	// get minute
	curMin = _ttoi(minText);
	
	if (curMin < 0 || curMin > 59)
	{
		AfxMessageBox("Invalid minute entry. Please, try again");
		
		return;
	}
	
	// get timzone
	if ((tzText.Mid(0, 3).CompareNoCase(_T("GMT")) != 0) || (tzText.GetLength() < 3))
	{
		AfxMessageBox("This timezone is not valid. Please, try again");

		return;
	}

	if (tzText.CompareNoCase(_T("GMT")) == 0)
		curTZ = 0;
	else
		curTZ = _ttoi(tzText.Mid(4, tzText.GetLength() - 4));

	bool bMale;
	if (this->m_genderMale.GetCheck() == BST_CHECKED)
		bMale = true;
	else
		bMale = false;
	
	// way of calculating time zone
	/* bool bTestLocalTZ = false;

	CMenu* pSysMenu = GetSystemMenu(FALSE);

	UINT state = pSysMenu->GetMenuState(IDM_LOCALTZ, MF_BYCOMMAND);
	if (state & MF_CHECKED)
		bTestLocalTZ = true;*/

	SunDate* pSunDate = new SunDate(curYear, curMonth, curDay, curHour, curMin, curTZ);
	
	// AfxMessageBox("Debug Message : Before getting the moon date.");

	CString errorMessage;
	MoonDate* pMoonDate = new MoonDate();

	bool bRes = pMoonDate->Initialize(*pSunDate, errorMessage, m_myResource.m_pszData );
	if (!bRes)
	{
		AfxMessageBox(errorMessage, MB_OK | MB_ICONSTOP);
		
		return;
	}

	// AfxMessageBox("Debug Message : After getting the moon date.");
	BirthCharacters* pBirthChars = new BirthCharacters(*pSunDate, *pMoonDate);

	TzuWeiCalc* pTzuWei = new TzuWeiCalc(*pBirthChars, *pSunDate, *pMoonDate, bMale);
	TzuWeiFullInfo* pInfo = new TzuWeiFullInfo(nameText, bMale, pSunDate, pMoonDate, pBirthChars, pTzuWei);

	// draw the window
	TzuWeiChartDlg dlg(this);
	dlg.SetInfo(pInfo);
	dlg.DoModal();
}

void CPrototype3Dlg::OnBnClickedButton1()
{
	// TestCalculations();
	// CalcZeroDay();
//	FullTestChineseCalendarComp();
}

void CPrototype3Dlg::OnEnChangeName()
{
	CString strName = "";
	this->m_ctrlName.GetWindowText(strName);
	if (strName.GetLength() == 0)
	{
		this->m_btnBuildChart.EnableWindow(FALSE);
		this->m_btnSaveProfile.EnableWindow(FALSE);
	}
	else
	{
		this->m_btnBuildChart.EnableWindow(TRUE);
		this->m_btnSaveProfile.EnableWindow(TRUE);
	}
}

void CPrototype3Dlg::OnBnClickedSaveprofile()
{
	// TODO: Add your control notification handler code here
	CFileDialog* pDialog = new CFileDialog(FALSE, _T("wei"), NULL, OFN_HIDEREADONLY | OFN_OVERWRITEPROMPT, _T("Zi Wei Files (*.wei)|*.wei|All Files (*.*)|*.*||"), NULL);

    if (pDialog->DoModal() == IDOK)
	{
		// open the file
		CFile fWrite;
		CFileException ex; 

		if (!fWrite.Open(pDialog->GetPathName(), CFile::modeWrite |
            CFile::shareExclusive | CFile::modeCreate, &ex))
	    {
			AfxMessageBox("File creation error! Please, try again.");
			
			return;
		}

		CString strTemp;
		this->m_ctrlName.GetWindowText(strTemp);
		strTemp = _T("name=") + strTemp;
		strTemp += _T("\n");
		fWrite.Write(strTemp, strTemp.GetLength() * sizeof(TCHAR));

		strTemp = _T("date=");

		CString strTemp2;
		
		this->m_ctrlYear.GetWindowText(strTemp2);
		strTemp += strTemp2;
		strTemp += profileDelimiter;
		this->m_ctrlMonth.GetWindowText(strTemp2);
		strTemp += strTemp2;
		strTemp += profileDelimiter;
		this->m_ctrlDay.GetWindowText(strTemp2);
		strTemp += strTemp2;
		strTemp += profileDelimiter;
		this->m_ctrlHour.GetWindowText(strTemp2);
		strTemp += strTemp2;
		strTemp += profileDelimiter;
		this->m_ctrlMin.GetWindowText(strTemp2);
		strTemp += strTemp2;
		strTemp += profileDelimiter;
		this->m_ctrlTZ.GetWindowText(strTemp2);
		
		if (strTemp2.CompareNoCase(_T("GMT")) == 0)
			strTemp2 = _T("0");
		else 
		{
			strTemp2 = strTemp2.Mid(4, strTemp2.GetLength() - 4);
			if (strTemp2.Left(1).Compare(_T("+")) == 0)
			{
				strTemp2 = strTemp2.Right(strTemp2.GetLength() - 1);
			}
		}

		strTemp += strTemp2;
		strTemp += _T("\n");

		fWrite.Write(strTemp, strTemp.GetLength() * sizeof(TCHAR));

		strTemp=_T("gender=");
		if (this->m_genderMale.GetCheck() == BST_CHECKED)
			strTemp += _T("true");
		else
			strTemp += _T("false");

		strTemp += _T("\n");
		
		fWrite.Write(strTemp, strTemp.GetLength() * sizeof(TCHAR));

		fWrite.Close();

		AfxMessageBox("Your profile has been saved!");
	}
}

void CPrototype3Dlg::OnBnClickedLoadprofile()
{
	CFileDialog* pDialog = new CFileDialog(TRUE, _T("wei"), NULL, NULL, _T("Zi Wei Files (*.wei)|*.wei|All Files (*.*)|*.*||"), NULL);

    if (pDialog->DoModal() == IDOK)
	{
		// open the file
		FILE* fRead = _tfopen(pDialog->GetPathName(), "r");
		
		if (fRead == NULL)
	    {
			AfxMessageBox("Error when trying to load file! Please, try again.");
			
			return;
		}
		TCHAR pszTemp[200];
		while (_fgetts(pszTemp, 200, fRead) != NULL)
		{
			CString strTemp = pszTemp;
			int nIdx = strTemp.Find(_T("="));
			if (nIdx == -1)
				continue;

			CString strKey = strTemp.Left(nIdx);
			CString strValue = strTemp.Right(strTemp.GetLength() - nIdx - 1);
			if (strKey.Compare(_T("name")) == 0)
			{
				this->m_ctrlName.SetWindowText(strValue);
			}
			else if (strKey.Compare(_T("date")) == 0)
			{
				int nStart = 0;
				CString strTemp2 = strValue.Tokenize(profileDelimiter, nStart);
				this->m_ctrlYear.SetWindowText(strTemp2);
				strTemp2 = strValue.Tokenize(profileDelimiter, nStart);
				this->m_ctrlMonth.SetWindowText(strTemp2);
				strTemp2 = strValue.Tokenize(profileDelimiter, nStart);
				this->m_ctrlDay.SetWindowText(strTemp2);
				strTemp2 = strValue.Tokenize(profileDelimiter, nStart);
				this->m_ctrlHour.SetWindowText(strTemp2);
				strTemp2 = strValue.Tokenize(profileDelimiter, nStart);
				this->m_ctrlMin.SetWindowText(strTemp2);

				// time zone
				strTemp2 = strValue.Tokenize(profileDelimiter, nStart);
				int tz = _tstoi(strTemp2);
				this->m_ctrlTZ.SetCurSel(tz + 12);
			}
			else if (strKey.Compare(_T("gender")) == 0)
			{
				if (strValue.Trim().CompareNoCase(_T("true")) == 0)
				{
					this->m_genderMale.SetCheck(BST_CHECKED);
					this->m_genderFemale.SetCheck(BST_UNCHECKED);
				}
				else
				{
					this->m_genderMale.SetCheck(BST_UNCHECKED);
					this->m_genderFemale.SetCheck(BST_CHECKED);
				}
			}
		}

		fclose(fRead);

		AfxMessageBox("Your profile has been loaded!");
	}
}
