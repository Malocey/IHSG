@echo off
echo #############################
echo #   Building Executable   #
echo #############################
echo.

REM Optional: Create a virtual environment
REM python -m venv venv
REM call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Run PyInstaller
pyinstaller build.spec --noconfirm

REM Optional: Deactivate virtual environment
REM deactivate

echo.
echo #############################
echo #    Build Complete!      #
echo #############################
echo Executable is in the 'dist' folder.
echo.
pause