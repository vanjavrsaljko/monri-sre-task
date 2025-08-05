#!/bin/bash
set -e

REPO_URL="https://github.com/YOUR_USERNAME/monri-sre-task.git"
WORK_DIR="/tmp/monri-app-setup"
APP_DIR="/opt/monri-payment-api"
CONTAINER_NAME="monri-payment-api"
IMAGE_NAME="monri-payment-api:latest"

cleanup() { rm -rf "$WORK_DIR"; }
trap cleanup EXIT

# Install Docker
sudo apt update -qq
sudo apt install -y curl git
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
sudo systemctl enable --now docker

# Deploy app
mkdir -p "$WORK_DIR" && cd "$WORK_DIR"
git clone "$REPO_URL" .
sudo mkdir -p "$APP_DIR"
sudo cp -r app/* "$APP_DIR/"
sudo chown -R $USER:$USER "$APP_DIR"

cd "$APP_DIR"
sudo docker build -t "$IMAGE_NAME" .
sudo docker stop "$CONTAINER_NAME" 2>/dev/null || true
sudo docker rm "$CONTAINER_NAME" 2>/dev/null || true
sudo docker run -d --name "$CONTAINER_NAME" --restart unless-stopped -p 5000:5000 "$IMAGE_NAME"

# Verify
sleep 10
curl -sf http://localhost:5000/health > /dev/null && echo "✅ App running on $(hostname -I | awk '{print $1}'):5000"
