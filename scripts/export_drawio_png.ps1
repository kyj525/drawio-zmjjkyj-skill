param(
    [Parameter(Mandatory = $true)]
    [string]$InputPath,

    [string]$OutputPath,
    [int]$Scale = 2
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Resolve-ExistingFile {
    param([Parameter(Mandatory = $true)][string]$Path)
    return (Resolve-Path -LiteralPath $Path -ErrorAction Stop).Path
}

function Get-DefaultOutputPath {
    param([Parameter(Mandatory = $true)][string]$SourcePath)
    $directory = Split-Path -Parent $SourcePath
    $basename = [System.IO.Path]::GetFileNameWithoutExtension($SourcePath)
    return Join-Path $directory ($basename + '.png')
}

function Get-DrawioExecutable {
    $envCandidates = @($env:DRAWIO_EXECUTABLE, $env:DIAGRAMS_NET_EXECUTABLE) | Where-Object { $_ }
    foreach ($candidate in $envCandidates) {
        if (Test-Path -LiteralPath $candidate) {
            return (Resolve-Path -LiteralPath $candidate).Path
        }
    }

    foreach ($commandName in @('draw.io', 'drawio', 'diagrams.net')) {
        $command = Get-Command $commandName -ErrorAction SilentlyContinue
        if ($command) { return $command.Source }
    }

    $pathCandidates = @(
        'C:\Program Files\draw.io\draw.io.exe',
        'C:\Program Files\diagrams.net\draw.io.exe',
        'C:\Program Files\diagrams.net\diagrams.net.exe',
        'C:\Program Files (x86)\draw.io\draw.io.exe',
        'C:\Program Files (x86)\diagrams.net\draw.io.exe',
        ('C:\Users\' + $env:USERNAME + '\AppData\Local\Programs\draw.io\draw.io.exe'),
        ('C:\Users\' + $env:USERNAME + '\AppData\Local\Programs\diagrams.net\draw.io.exe'),
        ('C:\Users\' + $env:USERNAME + '\AppData\Local\Programs\diagrams.net\diagrams.net.exe')
    )
    foreach ($candidate in $pathCandidates) {
        if (Test-Path -LiteralPath $candidate) {
            return (Resolve-Path -LiteralPath $candidate).Path
        }
    }

    throw "Could not find draw.io / diagrams.net desktop executable. Install diagrams.net desktop or set DRAWIO_EXECUTABLE / DIAGRAMS_NET_EXECUTABLE."
}

$inputFile = Resolve-ExistingFile -Path $InputPath
$outputFile = if ($OutputPath) { [System.IO.Path]::GetFullPath($OutputPath) } else { Get-DefaultOutputPath -SourcePath $inputFile }
$outputDirectory = Split-Path -Parent $outputFile
if ($outputDirectory -and -not (Test-Path -LiteralPath $outputDirectory)) {
    New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
}

$exe = Get-DrawioExecutable
$attempts = @(
    @('--export', '--format', 'png', '--scale', $Scale.ToString(), '--output', $outputFile, $inputFile),
    @('-x', '-f', 'png', '-s', $Scale.ToString(), '-o', $outputFile, $inputFile)
)

$lastError = $null
foreach ($attempt in $attempts) {
    try {
        & $exe @attempt
        if ($LASTEXITCODE -ne 0) { throw "draw.io export failed with exit code $LASTEXITCODE." }
        if (-not (Test-Path -LiteralPath $outputFile)) { throw "PNG was not created: $outputFile" }
        Write-Output $outputFile
        exit 0
    } catch {
        $lastError = $_
    }
}

throw "Unable to export PNG from '$inputFile'. Last error: $($lastError.Exception.Message)"
