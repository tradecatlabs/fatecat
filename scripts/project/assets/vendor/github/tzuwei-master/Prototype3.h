// Prototype3.h : main header file for the PROJECT_NAME application
//

#pragma once

#ifndef __AFXWIN_H__
	#error include 'stdafx.h' before including this file for PCH
#endif

#include "resource.h"		// main symbols


// CPrototype3App:
// See Prototype3.cpp for the implementation of this class
//

class CPrototype3App : public CWinApp
{
public:
	CPrototype3App();

// Overrides
	public:
	virtual BOOL InitInstance();

// Implementation

	DECLARE_MESSAGE_MAP()
	virtual int ExitInstance();
};

extern CPrototype3App theApp;

class CMyResource
{
public:
	CMyResource()
	{
		m_pszData = 0;

		TCHAR  sResName[5]  = _T("#130");
		TCHAR sRestype[13] = _T("TEXTFILE");
		HRSRC hres = FindResource(NULL, sResName, sRestype);
		if (hres == 0)
		{ 
			AfxMessageBox(_T("An Error Occurred.\n Could Not Locate Resource File."));
			return;
        }
        
        //If resource is found a handle to the resource is returned
        //now just load the resource
		HGLOBAL    hbytes = LoadResource(NULL, hres);

		// Lock the resource
		LPVOID pdata = LockResource(hbytes);

        //Convert the resource text file to data we can use
		char* pszResData = (char*) pdata;
		char* pszFind = strstr(pszResData, "-end-of-file-");
		long nBytes = pszFind - pszResData + strlen("-end-of-file-") + 1;
		m_pszData = new char[nBytes + 1];
		strncpy(m_pszData, pszResData, nBytes);
		m_pszData[nBytes] = 0;

		ATLTRACE("before strtok\n");
		// put 0 at all the end-of-line symbols
		char* line1; 
		line1 = strtok(m_pszData, "\n");
		
		while (line1 != NULL)
		{ 
			line1 = strtok(NULL, "\n");
		}

		ATLTRACE("after strtok\n");
	}

	virtual ~CMyResource()
	{
		delete m_pszData;
	}
	
	char* m_pszData;
};
