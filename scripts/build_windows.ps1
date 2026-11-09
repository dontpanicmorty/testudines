# Builds a self-contained Testudines folder and .zip for Windows.
# The folder embeds its own Python and every library: the result needs no internet, no uv and no
# system Python. Unzip it anywhere and double-click Testudines.cmd. Building needs internet once.
$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Here
$Dist = Join-Path $Here "dist"
$App = Join-Path $Dist "Testudines"
$Tmp = Join-Path $Dist "build-tmp"
$Version = (Select-String -Path pyproject.toml -Pattern '^version = "(.*)"').Matches[0].Groups[1].Value

# --- uv (build-time only) -------------------------------------------------
$Uv = Join-Path $Here ".tools\bin\uv.exe"
if (-not (Test-Path $Uv)) {
  $found = Get-Command uv -ErrorAction SilentlyContinue
  if ($found) { $Uv = $found.Source } else {
    $env:UV_UNMANAGED_INSTALL = Join-Path $Here ".tools\bin"
    Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
  }
}
$env:UV_NO_ENV_FILE = "1"
Remove-Item Env:UV_NATIVE_TLS, Env:UV_SYSTEM_CERTS, Env:VIRTUAL_ENV -ErrorAction SilentlyContinue
if ((& $Uv help 2>$null) -match "--system-certs") { $env:UV_SYSTEM_CERTS = "1" } else { $env:UV_NATIVE_TLS = "1" }

Write-Host "==> Cleaning"
Remove-Item -Recurse -Force $App, $Tmp -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force $App, $Tmp | Out-Null

Write-Host "==> Embedding Python 3.12"
$env:UV_PYTHON_INSTALL_DIR = Join-Path $Tmp "py"
& $Uv python install cpython-3.12-windows-x86_64-none  # x64: also runs on Windows on Arm, emulated
if ($LASTEXITCODE) { throw "python install failed" }
Remove-Item Env:UV_PYTHON_INSTALL_DIR
$SrcPy = Get-ChildItem (Join-Path $Tmp "py") -Directory | Where-Object Name -like "cpython-3.12*-windows-x86_64-*" | Select-Object -First 1
Copy-Item -Recurse $SrcPy.FullName (Join-Path $App "python")
$Py = Join-Path $App "python\python.exe"
& $Py --version

Write-Host "==> Installing Testudines + libraries into the bundled Python"
& $Uv pip install --python $Py --break-system-packages --compile-bytecode $Here
if ($LASTEXITCODE) { throw "install failed" }

# Polars' default runtime needs AVX2-era CPU features that older PCs (and some emulation on Windows on
# Arm) lack; its compatibility runtime runs on any 64-bit CPU. The exercises' data is small.
Write-Host "==> Polars compatibility runtime (any 64-bit CPU)"
$PolarsVersion = & $Py -c "import importlib.metadata as m; print(m.version('polars'))"
& $Uv pip install --python $Py --break-system-packages --compile-bytecode "polars-runtime-compat==$PolarsVersion"
if ($LASTEXITCODE) { throw "polars compat install failed" }
& $Uv pip uninstall --python $Py --break-system-packages polars-runtime-32 polars-runtime-64 2>$null

Write-Host "==> Removing the parts of Qt the app never uses"
& $Py -I (Join-Path $Here "scripts\prune_bundle.py") (Join-Path $App "python\Lib\site-packages")
if ($LASTEXITCODE) { throw "prune failed" }

Write-Host "==> Bundling the SQL and Python curricula and datasets"
Copy-Item -Recurse (Join-Path $Here "content") (Join-Path $App "content")
Copy-Item -Recurse (Join-Path $Here "datasets") (Join-Path $App "datasets")
Get-ChildItem $App -Recurse -Directory -Include "__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache" |
  Where-Object { $_.FullName -notlike "*\python\*" } | Remove-Item -Recurse -Force

Write-Host "==> Launcher"
# Starts the bundled Python without a console window, from wherever the folder was unzipped.
@'
@echo off
setlocal
set "HERE=%~dp0"
set "PYTHONHOME="
set "PYTHONPATH="
set "TESTUDINES_PACKAGED=1"
set "PYTHONDONTWRITEBYTECODE=1"
set "TESTUDINES_CONTENT=%HERE%content"
set "TESTUDINES_DATASETS=%HERE%datasets"
if /I "%~1"=="selftest" goto console
if /I "%~1"=="validate" goto console
start "" "%HERE%python\pythonw.exe" -m testudines %*
exit /b 0
:console
"%HERE%python\python.exe" -m testudines %*
exit /b %ERRORLEVEL%
'@ | Set-Content -Encoding ASCII (Join-Path $App "Testudines.cmd")
Copy-Item (Join-Path $Here "src\testudines\assets\icon.png") (Join-Path $App "icon.png")

Write-Host "==> Self-test of the packaged build"
$env:TESTUDINES_HOME = Join-Path $Tmp "selftest-data"
$env:QT_QPA_PLATFORM = "offscreen"
& (Join-Path $App "Testudines.cmd") selftest
if ($LASTEXITCODE) { throw "selftest failed" }
Remove-Item Env:TESTUDINES_HOME, Env:QT_QPA_PLATFORM

Write-Host "==> Zip"
$Zip = Join-Path $Dist "Testudines-$Version-windows-x64.zip"
Remove-Item -Force $Zip -ErrorAction SilentlyContinue
Compress-Archive -Path $App -DestinationPath $Zip
Remove-Item -Recurse -Force $Tmp
Write-Host ""
Write-Host "Built: $App"
Write-Host "       $Zip"
