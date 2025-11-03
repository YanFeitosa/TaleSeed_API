@echo off
echo.
echo ========================================
echo   TaleSeed API - Inicializando...
echo ========================================
echo.

REM Verifica se o arquivo .env existe
if not exist .env (
    echo [AVISO] Arquivo .env nao encontrado!
    echo.
    echo Por favor, crie um arquivo .env baseado no .env.example
    echo e configure sua GEMINI_API_KEY
    echo.
    pause
    exit /b 1
)

REM Verifica se as dependências estão instaladas
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo [INFO] Instalando dependencias...
    python -m pip install -r requirements.txt
    echo.
)

REM Inicia a API
echo [INFO] Iniciando TaleSeed API...
echo.
python main.py

pause
