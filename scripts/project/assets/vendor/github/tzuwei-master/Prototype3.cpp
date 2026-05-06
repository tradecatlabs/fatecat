// Prototype3.cpp : Defines the class behaviors for the application.
//

#include "stdafx.h"
#include "Prototype3.h"
#include "Prototype3Dlg.h"
#include ".\prototype3.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


// CPrototype3App

BEGIN_MESSAGE_MAP(CPrototype3App, CWinApp)
	ON_COMMAND(ID_HELP, CWinApp::OnHelp)
END_MESSAGE_MAP()


// CPrototype3App construction

CPrototype3App::CPrototype3App()
{
	// TODO: add construction code here,
	// Place all significant initialization in InitInstance
}

// The one and only CPrototype3App object

CPrototype3App theApp;

// CPrototype3App initialization

BOOL CPrototype3App::InitInstance()
{
	// InitCommonControls() is required on Windows XP if an application
	// manifest specifies use of ComCtl32.dll version 6 or later to enable
	// visual styles.  Otherwise, any window creation will fail.
	InitCommonControls();

	CWinApp::InitInstance();

	AfxEnableControlContainer();

	// Standard initialization
	// If you are not using these features and wish to reduce the size
	// of your final executable, you should remove from the following
	// the specific initialization routines you do not need
	// Change the registry key under which our settings are stored
	// TODO: You should modify this string to be something appropriate
	// such as the name of your company or organization
	SetRegistryKey(_T("Local AppWizard-Generated Applications"));

    HRESULT hRes = CoInitializeEx(NULL, COINIT_MULTITHREADED);

	CPrototype3Dlg dlg;
	m_pMainWnd = &dlg;
	INT_PTR nResponse = dlg.DoModal();
	if (nResponse == IDOK)
	{
		// TODO: Place code here to handle when the dialog is
		//  dismissed with OK
	}
	else if (nResponse == IDCANCEL)
	{
		// TODO: Place code here to handle when the dialog is
		//  dismissed with Cancel
	}

	// Since the dialog has been closed, return FALSE so that we exit the
	//  application, rather than start the application's message pump.
	return FALSE;
}

int CPrototype3App::ExitInstance()
{
	// TODO: Add your specialized code here and/or call the base class
	CoUninitialize();

	return CWinApp::ExitInstance();
}
