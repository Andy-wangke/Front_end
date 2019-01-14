:: This batch file trigger and count for fanatic badge...
@echo off
rem set logfile=stackoverflow.log


cmd /k "taskkill /f /IM firefox.exe /T & START "Stackoverflow01" /D "C:\Program Files\Mozilla Firefox\" firefox.exe -height 600 -width 1000 -purgecaches -new-window https://stackoverflow.com/users/6891192/andywang  & timeout 5 & taskkill /f /IM firefox.exe /T &timeout 5 & START "Stackoverflow02" /D "C:\Program Files\Mozilla Firefox\" firefox.exe -height 600 -width 1000 -purgecaches -new-window https://stackoverflow.com/users/6891192/andywang?tab=topactivity & timeout 5 & taskkill /f /IM firefox.exe /T"

rem echo triggering stackoverflow fanatic counter.... >> %logfile%
:: ping stackoverflow.com >> %logfile%
rem echo will be starting firefox at UTC+8 [%date%,%time%] >> %logfile%
rem echo firefox Window 1 running
rem START "Stackoverflow01" /D "C:\Program Files\Mozilla Firefox\" firefox.exe -height 600 -width 1000 -purgecaches -new-window https://stackoverflow.com/users/6891192/andywang >> %logfile%
::type nul>%logfile%
rem timeout 5
rem & taskkill /f /IM firefox.exe /T 
rem taskkill /f firefox.exe
rem START "Stackoverflow02" /D "C:\Program Files\Mozilla Firefox\" firefox.exe -height 600 -width 1000 -purgecaches -new-window https://stackoverflow.com/users/6891192/andywang?tab=topactivity >> %logfile%
rem echo triggering stackoverflow fanatic counter end.... >> %logfile%
rem echo. >> %logfile%
::echo on
rem Macro Execution completed
echo FINISHED!
pause