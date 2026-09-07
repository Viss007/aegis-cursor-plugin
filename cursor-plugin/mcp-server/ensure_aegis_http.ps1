$ErrorActionPreference = "Stop"
$port = 8815
$listening = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
if ($listening) {
  $pid0 = @($listening.OwningProcess)[0]
  Write-Output "Aegis HTTP already on $port (pid $pid0)"
  exit 0
}
$py = "C:\Users\Vismantas\AppData\Local\Programs\Python\Python311\python.exe"
$script = "C:\Users\Vismantas\Desktop\viss-workspace\aegis\cursor-plugin\mcp-server\run_aegis_http.py"
$logDir = "C:\Users\Vismantas\Desktop\viss-workspace\var\aegis"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$out = Join-Path $logDir "http-8815.out.log"
$err = Join-Path $logDir "http-8815.err.log"
$p = Start-Process -FilePath $py -ArgumentList $script -WindowStyle Hidden -RedirectStandardOutput $out -RedirectStandardError $err -PassThru
Start-Sleep -Seconds 3
$listening = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
if (-not $listening) {
  $tail = ""
  if (Test-Path $err) { $tail = Get-Content $err -Raw -ErrorAction SilentlyContinue }
  throw "Aegis HTTP failed to bind :$port. Log: $tail"
}
Write-Output "STARTED pid=$($p.Id) http://127.0.0.1:$port/mcp"
