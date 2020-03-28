@echo off
echo Running Remote Desktop Monitor Task
set DATABASE="--------Enter Your DataBase Path-------"
cd "C:\Program Files\RemoteDesktopMonitor"
start RemoteDesktopMonitor.exe --database %DATABASE%