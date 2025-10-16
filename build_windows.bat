@echo off
REM This script builds the executable for Windows.

echo ========================================
echo Building Idle Horde Slayer for Windows...
echo ========================================

REM Activate virtual environment if it exists
IF EXIST venv (
    echo --- Activating virtual environment ---
    call venv\Scripts\activate
) ELSE (
    echo --- WARNING: No virtual environment found. Using system Python. ---
)

echo.
echo --- Running PyInstaller ---
pyinstaller build.spec

echo.
echo ========================================
echo Build complete!
echo The executable can be found in the 'dist\IdleHordeSlayer' folder.
echo ========================================
echo.

REM Pause to allow the user to see the output.
pause