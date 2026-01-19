$ErrorActionPreference = "Stop"

Write-Host "============================================="
Write-Host "  INSTALADOR AUTOMATICO DO CHROMEDRIVER"
Write-Host "============================================="
Write-Host ""

Write-Host "Detectando versao do Google Chrome..."

$chromeVersion = $null

$paths = @(
    "HKLM:\SOFTWARE\Google\Chrome\BLBeacon",
    "HKLM:\SOFTWARE\WOW6432Node\Google\Chrome\BLBeacon",
    "HKCU:\Software\Google\Chrome\BLBeacon"
)

foreach ($p in $paths) {
    if (Test-Path $p) {
        try {
            $chromeVersion = (Get-ItemProperty $p).version
            if ($chromeVersion) { break }
        } catch {
        }
    }
}

if (-not $chromeVersion) {
    Write-Host "ERRO: Google Chrome nao encontrado."
    exit 1
}

Write-Host "Chrome detectado: versao $chromeVersion"

$majorVersion = $chromeVersion.Split(".")[0]
$apiUrl = "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_$majorVersion"

Write-Host "Buscando versao do ChromeDriver para $majorVersion..."

try {
    $driverVersion = Invoke-RestMethod -Uri $apiUrl
} catch {
    Write-Host "ERRO: nao foi possivel obter a versao do ChromeDriver."
    exit 1
}

Write-Host "ChromeDriver encontrado: versao $driverVersion"

$downloadUrl = "https://storage.googleapis.com/chrome-for-testing-public/$driverVersion/win32/chromedriver-win32.zip"

Write-Host "Baixando ChromeDriver..."
Invoke-WebRequest -Uri $downloadUrl -OutFile "chromedriver.zip"

if (Test-Path "chromedriver_temp") {
    Remove-Item "chromedriver_temp" -Recurse -Force
}

Write-Host "Extraindo arquivos..."
Expand-Archive -Path "chromedriver.zip" -DestinationPath "chromedriver_temp" -Force

$driverExe = Get-ChildItem "chromedriver_temp" -Recurse -Filter "chromedriver.exe" | Select-Object -First 1

if (-not $driverExe) {
    Write-Host "ERRO: chromedriver.exe nao encontrado apos extracao."
    exit 1
}

Move-Item $driverExe.FullName ".\chromedriver.exe" -Force

Remove-Item "chromedriver.zip" -Force
Remove-Item "chromedriver_temp" -Recurse -Force

Write-Host ""
Write-Host "ChromeDriver instalado com sucesso."
Write-Host "Local: $(Get-Location)\chromedriver.exe"
Write-Host ""