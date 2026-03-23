@echo off
REM ThreatWatch — Windows Setup Script
REM Run this from inside your virtual environment

echo.
echo ============================================
echo  ThreatWatch Windows Installation Helper
echo ============================================
echo.

REM Step 1: Upgrade pip first
echo [1/5] Upgrading pip...
python.exe -m pip install --upgrade pip --quiet

REM Step 2: Install numpy with wheel first (pandas needs it)
echo [2/5] Installing numpy...
pip install "numpy==1.26.4" --quiet

REM Step 3: Install pandas using a prebuilt wheel
echo [3/5] Installing pandas (prebuilt wheel)...
pip install "pandas==2.1.4" --quiet
IF %ERRORLEVEL% NEQ 0 (
    echo WARNING: pandas 2.1.4 failed, trying pandas 2.0.3...
    pip install "pandas==2.0.3" --quiet
)

REM Step 4: Install everything else
echo [4/5] Installing remaining packages...
pip install Flask==3.0.3 Flask-SQLAlchemy==3.1.1 Flask-Login==0.6.3 Flask-WTF==1.2.1 Werkzeug==3.0.3 SQLAlchemy==2.0.31 --quiet
pip install scikit-learn==1.4.2 joblib==1.4.2 --quiet
pip install requests==2.32.3 fpdf2==2.7.9 python-dotenv==1.0.1 --quiet
pip install scapy==2.5.0 --quiet

echo [5/5] Done!
echo.
echo ============================================
echo  Verifying installation...
echo ============================================
python -c "import flask; print('Flask:', flask.__version__)"
python -c "import flask_sqlalchemy; print('Flask-SQLAlchemy: OK')"
python -c "import flask_login; print('Flask-Login: OK')"
python -c "import pandas; print('pandas:', pandas.__version__)"
python -c "import sklearn; print('scikit-learn:', sklearn.__version__)"
python -c "import scapy; print('Scapy: OK')"
echo.
echo If all lines above printed OK, run:
echo   python seed_data.py
echo   python app.py
echo.
echo NOTE: Scapy packet capture on Windows requires Npcap.
echo Download from: https://npcap.com/
echo.
pause
