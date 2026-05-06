// Prototype3Dlg.h : header file
//

#pragma once
#include "afxwin.h"
#include <string>
#include "Prototype3.h"

#ifdef _UNICODE
	typedef std::wstring	_tstring;
#else
	typedef std::string		_tstring;
#endif

using namespace std;

// CPrototype3Dlg dialog
class CPrototype3Dlg : public CDialog
{
// Construction
public:
	CPrototype3Dlg(CWnd* pParent = NULL);	// standard constructor

// Dialog Data
	enum { IDD = IDD_PROTOTYPE3_DIALOG };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV support


// Implementation
protected:
	HICON m_hIcon;

	// Generated message map functions
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
	CComboBox m_ctrlYear;
	CComboBox m_ctrlMonth;
	afx_msg void OnBnClickedOk();
	CComboBox m_ctrlDay;
private:
	// map < int, _tstring > m_months;
	CComboBox m_ctrlHour;
	CComboBox m_ctrlMin;
	CComboBox m_ctrlTZ;
public:
	afx_msg void OnBnClickedButton1();
	CEdit m_ctrlName;
	CStatic m_grBoxGender;
	CButton m_genderMale;
	afx_msg void OnUpdateUIState(UINT /*nAction*/, UINT /*nUIElement*/);
private:
	// the only resource object
	CMyResource m_myResource;
public:
	afx_msg void OnEnChangeName();
	CButton m_btnBuildChart;
	CButton m_btnSaveProfile;
	afx_msg void OnBnClickedSaveprofile();
	afx_msg void OnBnClickedLoadprofile();
	CButton m_genderFemale;
};
