@echo off
cd /d "C:\deepseek  harness\weiqi\go-website"

if not exist "cloudflared.exe" (
    echo Downloading cloudflared...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe' -OutFile 'cloudflared.exe'"
)

echo Starting tunnel to http://127.0.0.1:8080
echo Keep this window open. Your public URL will be shown below.
cloudflared.exe tunnel --url http://127.0.0.1:8080
pause
