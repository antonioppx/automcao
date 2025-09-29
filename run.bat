@echo off
title Instagram Automation
echo.
echo ========================================
echo    INSTAGRAM AUTOMATION
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale o Python 3.7 ou superior.
    pause
    exit /b 1
)

REM Verificar se requirements.txt existe
if not exist "requirements.txt" (
    echo ERRO: Arquivo requirements.txt nao encontrado!
    pause
    exit /b 1
)

REM Instalar dependências se necessário
echo Verificando dependencias...
pip show selenium >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERRO: Falha ao instalar dependencias!
        pause
        exit /b 1
    )
)

REM Executar o programa principal
echo.
echo Iniciando Instagram Automation...
echo.
python main.py

REM Pausar para ver mensagens de erro se houver
if errorlevel 1 (
    echo.
    echo ERRO: Programa terminou com erro!
    pause
)