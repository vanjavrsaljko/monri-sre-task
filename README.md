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
curl -fsSL https://raw.githubusercontent.com/vanjavrsaljko/monri-sre-task/main/scripts/setup-app-vm.sh | bash
```

This script will:
- Install Docker
- Clone the repository
- Build and run the Flask API container
- Verify the application is running on port 5000

### Monitoring VM Setup

```bash
# Get the App VM IP address first, then run:
curl -fsSL https://raw.githubusercontent.com/vanjavrsaljko/monri-sre-task/main/scripts/setup-monitoring-vm.sh | bash -s <APP_VM_IP>

# Example:
curl -fsSL https://raw.githubusercontent.com/vanjavrsaljko/monri-sre-task/main/scripts/setup-monitoring-vm.sh | bash -s 10.0.1.100
```

This script will:
- Install Docker and Docker Compose
- Clone the repository
- Configure Prometheus to scrape the application VM at the provided IP
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

## Alerts (Grafana Unified Alerting)

Grafana unified alerting is enabled. Set up the following alert rules manually via the UI:

### Recommended Alert Rules:

1. **High Error Rate**
   - Query A: `(rate(payment_requests_total{status="error"}[5m]) / rate(payment_requests_total[5m])) * 100`
   - Condition B: `$A > 5`
   - Evaluation: Every 1m for 5m
   - Severity: Warning

2. **Slow Response Time**
   - Query A: `histogram_quantile(0.95, rate(payment_processing_duration_seconds_bucket[5m]))`
   - Condition B: `$A > 2`
   - Evaluation: Every 1m for 5m
   - Severity: Warning

3. **Application Down**
   - Query A: `up{job="payment-api"}`
   - Condition B: `$A < 1`
   - Evaluation: Every 1m for 1m
   - Severity: Critical

4. **High Active Transactions**
   - Query A: `active_transactions_gauge`
   - Condition B: `$A > 100`
   - Evaluation: Every 1m for 2m
   - Severity: Warning

### Setup Instructions:
1. Go to: http://monitoring-vm-ip:3000/alerting
2. Click "New rule" to create each alert
3. **Add Query A**: Enter the Prometheus query
4. **Add Expression B**: Set condition (e.g., `$A > 5`)
5. **Set Labels**: Add `severity=warning` or `severity=critical` in the Labels section
6. **Configure evaluation**: Set evaluation interval and "for" duration
7. **Add annotations**: Summary and description for alert details
8. Configure contact points for notifications (email, Slack, etc.)
9. Test alerts by running the traffic generator script

## API Endpoints

- `GET /health` - Health check
- `GET /api/payments` - List payments
- `POST /api/payments` - Create payment
- `GET /api/transactions` - List transactions
- `GET /metrics` - Prometheus metrics

## Traffic Generator

```bash
# Download and execute the traffic generator script
curl -fsSL https://raw.githubusercontent.com/vanjavrsaljko/monri-sre-task/main/scripts/generate-traffic.sh | bash
```

Generates realistic API traffic for dashboard testing:
- Creates random payment requests (50% of traffic)
- Queries payments and transactions (25% each)
- Random delays between 1-3 seconds
- Runs continuously until stopped

Created for Monri Payments d.o.o. SRE interview task.
