@echo off
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Installing build tools...
pip install pyinstaller

echo.
echo Setup complete!
echo You can now build the EXE using: python main.py
pause
