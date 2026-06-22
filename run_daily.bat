@echo off
rem Bao cao desk hang ngay - chay boi Task Scheduler 6h30 sang T2-T6
rem Dung Claude CLI (goi thue bao, khong can API key). Log: data\local_run.log

cd /d "F:\Hai BUi\Mini_Investment_Desk_Agent_System_v1"
set PATH=%USERPROFILE%\.local\bin;%PATH%
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

set PY=C:\Users\ADMIN\AppData\Local\Programs\Python\Python311\python.exe

echo ==================== %date% %time% ==================== >> data\local_run.log
"%PY%" -m pipeline.run_pipeline --cli >> data\local_run.log 2>&1
if errorlevel 1 (
  echo PIPELINE FAILED >> data\local_run.log
  exit /b 1
)

git add docs data >> data\local_run.log 2>&1
git commit -m "Daily desk report (local run)" >> data\local_run.log 2>&1
git push >> data\local_run.log 2>&1
echo DONE %date% %time% >> data\local_run.log
