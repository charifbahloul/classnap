@echo off

@REM Change into the directory of this batch file.
cd %~dp0

@REM Sleep.
ping localhost -n 7 > nul


@REM Open http://127.0.0.1:5000/
start chrome http://127.0.0.1:5000/

exit