@echo off
cd /d "%~dp0"
if defined SPT5_TEE goto :spt_begin
if "%~1"=="" goto :spt_begin
set "SPT5_TEE=1"
if not exist "%~dp0StalkerPakToolFiles\logs" mkdir "%~dp0StalkerPakToolFiles\logs"
if exist "%~dp0logs\*.log" move /y "%~dp0logs\*.log" "%~dp0StalkerPakToolFiles\logs\" >nul
if exist "%~dp0StalkerPakToolFiles\last_run.log" move /y "%~dp0StalkerPakToolFiles\last_run.log" "%~dp0StalkerPakToolFiles\logs\last_run.log" >nul
if exist "%~dp0StalkerPakToolFiles\logs\_error" del /q "%~dp0StalkerPakToolFiles\logs\_error"
set "SPT5_LOG=%~dp0StalkerPakToolFiles\logs\last_run.log"
"%ComSpec%" /d /s /c ""%~f0" %*" 2>&1 | powershell -NoProfile -Command "$input | Tee-Object -FilePath $env:SPT5_LOG"
if exist "%~dp0StalkerPakToolFiles\logs\_error" powershell -NoProfile -Command "$dir=Split-Path -Parent $env:SPT5_LOG; Copy-Item -LiteralPath $env:SPT5_LOG -Destination (Join-Path $dir ('error_' + (Get-Date -Format 'yyyy-MM-dd_HH-mm-ss') + '.log')) -Force; Remove-Item -LiteralPath (Join-Path $dir '_error') -Force"
exit /b
:spt_begin
setlocal EnableDelayedExpansion

set "VERSION=5.3"
:: Set AES key - comment out or leave empty if not needed
:: NOTE: Using an AES key does not harm this script even if the game doesn't use one.
:: --------------------------------------------------------------------------------
set "AES_KEY=0x33A604DF49A07FFD4A4C919962161F5C35A134D37EFA98DB37A34F6450D7D386"

:: Set your game directory here if you don't want to use the INI file
:: Example: "CUSTOM_GAME_DIR=C:\Program Files (x86)\Steam\steamapps\common\S.T.A.L.K.E.R. 2 Heart of Chornobyl"
:: --------------------------------------------------------------------------------
set "CUSTOM_GAME_DIR="

:: Pak / IoStore versions - Stalker 2 is UE 5.5, pak V11. Change these if using another game.
:: --------------------------------------------------------------------------------
set "PAK_VERSION=V11"
set "UE_VERSION=UE5_5"
set "TOC_VERSION=ReplaceIoChunkHashWithIoHash"
set "HEADER_VERSION=SoftPackageReferences"

set "REPAK_PATH=%~dp0StalkerPakToolFiles\repak.exe"
set "RETOC_PATH=%~dp0StalkerPakToolFiles\retoc.exe"
set "BIN2CFG_PATH=%~dp0StalkerPakToolFiles\bin2cfg\bin2cfg.exe"
set "GAME_PAKS="
if not "!CUSTOM_GAME_DIR!"=="" set "GAME_DIR=!CUSTOM_GAME_DIR!"
set "SPT5_ROOT=%~dp0"
set "TOOL_TEMP=%~dp0temp_spt_files"
if exist "%~dp0temp" (
    echo Removing leftover temp folder from a previous run...
    rmdir /s /q "%~dp0temp" 2>nul
)
if exist "!TOOL_TEMP!" (
    echo Removing leftover temp folder from a previous run...
    call :clean_tool_temp
)

if not exist "!REPAK_PATH!" (
    echo Error: repak.exe not found in StalkerPakToolFiles
    call :mark_run_error
    pause
    exit /b 1
)
if not exist "!RETOC_PATH!" (
    echo Error: retoc.exe not found in StalkerPakToolFiles
    call :mark_run_error
    pause
    exit /b 1
)
if not exist "!BIN2CFG_PATH!" (
    echo Warning: bin2cfg.exe not found in StalkerPakToolFiles\bin2cfg
    echo .cfg.bin files will not be converted to readable .cfg
    echo.
)

:: Drag-drop. Do not wrap this in if (...).
if "%~1"=="" goto :interactive_banner

:drag_init
set "HAS_ERROR=0"
set "SPT5_PROMPT=1"
set "SEEN_IOSTORE=;"
set "SPT5_SKIP_IOSTORE="
set "SPT5_NEED_GAME=0"
set "SPT5_GAME_TRIED=0"
set "CONFIG_FILE=%~dp0stalker2_location.ini"

