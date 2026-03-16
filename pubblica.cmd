@echo off
cd /d "%~dp0"
echo Aggiorno i post...
python scripts/update-posts.py
echo.
echo Invio su GitHub...
git add -A
git commit -m "Aggiorna contenuto"
git push origin main
echo.
echo Pubblicato!
pause
