@echo off
rem Start the long jobs on a Windows machine. Double-click this file, or run it in a terminal.
rem For two machines: run_windows.bat --part 1/2 on the first, --part 2/2 on the second.
cd /d "%~dp0.."
if not exist .venv (
  py -3 -m venv .venv || python -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r cluster\requirements.txt || goto :error
python cluster\run_cluster.py --smoke || goto :error
python cluster\run_cluster.py %* || goto :error
python cluster\run_cluster.py --pack || goto :error
echo.
echo FINISHED. Send back the file results_cluster_out_*.zip in this folder.
pause
exit /b 0
:error
echo.
echo ERROR. Send back the file cluster_out\progress.log (or a photo of this window).
pause
exit /b 1
