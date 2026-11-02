# Py Dojo launcher (Windows). Self-contained: uses no system Python.
$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Here
$env:UV_PYTHON_INSTALL_DIR = "$Here\.tools\python"
$env:UV_PYTHON_PREFERENCE = "only-managed"
$env:UV_PROJECT_ENVIRONMENT = "$Here\.venv"
$env:UV_CACHE_DIR = "$Here\.tools\uv-cache"
$env:UV_NO_ENV_FILE = "1"
$Uv = "$Here\.tools\bin\uv.exe"
if (-not (Test-Path $Uv)) {
  $found = Get-Command uv -ErrorAction SilentlyContinue
  if ($found) { $Uv = $found.Source } else {
    Write-Host "Installing uv (one-time)..."
    $env:UV_UNMANAGED_INSTALL = "$Here\.tools\bin"
    Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
  }
}
& $Uv run pydojo @args
