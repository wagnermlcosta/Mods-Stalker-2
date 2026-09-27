@echo off
set "pak_folder=.\1-input-pak-files"
set "output_folder=%~dp02-extracted-pak-files"
setlocal enabledelayedexpansion

if not exist "%pak_folder%" (
    echo The folder "%pak_folder%" does not exist. Make sure it contains .pak files.
    pause
    exit /b
)

if not exist "%output_folder%" (
    echo Creating output folder: "%output_folder%"
    mkdir "%output_folder%"
)

echo Searching for .pak files in "%pak_folder%"...
set "file_list="
set "index=0"
for /r "%pak_folder%" %%f in (*.pak) do (
    set /a index+=1
    echo !index!: %%f
    set "file_!index!=%%f"
)

if "%index%"=="0" (
    echo No .pak files found in "%pak_folder%".
    pause
    exit /b
)

:choose_files
set /p "choice=Enter the numbers of the files to process (separate with spaces): "
set "valid_choice=true"
for %%i in (%choice%) do (
    if "!file_%%i!"=="" (
        echo Invalid selection: %%i. Try again.
        set "valid_choice=false"
    )
)
if "%valid_choice%"=="false" (
    goto choose_files
)

for %%i in (%choice%) do (
    set "selected_file=!file_%%i!"
    for %%a in ("!selected_file!") do set "file_name=%%~na"
    set "file_output_folder=%output_folder%\!file_name!"
    if not exist "!file_output_folder!" (
        echo Creating folder: "!file_output_folder!"
        mkdir "!file_output_folder!"
    )
    echo Processing file: "!selected_file!"
    repak --aes-key 0x33A604DF49A07FFD4A4C919962161F5C35A134D37EFA98DB37A34F6450D7D386 unpack "!selected_file!" --output "!file_output_folder!"
)

echo Output saved in: "%output_folder%"
pause