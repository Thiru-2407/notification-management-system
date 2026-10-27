$kubeDir = "$env:USERPROFILE\.kube"
New-Item -ItemType Directory -Force -Path $kubeDir | Out-Null
$wslIp = (wsl -d Ubuntu hostname -I).Trim().Split(' ')[0]
$config = wsl -d Ubuntu cat /etc/rancher/k3s/k3s.yaml
$config = $config -replace 'https://127.0.0.1:6443', "https://${wslIp}:6443"
$config = $config -replace 'certificate-authority-data:.*', 'insecure-skip-tls-verify: true'
Set-Content -Path "$kubeDir\config" -Value $config
Write-Output "Configured kubectl with $wslIp:6443"
& kubectl get nodes -o wide
