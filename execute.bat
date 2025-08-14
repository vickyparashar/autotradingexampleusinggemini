@echo off
setlocal

set "BASEDIR=%~dp0"
pushd "%BASEDIR%" || exit /b 1

call ".\venv\Scripts\activate.bat" || (popd & exit /b 1)

python ".\takescreenshot.py"
set "RC=%ERRORLEVEL%"

popd
endlocal & exit /b %RC%