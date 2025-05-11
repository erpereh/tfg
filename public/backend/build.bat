@echo off

REM Activar el entorno virtual
call venv\Scripts\activate.bat

REM Actualizar pip
python -m pip install --upgrade pip

REM Instalar Reflex y dependencias
REM pip install reflex
REM pip install -r requirements.txt

REM Borrar carpeta 'public' si existe
rmdir /S /Q public

REM Inicializar y exportar Reflex
reflex export

REM Crear carpeta 'public'
mkdir public

REM Extraer los archivos ZIP
powershell -Command "Expand-Archive -Force 'backend.zip' 'public\backend'"
powershell -Command "Expand-Archive -Force 'frontend.zip' 'public\frontend'"

REM Borrar archivos ZIP
del backend.zip
del frontend.zip

REM Desplegar
reflex deploy
