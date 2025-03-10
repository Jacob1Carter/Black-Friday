@echo off
:: Check for administrative privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    :: If running with admin privileges, run the Python script
    python firewall_rule.py
) else (
    :: If not running with admin privileges, request them
    echo Requesting administrative privileges...
    powershell -Command "Start-Process cmd -ArgumentList '/c %~dp0run_with_admin.bat' -Verb RunAs"
)