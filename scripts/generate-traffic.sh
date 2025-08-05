#!/bin/bash
API_URL="http://localhost:5001"

# Check API availability
curl -sf "$API_URL/health" > /dev/null || { echo "API not accessible at $API_URL"; exit 1; }

echo "Generating traffic to $API_URL (Ctrl+C to stop)"

while true; do
    case $((RANDOM % 4)) in
        0|1) # POST payment
            amount=$((50 + RANDOM % 450))
            currencies=("EUR" "USD" "GBP")
            currency=${currencies[$RANDOM % 3]}
            curl -sf -X POST -H "Content-Type: application/json" \
                -d "{\"amount\": $amount, \"currency\": \"$currency\"}" \
                "$API_URL/api/payments" > /dev/null
            ;;
        2) # GET payments
            curl -sf "$API_URL/api/payments" > /dev/null
            ;;
        3) # GET transactions
            curl -sf "$API_URL/api/transactions" > /dev/null
            ;;
    esac
    sleep $((1 + RANDOM % 3))
done
