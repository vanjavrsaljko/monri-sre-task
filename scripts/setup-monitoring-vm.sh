#!/bin/bash
set -e

REPO_URL="https://github.com/YOUR_USERNAME/monri-sre-task.git"
WORK_DIR="/tmp/monri-sre-setup"
MONITORING_DIR="/opt/monri-monitoring"

cleanup() { rm -rf "$WORK_DIR"; }
trap cleanup EXIT

# Install Docker & Docker Compose
sudo apt update -qq
sudo apt install -y curl git
curl -fsSL https://get.docker.com | sh
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo usermod -aG docker $USER
sudo systemctl enable --now docker

# Deploy monitoring stack
mkdir -p "$WORK_DIR" && cd "$WORK_DIR"
git clone "$REPO_URL" .
sudo mkdir -p "$MONITORING_DIR"
sudo chown $USER:$USER "$MONITORING_DIR"
cp -r monitoring/* "$MONITORING_DIR/"

# Configure app IP
read -p "App VM IP: " APP_VM_IP
[[ -n "$APP_VM_IP" ]] && sed -i "s/APPLICATION_VM_IP/$APP_VM_IP/g" "$MONITORING_DIR/prometheus/prometheus.yml"

# Start services
cd "$MONITORING_DIR"
sudo docker-compose up -d
sleep 20

# Verify
curl -sf http://localhost:9090/-/healthy > /dev/null && curl -sf http://localhost:3000/api/health > /dev/null && \
echo "✅ Monitoring stack running: Grafana $(hostname -I | awk '{print $1}'):3000 (admin/admin)"
