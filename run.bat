@echo off
title TeamBoard · Verisure Analisis

echo.
echo  =========================================
echo   TeamBoard - Verisure Analisis
echo  =========================================
echo.
echo  Iniciando backend  (puerto 8001)...
echo  Iniciando frontend (puerto 5173)...
echo.
echo  Acceso:
echo    App:     http://localhost:5173
echo    API:     http://localhost:8001
echo    API Doc: http://localhost:8001/docs
echo.
echo  Cierra esta ventana para detener todo.
echo  =========================================
echo.

:: Backend
start "TeamBoard Backend" cmd /k "cd /d %~dp0backend && ..\venv\Scripts\activate && uvicorn main:app --reload --port 8001"

:: Esperar 3 segundos a que el backend arranque
timeout /t 3 /nobreak > nul

:: Frontend
start "TeamBoard Frontend" cmd /k "cd /d %~dp0frontend && set PATH=C:\Users\pablo.magana\AppData\Local\Programs\nodejs\node-v24.14.1-win-x64;%PATH% && npm run dev"

:: Esperar 4 segundos y abrir el navegador
timeout /t 4 /nobreak > nul
start http://localhost:5173
