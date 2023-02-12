@REM I want to change into wherever this directory is and run app.py.

@echo off

@REM Change into the directory of this batch file.
cd %~dp0

@REM Install the requirements.
pip install -r requirements.txt

@REM Open openWebsite.bat so that the website opens.
start openWebsite.bat

@REM Run the app.
python app.py