:drag_loop
if "%~1"=="" goto :drag_done
set "input_path=%~f1"
set "input_ext=%~x1"
set "input_base=%~dpn1"
if /i "!input_ext!"==".utoc" goto :drag_unpack
if /i "!input_ext!"==".ucas" goto :drag_unpack
if /i "!input_ext!"==".pak" goto :drag_unpack
dir /a:d "!input_path!" >nul 2>&1
if errorlevel 1 goto :drag_invalid
set "SPT5_NEED_GAME=1"
set "SPT5_AFTER_GAME=pack"
if not "!GAME_PAKS!"=="" if exist "!GAME_PAKS!\global.utoc" goto :do_pack
if "!SPT5_GAME_TRIED!"=="1" goto :do_pack
goto :load_game_dir
:do_pack
echo Packing: %~nx1
call :pack_folder "!input_path!"
if errorlevel 1 set "HAS_ERROR=1"
goto :drag_shift
:drag_unpack
if /i not "!input_ext!"==".pak" goto :cooked_prep
if exist "!input_base!.utoc" goto :cooked_prep
if exist "!input_base!" rmdir /s /q "!input_base!"
set "PAK_OK=0"
if not "!AES_KEY!"=="" (
    "!REPAK_PATH!" -a !AES_KEY! unpack "!input_path!" -o "!input_base!" -f >nul 2>&1
    if !errorlevel! equ 0 set "PAK_OK=1"
)
if "!PAK_OK!"=="0" (
    "!REPAK_PATH!" unpack "!input_path!" -o "!input_base!" -f >nul 2>&1
    if !errorlevel! equ 0 set "PAK_OK=1"
)
if "!PAK_OK!"=="0" (
    echo Error unpacking file: !input_path!
    set "HAS_ERROR=1"
    goto :drag_shift
)
call :convert_cfg_bin "!input_base!"
if errorlevel 1 set "HAS_ERROR=1"
goto :drag_shift
:cooked_prep
set "SPT5_NEED_GAME=1"
set "SPT5_AFTER_GAME=unpack"
if "!SPT5_SKIP_IOSTORE!"=="1" goto :skip_cooked_unpack
if not "!GAME_PAKS!"=="" if exist "!GAME_PAKS!\global.utoc" goto :iostore_go
goto :load_game_dir
:load_game_dir
set "SPT5_GAME_TRIED=1"
if "!CUSTOM_GAME_DIR!"=="" goto :load_from_drop
set "GAME_DIR=!CUSTOM_GAME_DIR!"
set "SPT5_WALK_RET=load_from_drop"
goto :walk_to_paks
:load_from_drop
if not "!GAME_PAKS!"=="" goto :game_dir_ready
set "GAME_DIR=%~dp1"
set "SPT5_WALK_RET=load_from_ini"
goto :walk_to_paks
:load_from_ini
if not "!GAME_PAKS!"=="" goto :game_dir_ready
if not exist "!CONFIG_FILE!" goto :game_dir_ready
for /f "usebackq tokens=1* delims==" %%a in ("!CONFIG_FILE!") do (
    if /i "%%a"=="gamedir" set "GAME_DIR=%%b"
)
set "SPT5_WALK_RET=game_dir_ready"
goto :walk_to_paks
:walk_to_paks
if "!GAME_DIR!"=="" goto :walk_to_paks_done
set "GAME_DIR=!GAME_DIR:"=!"
if "!GAME_DIR:~-1!"=="\" set "GAME_DIR=!GAME_DIR:~0,-1!"
set "SPT5_TRY=!GAME_DIR!"
set "SPT5_I=0"
:walk_to_paks_loop
if exist "!SPT5_TRY!\Stalker2\Content\Paks\global.utoc" goto :walk_to_paks_ok
set "SPT5_PARENT="
for %%P in ("!SPT5_TRY!") do set "SPT5_PARENT=%%~dpP"
if "!SPT5_PARENT!"=="" goto :walk_to_paks_done
if "!SPT5_PARENT:~-1!"=="\" set "SPT5_PARENT=!SPT5_PARENT:~0,-1!"
if /i "!SPT5_PARENT!"=="!SPT5_TRY!" goto :walk_to_paks_done
set "SPT5_TRY=!SPT5_PARENT!"
set /a "SPT5_I+=1"
if !SPT5_I! geq 12 goto :walk_to_paks_done
goto :walk_to_paks_loop
:walk_to_paks_ok
set "GAME_DIR=!SPT5_TRY!"
set "GAME_PAKS=!GAME_DIR!\Stalker2\Content\Paks"
:walk_to_paks_done
goto :!SPT5_WALK_RET!
:game_dir_ready
if /i "!SPT5_AFTER_GAME!"=="pack" goto :do_pack
if not "!GAME_PAKS!"=="" if exist "!GAME_PAKS!\global.utoc" goto :iostore_go
:ask_game_dir
echo.
echo This mod has cooked .utoc/.ucas files.
echo Unpacking those needs the game's global.utoc from your Stalker 2 install,
echo not from the mod itself.
echo.
echo Leave blank to skip cooked files and only unpack the .pak if there is one.
echo.
echo Example Steam Location:
echo C:\Program Files (x86^)\Steam\steamapps\common\S.T.A.L.K.E.R. 2 Heart of Chornobyl
echo Example Gamepass Location:
echo C:\XboxGames\S.T.A.L.K.E.R. 2- Heart of Chornobyl (Windows^)\Content
echo.
echo Enter the Stalker 2 folder location:
set "GAME_DIR="
set /p "GAME_DIR="
if "!GAME_DIR!"=="" goto :skip_cooked_unpack
set "GAME_DIR=!GAME_DIR:"=!"
if "!GAME_DIR:~-1!"=="\" set "GAME_DIR=!GAME_DIR:~0,-1!"
set "SPT5_TRY=!GAME_DIR!"
set "SPT5_I=0"
:ask_walk
if exist "!SPT5_TRY!\Stalker2\Content\Paks\global.utoc" goto :ask_walk_ok
set "SPT5_PARENT="
for %%P in ("!SPT5_TRY!") do set "SPT5_PARENT=%%~dpP"
if "!SPT5_PARENT!"=="" goto :ask_walk_fail
if "!SPT5_PARENT:~-1!"=="\" set "SPT5_PARENT=!SPT5_PARENT:~0,-1!"
if /i "!SPT5_PARENT!"=="!SPT5_TRY!" goto :ask_walk_fail
set "SPT5_TRY=!SPT5_PARENT!"
set /a "SPT5_I+=1"
if !SPT5_I! geq 12 goto :ask_walk_fail
goto :ask_walk
:ask_walk_fail
echo.
echo Could not find Stalker2\Content\Paks\global.utoc in: !GAME_DIR!
goto :ask_game_dir
:ask_walk_ok
set "GAME_DIR=!SPT5_TRY!"
goto :game_dir_ok
:game_dir_ok
set "GAME_PAKS=!GAME_DIR!\Stalker2\Content\Paks"
echo gamedir=!GAME_DIR!>"%~dp0stalker2_location.ini"
echo Using game folder: !GAME_DIR!
:iostore_go
call :queue_set "!input_base!" "%~n1"
goto :drag_shift
:skip_cooked_unpack
set "SPT5_SKIP_IOSTORE=1"
echo Skipping cooked .utoc unpack. No game folder set.
if not exist "!input_base!.pak" (
    echo No .pak next to it to unpack either.
    set "HAS_ERROR=1"
    goto :drag_shift
)
if exist "!input_base!" rmdir /s /q "!input_base!"
set "SPT5_PAK_ONLY=1"
call :unpack_pak_into "!input_base!.pak" "!input_base!"
set "SPT5_PAK_ONLY="
if errorlevel 1 set "HAS_ERROR=1"
if not exist "!input_base!" goto :drag_shift
call :convert_cfg_bin "!input_base!"
if errorlevel 1 set "HAS_ERROR=1"
dir /s /b /a-d "!input_base!\*.*" >nul 2>&1 && echo. && echo Successfully unpacked to: !input_base!
goto :drag_shift
:drag_invalid
echo Invalid file or folder: !input_path!
set "HAS_ERROR=1"
:drag_shift
shift /1
goto :drag_loop
:drag_done
if "!SPT5_NEED_GAME!"=="0" goto :drag_exit
call :clean_tool_temp
:drag_exit
if !HAS_ERROR! equ 1 call :mark_run_error
if !HAS_ERROR! equ 1 pause
exit /b !HAS_ERROR!

