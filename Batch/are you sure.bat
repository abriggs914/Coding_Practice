@echo off
setlocal
SET AREYOUSURE=N
:PROMPT
SET /P AREYOUSURE=Are you sure (Y/[N])?
IF /I "%AREYOUSURE%" NEQ "Y" GOTO END

echo what would you like to do?
echo ... rest of file ...


:END

pause
echo goodbye!
endlocal