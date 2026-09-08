$ErrorActionPreference = "Stop"
$port = 18715
if ($env:AEGIS_PORT) { $port = [int]$env:AEGIS_PORT }
$listening = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
if ($listening) {
  $pid0 = @($listening.OwningProcess)[0]
  Write-Output "Aegis HTTP already on $port (pid $pid0)"
  exit 0
}

$Root = $PSScriptRoot
$py = $env:AEGIS_PYTHON
if (-not $py) {
  $cmd = Get-Command python -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($cmd) { $py = $cmd.Source }
}
if (-not $py -and $env:LocalAppData) {
  $guess = Join-Path $env:LocalAppData "Programs\Python\Python311\python.exe"
  if (Test-Path -LiteralPath $guess) { $py = $guess }
}
if (-not $py) { throw "python not found. Set AEGIS_PYTHON." }

$script = Join-Path $Root "run_aegis_http.py"
if (-not (Test-Path -LiteralPath $script)) { throw "missing $script" }

$logDir = $env:AEGIS_LOG_DIR
if (-not $logDir) {
  $wsVar = Join-Path $Root "..\..\..\var\aegis"
  if (Test-Path -LiteralPath (Split-Path -Parent $wsVar)) {
    $logDir = $wsVar
  } else {
    $logDir = Join-Path $Root "logs"
  }
}
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$out = Join-Path $logDir "http-$port.out.log"
$err = Join-Path $logDir "http-$port.err.log"
$env:AEGIS_PORT = "$port"
$p = Start-Process -FilePath $py -ArgumentList $script -WindowStyle Hidden -RedirectStandardOutput $out -RedirectStandardError $err -PassThru
Start-Sleep -Seconds 3
$listening = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
if (-not $listening) {
  $tail = ""
  if (Test-Path -LiteralPath $err) { $tail = Get-Content -LiteralPath $err -Raw -ErrorAction SilentlyContinue }
  throw "Aegis HTTP failed to bind :$port. Log: $tail"
}
Write-Output "STARTED pid=$($p.Id) http://127.0.0.1:$port/mcp"