:interactive_banner

echo StalkerPakTool v%VERSION% by v3fish - MIT License
echo repak by Truman Kilen (github.com/trumank/repak) - MIT and Apache-2.0 licensed
echo retoc by Truman Kilen (github.com/trumank/retoc) - MIT licensed
echo bin2cfg based on joric (github.com/joric/stalker) - custom build, Unlicense
echo.
echo StalkerPakToolFiles\repak.exe    - classic .pak (cfg, ini, GameLite)
echo StalkerPakToolFiles\retoc.exe    - IoStore .utoc/.ucas (cooked assets)
echo StalkerPakToolFiles\bin2cfg\bin2cfg.exe  - convert .cfg.bin to readable .cfg
echo.
echo Drag and drop:
echo   .pak / .utoc / .ucas  unpack the whole set, then convert .cfg.bin to .cfg
echo   folder of .cfg/.ini   pack with repak
echo   folder of .uasset     pack with retoc to .pak + .utoc + .ucas
echo   folder with both      loose files go in the .pak, cooked assets go in .utoc/.ucas
echo.
echo To check .pak / cfg conflicts in ~mods, type 'y' or 'yes'.
echo.
:ask_conflicts
set "CHECK_CONFLICTS="
set /p "CHECK_CONFLICTS=Check for pak/cfg conflicts? (y/n): "
if /i "!CHECK_CONFLICTS!"=="y" goto :start_conflict_check
if /i "!CHECK_CONFLICTS!"=="yes" goto :start_conflict_check
if /i "!CHECK_CONFLICTS!"=="n" exit /b
if /i "!CHECK_CONFLICTS!"=="no" exit /b
echo Please type y or n.
goto :ask_conflicts

:start_conflict_check
set "SPT5_PROMPT=0"
set "SCRIPT_DIR=%~dp0"
set "CONFIG_FILE=%SCRIPT_DIR%stalker2_location.ini"
set "TEMP_DIR=!TOOL_TEMP!\conflicts"
set "FILE_LIST=!TEMP_DIR!\filelist.txt"

:check_game_dir
if "!CUSTOM_GAME_DIR!"=="" goto :check_ini
set "GAME_DIR=!CUSTOM_GAME_DIR!"
goto :verify_path
echo Invalid path in CUSTOM_GAME_DIR: !CUSTOM_GAME_DIR!
echo Please check the path in the batch file.
if exist "!CONFIG_FILE!" (
    echo.
    echo Found existing INI configuration.
    call :prompt_con "Use INI settings instead? (y/n): " USE_INI
    if /i "!USE_INI!"=="y" goto :load_ini
)
goto :show_examples

:check_ini
if exist "!CONFIG_FILE!" goto :load_ini
goto :verify_path

:load_ini
for /f "tokens=1* delims==" %%a in ('type "!CONFIG_FILE!"') do (
    if /i "%%a"=="gamedir" set "GAME_DIR=%%b"
)
goto :verify_path

:verify_path
if "!GAME_DIR!"=="" goto :show_examples
set "GAME_DIR=!GAME_DIR:"=!"
if "!GAME_DIR:~-1!"=="\" set "GAME_DIR=!GAME_DIR:~0,-1!"
set "SPT5_TRY=!GAME_DIR!"
set "SPT5_I=0"
:vp_walk
if exist "!SPT5_TRY!\Stalker2\Content\Paks" set "GAME_DIR=!SPT5_TRY!"
if exist "!SPT5_TRY!\Stalker2\Content\Paks" goto :vp_walk_done
set "SPT5_PARENT="
for %%P in ("!SPT5_TRY!") do set "SPT5_PARENT=%%~dpP"
if "!SPT5_PARENT!"=="" goto :vp_walk_done
if "!SPT5_PARENT:~-1!"=="\" set "SPT5_PARENT=!SPT5_PARENT:~0,-1!"
if /i "!SPT5_PARENT!"=="!SPT5_TRY!" goto :vp_walk_done
set "SPT5_TRY=!SPT5_PARENT!"
set /a "SPT5_I+=1"
if !SPT5_I! geq 12 goto :vp_walk_done
goto :vp_walk
:vp_walk_done
if not exist "!GAME_DIR!\Stalker2\Content\Paks" goto :show_examples
if "!SPT5_SAVE_INI!"=="1" echo gamedir=!GAME_DIR!>"!CONFIG_FILE!"
set "SPT5_SAVE_INI="
set "GAME_PAKS=!GAME_DIR!\Stalker2\Content\Paks"
echo Using game folder: !GAME_DIR!
goto :continue_script

