@echo off
cd /d "C:\deepseek  harness\go-website"
C:\Python\python.exe -m pip install -r requirements.txt
C:\Python\python.exe app.py
pause
