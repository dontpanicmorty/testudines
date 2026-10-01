# Builds SQL Dojo.msi (Windows) via Tauri. Windows counterpart to build.sh (macOS/Linux) —
# Tauri needs a native build on each target OS (installer formats and webview backends are
# OS-specific: .app/WKWebView on macOS vs .msi/WebView2 here); ../webapp is the same,
# unmodified frontend either way.
#
# Bundles an .msi installer. Tauri's bundler downloads the WiX Toolset it needs for .msi
# automatically, so no extra installs are required beyond Rust/Cargo itself. (An NSIS .exe
# bundle is also possible via `cargo tauri build --bundles nsis`, but that requires NSIS to be
# installed separately — .msi avoids that.)

$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "src-tauri")

if (-not (Get-Command cargo -ErrorAction SilentlyContinue)) {
    Write-Host "cargo not found. SQL Dojo needs the Rust toolchain to build." -ForegroundColor Yellow
    $reply = Read-Host 'Type "agree" to install Rust now via rustup (https://rustup.rs). Any other submission will abort the Rust installation and app setup'
    if ($reply -eq "agree") {
        $installer = Join-Path $env:TEMP "rustup-init.exe"
        Invoke-WebRequest -Uri "https://win.rustup.rs/x86_64" -OutFile $installer

        # --no-modify-path: this build only needs cargo on PATH for the rest of this session,
        # which the PATH update below already provides — it doesn't need rustup to touch any
        # persistent user/system PATH.
        & $installer -y --no-modify-path
        Remove-Item $installer -ErrorAction SilentlyContinue

        $cargoBin = Join-Path $env:USERPROFILE ".cargo\bin"
        $env:PATH = "$cargoBin;$env:PATH"
    } else {
        Write-Error "Aborting: Rust installation and app setup were not agreed to."
        exit 1
    }
}

cargo tauri --version *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing tauri-cli (one-time)..."
    cargo install tauri-cli --version "^2.0.0" --locked
}

cargo tauri build --bundles msi

Write-Host ""
Write-Host "Built: src-tauri\target\release\bundle\msi\SQL Dojo_1.0.0_x64_en-US.msi"
Write-Host "Run the installer to install SQL Dojo, then launch it from the Start Menu."