:show_examples
if not "!GAME_DIR!"=="" (
    echo Invalid Stalker 2 directory: !GAME_DIR!
    echo.
)
echo Example Steam Location:
echo C:\Program Files (x86^)\Steam\steamapps\common\S.T.A.L.K.E.R. 2 Heart of Chornobyl
echo Example Gamepass Location:
echo C:\XboxGames\S.T.A.L.K.E.R. 2- Heart of Chornobyl (Windows^)\Content
echo.
echo Enter the Stalker 2 folder location:
set /p "GAME_DIR="
set "SPT5_SAVE_INI=1"
goto :verify_path

:continue_script
set "MODS_DIR=!GAME_DIR!\Stalker2\Content\Paks\~mods"

if not exist "!MODS_DIR!" (
    echo ~mods folder not found. Please create !MODS_DIR! and add your mods, then run this script again.
    pause
    exit /b
)

set "MOD_COUNT=0"
for %%f in ("!MODS_DIR!\*.pak") do set /a "MOD_COUNT+=1"
for /d %%d in ("!MODS_DIR!\*") do (
    for %%f in ("%%d\*.pak") do set /a "MOD_COUNT+=1"
)

if !MOD_COUNT! equ 0 (
    echo No mods detected in !MODS_DIR!
    echo Add your mods and try again.
    pause
    exit /b
)

call :clean_tool_temp
mkdir "!TEMP_DIR!" 2>nul

echo Processing .pak files for cfg/ini conflicts...
echo.

type nul > "!FILE_LIST!"

call :scan_mods_dir "!MODS_DIR!" ""

echo.
echo Checking for conflicts...
echo.

set "PREV_FILE="
set "CONFLICT_COUNT=0"
set "CURRENT_FILE="
set "MODS_IN_CONFLICT="
set "CONFLICTING_FILES="

for /f "tokens=1,* delims=|" %%a in ('sort "!FILE_LIST!"') do (
    if /i not "%%a"=="!CURRENT_FILE!" (
        if defined MODS_IN_CONFLICT (
            echo Conflict found: !CURRENT_FILE!
            for %%m in ("!MODS_IN_CONFLICT:;=" "!") do (
                if not "%%~m"=="" echo   - In mod: %%~m
            )
            echo.
            if defined CONFLICTING_FILES (
                set "CONFLICTING_FILES=!CONFLICTING_FILES!, !CURRENT_FILE!"
            ) else (
                set "CONFLICTING_FILES=!CURRENT_FILE!"
            )
            set "MODS_IN_CONFLICT="
        )
        set "CURRENT_FILE=%%a"
    )

    if /i "%%a"=="!PREV_FILE!" if /i not "%%b"=="!PREV_PAK!" (
        if not defined MODS_IN_CONFLICT (
            set "MODS_IN_CONFLICT=!PREV_PAK!"
            set /a "CONFLICT_COUNT+=1"
        )
        set "MODS_IN_CONFLICT=!MODS_IN_CONFLICT!;%%b"
        set /a "CONFLICT_COUNT+=1"
    )
    set "PREV_FILE=%%a"
    set "PREV_PAK=%%b"
)

if defined MODS_IN_CONFLICT (
    echo Conflict found: !CURRENT_FILE!
    for %%m in ("!MODS_IN_CONFLICT:;=" "!") do (
        if not "%%~m"=="" echo   - In mod: %%~m
    )
    echo.
    if defined CONFLICTING_FILES (
        set "CONFLICTING_FILES=!CONFLICTING_FILES!, !CURRENT_FILE!"
    ) else (
        set "CONFLICTING_FILES=!CURRENT_FILE!"
    )
)

echo Conflicting Files: !CONFLICTING_FILES!
echo Total mod conflicts: !CONFLICT_COUNT!
if !CONFLICT_COUNT! equ 0 echo Good hunting, Stalker.

if exist "!TEMP_DIR!" rmdir /s /q "!TEMP_DIR!" 2>nul
call :clean_tool_temp

pause
exit /b 0

:scan_mods_dir
set "SCAN_DIR=%~1"
set "SCAN_PREFIX=%~2"

for %%f in ("!SCAN_DIR!\*.pak") do (
    echo [%%~nxf]
    if not "!AES_KEY!"=="" (
        "!REPAK_PATH!" -a !AES_KEY! unpack "%%f" -o "!TEMP_DIR!\%%~nf" >nul 2>&1
        if !errorlevel! neq 0 (
            "!REPAK_PATH!" unpack "%%f" -o "!TEMP_DIR!\%%~nf" >nul 2>&1
        )
    ) else (
        "!REPAK_PATH!" unpack "%%f" -o "!TEMP_DIR!\%%~nf" >nul 2>&1
    )
    for /f "delims=" %%i in ('dir /s /b /a-d "!TEMP_DIR!\%%~nf\*.*" 2^>nul') do (
        set "CF_OK=0"
        if /i "%%~xi"==".cfg" set "CF_OK=1"
        if /i "%%~xi"==".ini" set "CF_OK=1"
        set "CF_NAME=%%~nxi"
        if /i "!CF_NAME:~-8!"==".cfg.bin" set "CF_OK=1"
        if "!CF_OK!"=="1" if "!SCAN_PREFIX!"=="" (
            findstr /i /l /x /c:"%%~nxi|%%~nxf" "!FILE_LIST!" >nul
            if !errorlevel! neq 0 echo %%~nxi^|%%~nxf>> "!FILE_LIST!"
        )
        if "!CF_OK!"=="1" if not "!SCAN_PREFIX!"=="" (
            findstr /i /l /x /c:"%%~nxi|!SCAN_PREFIX!\%%~nxf" "!FILE_LIST!" >nul
            if !errorlevel! neq 0 echo %%~nxi^|!SCAN_PREFIX!\%%~nxf>> "!FILE_LIST!"
        )
    )
)

