$dirs = @(
    'evidence\01_environment',
    'evidence\02_application',
    'evidence\03_github',
    'evidence\04_tests',
    'evidence\05_jenkins',
    'evidence\06_docker',
    'evidence\07_dockerhub',
    'evidence\08_kubernetes',
    'evidence\09_browser_verification',
    'evidence\10_final_report'
)
foreach ($d in $dirs) {
    New-Item -ItemType Directory -Force -Path $d | Out-Null
}
Get-ChildItem evidence | Select-Object Name
