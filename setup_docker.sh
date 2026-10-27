#!/bin/bash
mkdir -p /etc/systemd/system/docker.service.d
cat << 'EOF' > /etc/systemd/system/docker.service.d/override.conf
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0:2375 --tls=false
EOF
systemctl daemon-reload
systemctl restart docker
sleep 1
docker info