if "!SCAN_PREFIX!"=="" (
    for /d %%d in ("!SCAN_DIR!\*") do (
        call :scan_mods_dir "%%d" "%%~nxd"
    )
)
goto :eof

:queue_set
set "SET_BASE=%~1"
set "SET_LABEL=%~2"
set "SET_KEY=!SET_BASE:\=_!"
set "SET_KEY=!SET_KEY::=_!"
set "SET_KEY=!SET_KEY: =_!"
echo ;!SEEN_IOSTORE!; | findstr /i /l /c:";!SET_KEY!;" >nul
if !errorlevel! equ 0 (
    echo Skipping extra file from the same set: !SET_LABEL!
    exit /b 0
)
set "SEEN_IOSTORE=!SEEN_IOSTORE!!SET_KEY!;"

set "SET_PAK=!SET_BASE!.pak"
set "SET_UTOC=!SET_BASE!.utoc"
if not exist "!SET_PAK!" if exist "!GAME_PAKS!\%~n1.pak" set "SET_PAK=!GAME_PAKS!\%~n1.pak"
if not exist "!SET_UTOC!" if exist "!GAME_PAKS!\%~n1.utoc" set "SET_UTOC=!GAME_PAKS!\%~n1.utoc"

if not exist "!SET_PAK!" if not exist "!SET_UTOC!" (
    echo Error: no .pak or .utoc found for !SET_LABEL!
    set "HAS_ERROR=1"
    exit /b 0
)

echo Unpacking set: !SET_LABEL!
set "IOSTORE_OK=0"
set "IO_ERR=0"
if exist "!SET_UTOC!" call :unpack_iostore "!SET_UTOC!" "!SET_BASE!"
set "IO_ERR=!errorlevel!"
if exist "!SET_UTOC!" if !IO_ERR! equ 0 set "IOSTORE_OK=1"
if exist "!SET_UTOC!" if !IO_ERR! equ 1 set "HAS_ERROR=1"
set "PAK_ERR=0"
if exist "!SET_PAK!" if "!IOSTORE_OK!"=="0" if exist "!SET_BASE!" rmdir /s /q "!SET_BASE!"
if exist "!SET_PAK!" call :unpack_pak_into "!SET_PAK!" "!SET_BASE!"
set "PAK_ERR=!errorlevel!"
if exist "!SET_PAK!" if !PAK_ERR! neq 0 if "!IOSTORE_OK!"=="0" set "HAS_ERROR=1"
if not exist "!SET_BASE!" exit /b 0
call :convert_cfg_bin "!SET_BASE!"
if errorlevel 1 set "HAS_ERROR=1"
if !IO_ERR! equ 1 exit /b 0
dir /s /b /a-d "!SET_BASE!\*.*" >nul 2>&1 && echo. && echo Successfully unpacked to: !SET_BASE!
exit /b 0

:unpack_pak_into
set "PAKFILE=%~1"
set "PAKOUT=%~2"
if not exist "!PAKFILE!" exit /b 1
echo Unpacking pak: %~nx1
if "!SPT5_PAK_ONLY!"=="1" goto :pak_unpack_go
call :confirm_large_file "!PAKFILE!" "%~nx1"
if !errorlevel! neq 0 exit /b 1
:pak_unpack_go
if not exist "!PAKOUT!" mkdir "!PAKOUT!" >nul 2>&1
set "PAK_OK=0"
if not "!AES_KEY!"=="" (
    if "!SPT5_PROMPT!"=="1" (
        "!REPAK_PATH!" -a !AES_KEY! unpack "!PAKFILE!" -o "!PAKOUT!" -f
    ) else (
        "!REPAK_PATH!" -a !AES_KEY! unpack "!PAKFILE!" -o "!PAKOUT!" -f >nul 2>&1
    )
    if !errorlevel! equ 0 set "PAK_OK=1"
)
if "!PAK_OK!"=="0" (
    if "!SPT5_PROMPT!"=="1" (
        "!REPAK_PATH!" unpack "!PAKFILE!" -o "!PAKOUT!" -f
    ) else (
        "!REPAK_PATH!" unpack "!PAKFILE!" -o "!PAKOUT!" -f >nul 2>&1
    )
    if !errorlevel! equ 0 set "PAK_OK=1"
)
if "!PAK_OK!"=="0" (
    echo Error unpacking file: !PAKFILE!
    exit /b 1
)
echo Unpacked pak files into: !PAKOUT!
echo.
exit /b 0

:unpack_iostore
set "UTOC=%~1"
set "OUTDIR=%~2"
set "UTOC_DIR=%~dp1"
set "UTOC_NAME=%~n1"
set "WORK=!TOOL_TEMP!\unpack"
echo Unpacking IoStore: !UTOC_NAME!
if exist "!WORK!" rmdir /s /q "!WORK!"
mkdir "!WORK!\src" >nul 2>&1

copy /y "!UTOC!" "!WORK!\src" >nul

set "UCAS="
if exist "%~dpn1.ucas" set "UCAS=%~dpn1.ucas"
if not defined UCAS if exist "!GAME_PAKS!\%~n1.ucas" set "UCAS=!GAME_PAKS!\%~n1.ucas"
if not defined UCAS (
    echo Error: !UTOC_NAME!.ucas is missing.
    echo Put the matching .ucas next to the .utoc, or leave the .utoc in the game Paks folder.
    echo The .utoc is only an index. The files are in the .ucas.
    rmdir /s /q "!WORK!" 2>nul
    exit /b 1
)

call :confirm_large_file "!UCAS!" "!UTOC_NAME!.ucas"
if !errorlevel! neq 0 (
    rmdir /s /q "!WORK!" 2>nul
    exit /b 1
)

