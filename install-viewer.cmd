@echo off
REM SPDX-License-Identifier: BSD-4-Clause
REM Separate optional viewer installer; no Python or main JAI installation is invoked.
powershell.exe -NoProfile -File "%~dp0apps\fabric-explorer\packaging\install-from-source.ps1" %*
exit /b %errorlevel%
