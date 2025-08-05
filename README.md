# Monri SRE Task - Monitoring Setup

## Overview

Python Flask API with Prometheus metrics monitored by Grafana dashboards.

## Architecture

- **VM 1**: Flask API (Docker container, port 5000)
- **VM 2**: Prometheus + Grafana (Docker Compose)

## Requirements

- **OS**: Ubuntu 24.04 LTS (tested and recommended)
- **VMs**: 2 separate Linux VMs with internet access
- **Resources**: 2GB RAM, 10GB disk per VM

## Setup

### Application VM Setup

```bash
# Download and execute the app VM setup script
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/monri-sre-task/main/scripts/setup-app-vm.sh | bash
```

This script will:
- Install Docker
- Clone the repository
- Build and run the Flask API container
- Verify the application is running on port 5000

### Monitoring VM Setup

```bash
# Download and execute the monitoring VM setup script
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/monri-sre-task/main/scripts/setup-monitoring-vm.sh | bash
```

This script will:
- Install Docker and Docker Compose
- Clone the repository
- Configure Prometheus to scrape the application VM
- Start Prometheus and Grafana services
- Verify services are running on ports 9090 and 3000

## Access

- **Grafana**: http://monitoring-vm-ip:3000 (admin/admin)
- **Prometheus**: http://monitoring-vm-ip:9090
- **API**: http://app-vm-ip:5000

## Metrics

1. **payment_requests_total** (Counter) - Total requests by method/status
2. **payment_processing_duration_seconds** (Histogram) - Response times
3. **active_transactions_gauge** (Gauge) - Active transactions

## Alerts

- **HighErrorRate**: >5% errors over 5min
- **SlowResponseTime**: 95th percentile >2s over 5min
- **ApplicationDown**: Service unavailable >1min
- **HighActiveTransactions**: >100 active >2min

## API Endpoints

- `GET /health` - Health check
- `GET /api/payments` - List payments
- `POST /api/payments` - Create payment
- `GET /api/transactions` - List transactions
- `GET /metrics` - Prometheus metrics

## Traffic Generator

```bash
./scripts/generate-traffic.sh
```

Generates realistic API traffic for dashboard testing:
- Creates random payment requests (50% of traffic)
- Queries payments and transactions (25% each)
- Random delays between 1-3 seconds
- Runs continuously until stopped

Created for Monri Payments d.o.o. SRE interview task.