echo Copying !UTOC_NAME!.ucas ... Please wait ...
mklink /H "!WORK!\src\!UTOC_NAME!.ucas" "!UCAS!" >nul 2>&1
if not exist "!WORK!\src\!UTOC_NAME!.ucas" copy /y "!UCAS!" "!WORK!\src" >nul
if not exist "!WORK!\src\!UTOC_NAME!.ucas" (
    echo Error copying !UTOC_NAME!.ucas
    rmdir /s /q "!WORK!" 2>nul
    exit /b 1
)
if exist "%~dpn1.pak" copy /y "%~dpn1.pak" "!WORK!\src" >nul
if exist "!GAME_PAKS!\%~n1.pak" if not exist "!WORK!\src\%~n1.pak" copy /y "!GAME_PAKS!\%~n1.pak" "!WORK!\src" >nul
if exist "!GAME_PAKS!\global.utoc" copy /y "!GAME_PAKS!\global.utoc" "!WORK!\src" >nul
if exist "!GAME_PAKS!\global.ucas" copy /y "!GAME_PAKS!\global.ucas" "!WORK!\src" >nul

if exist "!OUTDIR!" rmdir /s /q "!OUTDIR!"
mkdir "!OUTDIR!" >nul 2>&1

set "UNPACK_OK=0"
if not "!AES_KEY!"=="" call :run_retoc --aes-key !AES_KEY! --override-container-header-version !HEADER_VERSION! --override-toc-version !TOC_VERSION! to-legacy --version !UE_VERSION! --no-shaders --no-script-objects "!WORK!\src" "!OUTDIR!"
if not "!AES_KEY!"=="" if !errorlevel! equ 0 set "UNPACK_OK=1"
if exist "!WORK!\retoc_err.txt" findstr /c:"panicked" "!WORK!\retoc_err.txt" >nul && goto :ui_convert_done
if "!UNPACK_OK!"=="0" call :run_retoc --override-container-header-version !HEADER_VERSION! --override-toc-version !TOC_VERSION! to-legacy --version !UE_VERSION! --no-shaders --no-script-objects "!WORK!\src" "!OUTDIR!"
if "!UNPACK_OK!"=="0" if !errorlevel! equ 0 set "UNPACK_OK=1"
:ui_convert_done
set "EXT0=0"
set "EXT0OK=0"
if exist "!WORK!\retoc_err.txt" findstr /c:"Extracted 0 " "!WORK!\retoc_err.txt" >nul && set "EXT0=1"
if exist "!WORK!\retoc_err.txt" findstr /r /c:"Extracted 0 .0 failed." "!WORK!\retoc_err.txt" >nul && set "EXT0OK=1"
if "!UNPACK_OK!"=="1" if "!EXT0!"=="1" if not "!EXT0OK!"=="1" set "UNPACK_OK=0"
if "!UNPACK_OK!"=="1" goto :ui_done
echo.
echo This mod uses an older IoStore format than current Stalker 2.
echo Extracting with the older unpack method...
echo.
if exist "!OUTDIR!" rmdir /s /q "!OUTDIR!"
mkdir "!OUTDIR!" >nul 2>&1
set "UNPACK_OK=0"
if not "!AES_KEY!"=="" call :run_retoc --aes-key !AES_KEY! unpack "!WORK!\src\!UTOC_NAME!.utoc" "!OUTDIR!"
if not "!AES_KEY!"=="" if !errorlevel! equ 0 set "UNPACK_OK=1"
if "!UNPACK_OK!"=="0" call :run_retoc unpack "!WORK!\src\!UTOC_NAME!.utoc" "!OUTDIR!"
if "!UNPACK_OK!"=="0" if !errorlevel! equ 0 set "UNPACK_OK=1"
dir /s /b /a-d "!OUTDIR!\*.*" >nul 2>&1
if errorlevel 1 set "UNPACK_OK=0"
if "!UNPACK_OK!"=="0" (
    echo Error unpacking IoStore: !UTOC!
    echo Cooked unpack needs global.utoc from your Stalker 2 Paks folder.
    rmdir /s /q "!WORK!" 2>nul
    exit /b 1
)
:ui_done
echo.
echo Successfully unpacked IoStore to: !OUTDIR!
echo.
rmdir /s /q "!WORK!" 2>nul
exit /b 0

:confirm_large_file
set "SIZE_FILE=%~1"
set "SIZE_NAME=%~2"
set "SIZE_NICE="
set "SIZE_BIG=NO"
set "SIZE_SKIPPED=0"
for /f "delims=" %%S in ('powershell -NoProfile -Command "$b=(Get-Item -LiteralPath $env:SIZE_FILE).Length; if ($b -ge 1GB) { '{0:N2} GB' -f ($b/1GB) } elseif ($b -ge 1MB) { '{0:N1} MB' -f ($b/1MB) } else { '{0:N0} KB' -f ($b/1KB) }"') do set "SIZE_NICE=%%S"
for /f "delims=" %%S in ('powershell -NoProfile -Command "if ((Get-Item -LiteralPath $env:SIZE_FILE).Length -ge 2GB) {'YES'} else {'NO'}"') do set "SIZE_BIG=%%S"
echo Size: !SIZE_NAME! = !SIZE_NICE!
if /i not "!SIZE_BIG!"=="YES" exit /b 0
if "!SPT5_ALLOW_LARGE!"=="1" exit /b 0
if "!SPT5_PROMPT!"=="1" (
    echo.
    echo WARNING: !SIZE_NAME! is !SIZE_NICE!
    echo Unpacking this may take a long time and use a lot of disk space.
    call :prompt_con "Continue? (y/n): " SPT5_CONT
    if /i not "!SPT5_CONT!"=="y" if /i not "!SPT5_CONT!"=="yes" (
        echo Skipped.
        set "SIZE_SKIPPED=1"
        exit /b 1
    )
    exit /b 0
)
echo Skipping !SIZE_NAME! ^(!SIZE_NICE!^) during conflict check.
set "SIZE_SKIPPED=1"
exit /b 1

