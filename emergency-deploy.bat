@echo off
REM Emergency clean deployment script for Windows

echo 🚨 EMERGENCY STREAMLIT DEPLOYMENT CLEANUP
echo ===========================================

REM Remove corrupted files
echo 🗑️ Removing corrupted files...
if exist requirements.txt del requirements.txt

REM Create ultra-minimal requirements.txt
echo 📝 Creating clean requirements.txt...
echo streamlit> requirements.txt

REM Verify file contents
echo ✅ Verifying requirements.txt contents:
type requirements.txt

echo.
echo 🚀 Ready to deploy with:
echo    - app.py (working Streamlit app)
echo    - requirements.txt (only 'streamlit')
echo.
echo Deploy commands:
echo    git add .
echo    git commit -m "Emergency clean deployment"
echo    git push
echo.
echo This WILL work! 🎉