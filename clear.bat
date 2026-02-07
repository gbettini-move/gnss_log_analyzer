@echo off
REM Script per cancellare cartella x, .venv, .lock, __pycache__

echo ----------
echo PULIZIA
echo avviata

REM Rimuovi cartelle di build precedenti
REM if exist dist rmdir /s /q dist

if exist .venv rmdir /s /q .venv
for /d /r . %%d in (__pycache__) do rmdir /s /q "%%d" 2>nul
if exist *.lock del /q *.lock

echo completata
echo ----------