:convert_cfg_bin
set "CONV_DIR=%~1"
if not exist "!BIN2CFG_PATH!" exit /b 0
if not exist "!CONV_DIR!" exit /b 0
dir /s /b /a-d "!CONV_DIR!\*.cfg.bin" >nul 2>&1 || exit /b 0
echo Converting .cfg.bin files...
"!BIN2CFG_PATH!" --quiet "!CONV_DIR!"
if !errorlevel! neq 0 exit /b 1
exit /b 0

:pack_folder
set "PK_IN=%~1"
set "PK_BASE=%~dpn1"
set "PK_HAS_ASSETS=0"
for %%E in (uasset uexp ubulk uptnl umap ufont) do dir /s /b /a-d "!PK_IN!\*.%%E" >nul 2>&1 && set "PK_HAS_ASSETS=1"
dir /s /b /a-d "!PK_IN!\scriptobjects.bin" >nul 2>&1 && set "PK_HAS_ASSETS=1"
if "!PK_HAS_ASSETS!"=="1" goto :pack_split
dir /s /b /a-d "!PK_IN!\*.*" >nul 2>&1
if errorlevel 1 goto :pack_empty
echo Packing pak files...
if "!SPT5_PROMPT!"=="1" (
    "!REPAK_PATH!" pack "!PK_IN!" "!PK_BASE!.pak" --version !PAK_VERSION!
) else (
    "!REPAK_PATH!" pack "!PK_IN!" "!PK_BASE!.pak" --version !PAK_VERSION! >nul 2>&1
)
if !errorlevel! neq 0 (
    echo Error packing loose files into: !PK_BASE!.pak
    exit /b 1
)
echo Packed pak to: !PK_BASE!.pak
exit /b 0
:pack_empty
echo Error: folder is empty: !PK_IN!
exit /b 1
:pack_split
set "PK_WORK=!TOOL_TEMP!\pack"
if exist "!PK_WORK!" rmdir /s /q "!PK_WORK!"
mkdir "!PK_WORK!\assets" >nul 2>&1
mkdir "!PK_WORK!\loose" >nul 2>&1
set "PK_ASSETS=!PK_WORK!\assets"
set "PK_LOOSE=!PK_WORK!\loose"
set "PK_NA="
set "PK_NL="
for /f "tokens=1,2" %%A in ('powershell -NoProfile -Command "$src=(Get-Item -LiteralPath $env:PK_IN).FullName; $assetExt=@('.uasset','.uexp','.ubulk','.uptnl','.umap','.ufont'); $nA=0; $nL=0; Get-ChildItem -LiteralPath $src -Recurse -File | ForEach-Object { $rel=$_.FullName.Substring($src.Length).TrimStart('\'); $isAsset=($assetExt -contains $_.Extension.ToLower()) -or ($_.Name -ieq 'scriptobjects.bin'); if ($isAsset) { $root=$env:PK_ASSETS; $nA++ } else { $root=$env:PK_LOOSE; $nL++ }; $dest=Join-Path $root $rel; $dir=[IO.Path]::GetDirectoryName($dest); if ($dir) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }; Copy-Item -LiteralPath $_.FullName -Destination $dest -Force }; Write-Output (\"$nA $nL\")"') do (
    set "PK_NA=%%A"
    set "PK_NL=%%B"
)
if "!PK_NA!"=="" set "PK_NA=0"
if "!PK_NL!"=="" set "PK_NL=0"

if "!PK_NA!"=="0" if "!PK_NL!"=="0" (
    echo Error: folder is empty: !PK_IN!
    rmdir /s /q "!PK_WORK!" 2>nul
    call :clean_tool_temp
    exit /b 1
)

set "PK_OK=0"
if not "!PK_NA!"=="0" (
    echo Packing IoStore cooked assets...
    call :pack_iostore "!PK_ASSETS!" "!PK_BASE!"
    if !errorlevel! neq 0 (
        rmdir /s /q "!PK_WORK!" 2>nul
        call :clean_tool_temp
        exit /b 1
    )
    set "PK_OK=1"
)
if not "!PK_NL!"=="0" (
    echo Packing pak files...
    if "!SPT5_PROMPT!"=="1" (
        "!REPAK_PATH!" pack "!PK_LOOSE!" "!PK_BASE!.pak" --version !PAK_VERSION!
    ) else (
        "!REPAK_PATH!" pack "!PK_LOOSE!" "!PK_BASE!.pak" --version !PAK_VERSION! >nul 2>&1
    )
    if !errorlevel! neq 0 (
        echo Error packing loose files into: !PK_BASE!.pak
        rmdir /s /q "!PK_WORK!" 2>nul
        call :clean_tool_temp
        exit /b 1
    )
    echo Packed pak to: !PK_BASE!.pak
    set "PK_OK=1"
)
rmdir /s /q "!PK_WORK!" 2>nul
call :clean_tool_temp
if "!PK_OK!"=="1" exit /b 0
exit /b 1

:pack_iostore
set "INDIR=%~1"
if not "%~2"=="" (
    set "OUT_UTOC=%~2.utoc"
) else (
    set "OUT_UTOC=%~dp1%~nx1.utoc"
)
set "WORK=!TOOL_TEMP!\pack_iostore"
if exist "!WORK!" rmdir /s /q "!WORK!"
mkdir "!WORK!\in" >nul 2>&1
xcopy "!INDIR!" "!WORK!\in" /E /I /Y /Q >nul

