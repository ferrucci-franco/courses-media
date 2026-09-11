@echo off
REM Regenere les pages du site et les QR codes, puis montre l'etat git.
REM Arguments transmis a make_qr.py :  update.cmd --size 22 --png
setlocal
cd /d "%~dp0"

set "PY="
call :find_py "C:\Users\ferrucci\miniforge3\envs\thesys_01\python.exe"
if not defined PY call :find_py python
if not defined PY call :find_py py

if not defined PY (
    echo.
    echo Aucun interpreteur Python avec le module segno n'a ete trouve.
    echo Installez-le, par exemple :
    echo     C:\Users\ferrucci\miniforge3\envs\thesys_01\python.exe -m pip install segno
    exit /b 1
)

echo Interpreteur : %PY%
echo.
"%PY%" tools\make_index.py || exit /b 1
echo.
"%PY%" tools\make_qr.py %* || exit /b 1
echo.
echo --- git status ---
git status --short
echo.
echo Si tout est correct :
echo     git add -A ^&^& git commit -m "votre message" ^&^& git push
exit /b 0

:find_py
%~1 -c "import segno" >nul 2>&1
if errorlevel 1 goto :eof
set "PY=%~1"
goto :eof
