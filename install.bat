@echo off
echo ========================================
echo    INSTAGRAM FOLLOW BOT - INSTALADOR
echo ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale Python 3.7 ou superior
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python encontrado!
echo.

echo Instalando dependencias...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERRO: Falha ao instalar dependencias!
    pause
    exit /b 1
)

echo.
echo ========================================
echo    INSTALACAO CONCLUIDA COM SUCESSO!
echo ========================================
echo.
echo Para executar o programa, use:
echo    python main.py
echo.
echo Ou execute o arquivo run.bat
echo.
pause
