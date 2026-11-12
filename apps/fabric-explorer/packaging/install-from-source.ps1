# Windows routing; existing package installation needs no Node.js/npm/source toolchain.
$ErrorActionPreference = 'Stop'
$build = $false; $allow = $false; $dry = $false; $operation = 'install'; $directory = $null
for ($at = 0; $at -lt $args.Count; $at++) {
  switch ($args[$at]) {
    '--help' { Write-Output 'Usage: install-viewer.cmd --package-dir DIRECTORY [--allow-development] [--dry-run]'; Write-Output 'Source: install-viewer.cmd --build --allow-development [--dry-run]'; Write-Output 'Management: --rollback, --uninstall or --purge-preferences with --package-dir.'; Write-Output 'Source prerequisites: stable Node >=24.0.0/npm >=11.0.0, git, tar, unzip, zip; JAI_VIEWER_NODE/JAI_VIEWER_NPM_CLI select explicit host tools. No implicit downloads.'; exit 0 }
    '--build' { $build = $true }
    '--allow-development' { $allow = $true }
    '--dry-run' { $dry = $true }
    '--package-dir' { $at++; if ($at -ge $args.Count) { throw '--package-dir requires a directory' }; $directory = $args[$at] }
    { $_ -in '--rollback','--uninstall','--purge-preferences' } { if ($operation -ne 'install') { throw 'Choose one management operation' }; $operation = @{ '--rollback'='rollback'; '--uninstall'='uninstall'; '--purge-preferences'='purge' }[$_] }
    default { throw "Unknown viewer installation argument: $_" }
  }
}
if ([Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT -or [Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString() -ne 'X64') { throw 'Unsupported viewer platform/architecture; no changes made' }
if ($build) {
  if ($directory -or $operation -ne 'install') { throw '--build conflicts with --package-dir and management operations' }
  if (!$allow) { throw 'Unsigned source builds require --allow-development' }
  $node = if ($env:JAI_VIEWER_NODE) { $env:JAI_VIEWER_NODE } else { 'node' }
  $arguments = @((Join-Path $PSScriptRoot 'install-from-source.mjs'), '--build', '--allow-development'); if ($dry) { $arguments += '--dry-run' }
  & $node @arguments
  exit $LASTEXITCODE
}
if (!$directory) { throw 'Use --package-dir DIRECTORY, or explicitly --build --allow-development after installing the documented prerequisites.' }
if (!(Test-Path -LiteralPath $directory -PathType Container)) { throw 'Local package directory missing; no build is performed' }
$sidecars = @(Get-ChildItem -LiteralPath $directory -File | Where-Object { $_.Name -match '^jai-fabric-explorer-.+-win32-x64\.zip\.install\.ps1$' })
if ($sidecars.Count -ne 1) { throw 'Expected exactly one local Windows x64 package sidecar' }
if ($dry) { Write-Output "Plan $operation for $($sidecars[0].FullName); development permission $allow. No writes, execution or integrity verification performed."; exit 0 }
$arguments = @('-NoProfile', '-File', $sidecars[0].FullName, '-Operation', $operation); if ($allow) { $arguments += '-AllowDevelopment' }
& powershell.exe @arguments
exit $LASTEXITCODE
