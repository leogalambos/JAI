REM SPDX-License-Identifier: BSD-4-Clause
REM Copyright (c) 2026 Leo Galambos and the Egothor team
REM https://www.egothor.org
@echo off
setlocal
py -3 "%~dp0.ai\setup\uninstaller.py" %*
if errorlevel 1 python "%~dp0.ai\setup\uninstaller.py" %*
