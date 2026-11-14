@echo off
setlocal EnableExtensions
cd /d "%~dp0"

ECHO.
ECHO ========================================================
ECHO  Muhammad Zikriya - WEBSITE and REVEALJS SLIDES
ECHO ========================================================
ECHO.
where quarto >nul 2>&1
if errorlevel 1 goto NO_QUARTO

if not exist "_quarto.yml" goto NO_YAML
if not exist "_RNN_LSTM_SOURCE\index.qmd" goto NO_SOURCE
if not exist "slides\police-bcc\index.qmd" goto NO_WANDA
if not exist "slides\police-bcc\UFPE_logo.png" goto NO_LOGOS
if not exist "slides\police-bcc\GEDAI_logo.png" goto NO_LOGOS

ECHO [1/5] Copy the original WANDA logos ONLY into the new lecture source.
copy /Y "slides\police-bcc\UFPE_logo.png" "_RNN_LSTM_SOURCE\assets\UFPE_logo.png" >nul
if errorlevel 1 goto FAILED
copy /Y "slides\police-bcc\GEDAI_logo.png" "_RNN_LSTM_SOURCE\assets\GEDAI_logo.png" >nul
if errorlevel 1 goto FAILED

ECHO [2/5] Render your existing Quarto website (WANDA is preserved).
quarto render
if errorlevel 1 goto FAILED

ECHO [3/5] Render the RNN/LSTM RevealJS slides in the SEPARATE Quarto project.
pushd "_RNN_LSTM_SOURCE"
quarto render index.qmd --to revealjs
if errorlevel 1 (
    popd
    goto FAILED
)
popd
if not exist "_RNN_LSTM_SOURCE\index.html" goto NO_PRESENTATION

ECHO [4/5] Remove the old published RNN/LSTM page, not the WANDA files.
if exist "docs\slides\rnn-lstm" rmdir /S /Q "docs\slides\rnn-lstm"
if errorlevel 1 goto FAILED
if not exist "docs\slides\rnn-lstm" mkdir "docs\slides\rnn-lstm"

ECHO [5/5] Copy finished slideshow and its resources into GitHub Pages output.
robocopy "_RNN_LSTM_SOURCE" "docs\slides\rnn-lstm" /E /NFL /NDL /NJH /NJS /NC /NS /XF *.qmd *.R *.py *.pt *.md *.bib *.csv *.json *.scss _quarto.yml /XD .quarto _freeze __pycache__ .git
if errorlevel 8 goto FAILED
if not exist "docs\slides\rnn-lstm\index.html" goto NO_PRESENTATION

ECHO.
ECHO Checking that the published page is really a RevealJS slideshow...
findstr /I /C:"revealjs" "docs\slides\rnn-lstm\index.html" >nul
if errorlevel 1 goto NOT_SLIDES

ECHO.
ECHO ========================================================
ECHO SUCCESS: The new page is RevealJS, not a normal webpage.
ECHO ========================================================
ECHO Open: docs\slides\rnn-lstm\index.html
ECHO Your WANDA presentation is unchanged.
ECHO.
ECHO To publish, in RStudio Terminal run:
ECHO   git add -A
ECHO   git commit -m "Publish RNN LSTM RevealJS lecture"
ECHO   git push origin main
ECHO.
pause
exit /b 0

:NO_QUARTO
ECHO ERROR: Quarto was not found in the Terminal PATH.
goto FAILED
:NO_YAML
ECHO ERROR: _quarto.yml is not in this website folder.
goto FAILED
:NO_SOURCE
ECHO ERROR: _RNN_LSTM_SOURCE\index.qmd is missing.
goto FAILED
:NO_WANDA
ECHO ERROR: WANDA source slides\police-bcc\index.qmd is missing.
ECHO Do not delete or replace your WANDA folder.
goto FAILED
:NO_LOGOS
ECHO ERROR: Existing WANDA logo files are missing.
ECHO Expected slides\police-bcc\UFPE_logo.png and GEDAI_logo.png.
goto FAILED
:NO_PRESENTATION
ECHO ERROR: Quarto did not produce the presentation index.html.
goto FAILED
:NOT_SLIDES
ECHO ERROR: The published index.html does not look like RevealJS.
ECHO Do not push this output to GitHub.
goto FAILED
:FAILED
ECHO.
ECHO BUILD FAILED. Do NOT run git push. Read the error above.
pause
exit /b 1
