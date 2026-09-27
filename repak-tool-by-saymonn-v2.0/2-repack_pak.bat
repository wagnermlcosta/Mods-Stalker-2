@echo off
set "input_folder=.\2-extracted-pak-files"
set "output_folder=.\3-repacked-pak-files"
setlocal enabledelayedexpansion

if not exist "%input_folder%" (
    echo The folder "%input_folder%" does not exist. Make sure it contains extracted folders.
    pause
    exit /b
)

if not exist "%output_folder%" (
    echo Creating output folder: "%output_folder%"
    mkdir "%output_folder%"
)

echo Searching for top-level folders in "%input_folder%"...
set "folder_list="
set "index=0"
for /d %%f in ("%input_folder%\*") do (
    set /a index+=1
    echo !index!: %%~nxf
    set "folder_!index!=%%f"
)

if "%index%"=="0" (
    echo No folders found in "%input_folder%".
    pause
    exit /b
)

:choose_folder
set /p "choice=Enter the number of the folder to process: "
if "!folder_%choice%!"=="" (
    echo Invalid selection: %choice%. Try again.
    goto choose_folder
)

set "selected_folder=!folder_%choice%!"

if not exist "!selected_folder!" (
    echo The selected folder "!selected_folder!" does not exist. Exiting.
    pause
    exit /b
)

set "subfolder_count=0"
for /d %%d in ("!selected_folder!\*") do (
    set /a subfolder_count+=1
    set "subfolder_!subfolder_count!=%%d"
)

if "%subfolder_count%"=="0" (
    echo No valid subfolders found in "!selected_folder!". Exiting.
    pause
    exit /b
)

for %%a in ("!selected_folder!") do set "folder_name=%%~na"
set "output_file=%output_folder%\%folder_name%.pak"

rem Create relative paths for display purposes
set "selected_relative=!selected_folder:%CD%=.!"
set "output_relative=!output_file:%CD%=.!"

echo Processing all subfolders in: "!selected_relative!"
repak.exe pack --version V11 "!selected_folder!" "!output_file!" || (
    echo Error: Failed to repack folder "!selected_relative!".
    pause
    exit /b
)

pause