if not exist "!WORK!\in\scriptobjects.bin" (
    if exist "!GAME_PAKS!\global.utoc" (
        mkdir "!WORK!\gsrc" >nul 2>&1
        mkdir "!WORK!\gout" >nul 2>&1
        copy /y "!GAME_PAKS!\global.utoc" "!WORK!\gsrc" >nul
        copy /y "!GAME_PAKS!\global.ucas" "!WORK!\gsrc" >nul
        if not "!AES_KEY!"=="" (
            "!RETOC_PATH!" --aes-key !AES_KEY! --override-container-header-version !HEADER_VERSION! --override-toc-version !TOC_VERSION! to-legacy --version !UE_VERSION! --no-shaders "!WORK!\gsrc" "!WORK!\gout" >nul 2>&1
        )
        if exist "!WORK!\gout\scriptobjects.bin" copy /y "!WORK!\gout\scriptobjects.bin" "!WORK!\in" >nul
    )
)

set "PK_IO_EC=1"
if not "!SPT5_PROMPT!"=="1" goto :pack_io_quiet
call :run_retoc --override-container-header-version !HEADER_VERSION! --override-toc-version !TOC_VERSION! to-zen --version !UE_VERSION! "!WORK!\in" "!OUT_UTOC!"
set "PK_IO_EC=!errorlevel!"
goto :pack_io_check
:pack_io_quiet
"!RETOC_PATH!" --override-container-header-version !HEADER_VERSION! --override-toc-version !TOC_VERSION! to-zen --version !UE_VERSION! "!WORK!\in" "!OUT_UTOC!" >nul 2>&1
set "PK_IO_EC=!errorlevel!"
:pack_io_check
if !PK_IO_EC! neq 0 (
    echo Error packing IoStore folder: !INDIR!
    rmdir /s /q "!WORK!" 2>nul
    exit /b 1
)
echo Successfully packed to: !OUT_UTOC!
echo   plus matching .ucas and .pak next to it
rmdir /s /q "!WORK!" 2>nul
exit /b 0

:run_retoc
set "RT_LOG=!WORK!\retoc_err.txt"
"!RETOC_PATH!" %* >"!RT_LOG!" 2>&1
set "RT_EC=!errorlevel!"
if "!SPT5_PROMPT!"=="1" call :filter_retoc_log "!RT_LOG!"
exit /b !RT_EC!

:filter_retoc_log
set "RT_LOG=%~1"
if not exist "!RT_LOG!" exit /b 0
powershell -NoProfile -Command "if (-not (Test-Path -LiteralPath $env:RT_LOG)) { exit 0 }; $keep = Get-Content -LiteralPath $env:RT_LOG -ErrorAction SilentlyContinue | Where-Object { $_.Trim() -ne '' -and $_ -notmatch 'Failed to resolve import map' -and $_ -notmatch 'not found in any containers' -and $_ -notmatch 'FIoChunkId' -and $_ -notmatch 'panicked' -and $_ -notmatch 'RUST_BACKTRACE' -and $_ -notmatch 'left == right' -and $_ -notmatch 'thread .main' -and $_ -notmatch ' left:' -and $_ -notmatch ' right:' }; if ($keep) { $keep | ForEach-Object { Write-Host $_ } }"
exit /b 0

:clean_tool_temp
cd /d "%~dp0"
if exist "temp_spt_files" attrib -R "temp_spt_files\*" /S /D >nul 2>&1
if exist "temp_spt_files" rd /s /q "temp_spt_files" 2>nul
if not exist "temp_spt_files" exit /b 0
ping -n 2 127.0.0.1 >nul
if exist "temp_spt_files" attrib -R "temp_spt_files\*" /S /D >nul 2>&1
if exist "temp_spt_files" rd /s /q "temp_spt_files" 2>nul
exit /b 0

:prompt_con
<nul set /p "=%~1" >CON
set /p "%~2="
exit /b 0

:mark_run_error
if not exist "%~dp0StalkerPakToolFiles\logs" mkdir "%~dp0StalkerPakToolFiles\logs" >nul 2>&1
echo.>"%~dp0StalkerPakToolFiles\logs\_error"
echo.
echo An error log was saved in StalkerPakToolFiles\logs
echo.
exit /b 0

:copy_into
set "CI_SRC=%~1"
set "CI_DSTDIR=%~2"
set "CI_DST=!CI_DSTDIR!\%~nx1"
if not exist "!CI_SRC!" exit /b 1
if exist "!CI_DST!" exit /b 0
mklink /H "!CI_DST!" "!CI_SRC!" >nul 2>&1
if exist "!CI_DST!" exit /b 0
mklink "!CI_DST!" "!CI_SRC!" >nul 2>&1
if exist "!CI_DST!" exit /b 0
echo Copying %~nx1 ...
copy /y "!CI_SRC!" "!CI_DST!" >nul
if not exist "!CI_DST!" exit /b 1
exit /b 0

:resolve_game_dir
if "!GAME_DIR!"=="" exit /b 1
set "GAME_DIR=!GAME_DIR:"=!"
if "!GAME_DIR:~-1!"=="\" set "GAME_DIR=!GAME_DIR:~0,-1!"
set "RESOLVE_OUT="
for /f "delims=" %%R in ('powershell -NoProfile -Command "$p=$env:GAME_DIR; if (-not $p) { exit 1 }; $p=$p.Trim().TrimEnd([char]0x5C); for ($i=0; $i -lt 12; $i++) { if (Test-Path -LiteralPath (Join-Path $p \"Stalker2\\Content\\Paks\")) { Write-Output $p; exit 0 }; $n=Split-Path -Parent $p; if (-not $n -or $n -eq $p) { exit 1 }; $p=$n }; exit 1"') do set "RESOLVE_OUT=%%R"
if "!RESOLVE_OUT!"=="" exit /b 1
set "GAME_DIR=!RESOLVE_OUT!"
exit /b 0
