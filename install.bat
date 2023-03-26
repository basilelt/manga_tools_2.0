::::::::::::::::::::::::::::::::::::::::::::
:: Automatically check & get admin rights V2
::::::::::::::::::::::::::::::::::::::::::::
@echo off
CLS
ECHO.
ECHO =============================
ECHO Running Admin shell
ECHO =============================

:init
setlocal DisableDelayedExpansion
set "batchPath=%~0"
for %%k in (%0) do set batchName=%%~nk
set "vbsGetPrivileges=%temp%\OEgetPriv_%batchName%.vbs"
setlocal EnableDelayedExpansion

:checkPrivileges
NET FILE 1>NUL 2>NUL
if '%errorlevel%' == '0' ( goto gotPrivileges ) else ( goto getPrivileges )

:getPrivileges
if '%1'=='ELEV' (echo ELEV & shift /1 & goto gotPrivileges)
ECHO.
ECHO **************************************
ECHO Invoking UAC for Privilege Escalation
ECHO **************************************

ECHO Set UAC = CreateObject^("Shell.Application"^) > "%vbsGetPrivileges%"
ECHO args = "ELEV " >> "%vbsGetPrivileges%"
ECHO For Each strArg in WScript.Arguments >> "%vbsGetPrivileges%"
ECHO args = args ^& strArg ^& " "  >> "%vbsGetPrivileges%"
ECHO Next >> "%vbsGetPrivileges%"
ECHO UAC.ShellExecute "!batchPath!", args, "", "runas", 1 >> "%vbsGetPrivileges%"
"%SystemRoot%\System32\WScript.exe" "%vbsGetPrivileges%" %*
exit /B

:gotPrivileges
setlocal & pushd .
cd /d %~dp0
if '%1'=='ELEV' (del "%vbsGetPrivileges%" 1>nul 2>nul  &  shift /1)

::::::::::::::::::::::::::::
::START
::::::::::::::::::::::::::::

cd /D "%~dp0"

mkdir download

curl -o python.exe https://www.python.org/downloads/release/python-3112/
python.exe /quit AppendPath=1

curl -o 7z.exe https://www.7-zip.org/a/7z2201-x64.exe
7z.exe /S
setx path "%path%;C:\Program Files\7-Zip"

powershell -Command "Invoke-WebRequest -Uri ((Invoke-WebRequest -Uri https://api.github.com/repos/git-for-windows/git/releases/latest | ConvertFrom-Json).assets | Where-Object { $_.name -like 'Git*64-bit.exe' } | Select-Object -First 1).browser_download_url -OutFile git.exe"
git.exe /VERYSILENT /NORESTART

python -m pip install --upgrade pip
python -m pip freeze | %{$_.split('==')[0]} | %{pip install --upgrade $_}
python -m pip install requirements.txt

git clone https://github.com/ArdaxHz/mangadex_bulk_uploader
git clone https://github.com/MechTechnology/SmartStitch

powershell -Command "Invoke-WebRequest -Uri ((Invoke-WebRequest -Uri https://api.github.com/repos/shssoichiro/oxipng/releases/latest | ConvertFrom-Json).assets | Where-Object { $_.name -like 'oxipng*windows*.zip' } | Select-Object -First 1).browser_download_url -OutFile oxipng.zip"
mkdir oxipng
tar -xf .\oxipng.zip -C oxipng
del .\oxipng.zip

powershell -Command "Invoke-WebRequest -Uri ((Invoke-WebRequest -Uri https://api.github.com/repos/nihui/waifu2x-ncnn-vulkan/releases/latest | ConvertFrom-Json).assets | Where-Object { $_.name -like 'waifu2x-ncnn-vulkan-*-windows.zip' } | Select-Object -First 1).browser_download_url -OutFile waifu2x.zip" 
tar -xf .\waifu2x.zip
del .\waifu2x.zip
powershell -Command "Get-ChildItem -Directory -Filter 'waifu2x*' | Rename-Item -NewName 'waifu2x' -Force"

powershell -Command "Invoke-WebRequest -Uri ((Invoke-WebRequest -Uri https://api.github.com/repos/dazedcat19/FMD2/releases/latest | ConvertFrom-Json).assets | Where-Object { $_.name -like 'fmd*-win64.7z' } | Select-Object -First 1).browser_download_url -OutFile fmd.7z"
7z x .\fmd.7z -ofmd
del .\fmd.7z

curl -o image_magick.zip https://imagemagick.org/archive/binaries/ImageMagick-7.1.1-5-portable-Q16-HDRI-x64.zip
mkdir image_magick
tar -xf .\image_magick.zip -C image_magick
del .\image_magick.zip
