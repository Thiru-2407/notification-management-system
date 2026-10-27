$output = @()
$output += "=== ENVIRONMENT & TOOL INSPECTION ==="
$output += "Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$output += "User: $(whoami)"
$output += "OS: $([System.Environment]::OSVersion.VersionString)"

$output += "`n[VS Code]"
try { $res = & code --version 2>&1; $output += $res } catch { $output += "VS Code CLI error: $_" }

$output += "`n[Git]"
try { $res = & git --version 2>&1; $output += $res } catch { $output += "Git error: $_" }
try { $output += "User name: $(git config --global user.name)" } catch {}
try { $output += "User email: $(git config --global user.email)" } catch {}

$output += "`n[Python & Pip]"
try { $res = & python --version 2>&1; $output += $res } catch { $output += "Python error: $_" }
try { $res = & pip --version 2>&1; $output += $res } catch { $output += "Pip error: $_" }

$output += "`n[Docker]"
try { $res = & docker --version 2>&1; $output += $res } catch { $output += "Docker error: $_" }
try { $res = & docker info --format 'ServerVersion: {{.ServerVersion}}, OperatingSystem: {{.OperatingSystem}}' 2>&1; $output += $res } catch { $output += "Docker info error: $_" }
try {
    # Check docker login status / config
    $dockerCfg = "$HOME\.docker\config.json"
    if (Test-Path $dockerCfg) {
        $cfgJson = Get-Content $dockerCfg | ConvertFrom-Json
        $auths = ($cfgJson.auths | Get-Member -MemberType NoteProperty).Name
        $output += "Docker config auths found: $($auths -join ', ')"
    } else {
        $output += "No ~/.docker/config.json found"
    }
} catch { $output += "Docker config check error: $_" }

$output += "`n[Kubernetes / kubectl]"
try { $res = & kubectl version --client=true --output=yaml 2>&1; $output += $res } catch { $output += "kubectl error: $_" }
try { $res = & kubectl cluster-info 2>&1; $output += $res } catch { $output += "kubectl cluster-info error: $_" }
try { $res = & kubectl get nodes 2>&1; $output += $res } catch { $output += "kubectl get nodes error: $_" }

$output += "`n[Minikube]"
try { $res = & minikube version 2>&1; $output += $res } catch { $output += "minikube error: $_" }
try { $res = & minikube status 2>&1; $output += $res } catch { $output += "minikube status error: $_" }

$output += "`n[Jenkins]"
try {
    $jenkinsService = Get-Service -Name "*jenkins*" -ErrorAction SilentlyContinue
    if ($jenkinsService) { $output += ($jenkinsService | Out-String) } else { $output += "No Jenkins service registered in Windows Services." }
} catch { $output += "Jenkins service check error: $_" }
try {
    $t = Test-NetConnection -ComputerName localhost -Port 8080 -WarningAction SilentlyContinue
    $output += "Port 8080 test: $($t.TcpTestSucceeded)"
} catch { $output += "Port 8080 test error: $_" }

$output += "`n[Headless Browser / Edge / Chrome]"
try {
    if (Test-Path "C:\Program Files\Google\Chrome\Application\chrome.exe") {
        $output += "Chrome installed: $((Get-Item 'C:\Program Files\Google\Chrome\Application\chrome.exe').VersionInfo.ProductVersion)"
    } else {
        $output += "Chrome not found at standard path"
    }
} catch {}
try {
    if (Test-Path "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe") {
        $output += "Edge installed: $((Get-Item 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe').VersionInfo.ProductVersion)"
    } else {
        $output += "Edge not found at standard path"
    }
} catch {}

$outputString = $output -join "`r`n"
Write-Output $outputString
New-Item -ItemType Directory -Force -Path "evidence\01_environment" | Out-Null
Set-Content -Path "evidence\01_environment\tool_versions.txt" -Value $outputString
