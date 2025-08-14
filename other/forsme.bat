@echo off
REM === CONFIGURATION ===
set SMEEME_URL=https://smee.io/IkLnqtoK5RUQ1xUU
set LOCAL_TARGET=http://localhost:5678/webhook/61a68f36-4d48-4ba2-a62d-ffd422ce00a1

REM === Start n8n in background ===
echo Starting n8n...
start "" /MIN cmd /c "n8n"

REM === Wait for n8n to come online ===
timeout /t 7 /nobreak >nul

REM === Run Smee exactly as you want ===
echo Forwarding %SMEEME_URL% to %LOCAL_TARGET%
echo Press CTRL+C to stop.
smee -u %SMEEME_URL% --target %LOCAL_TARGET%