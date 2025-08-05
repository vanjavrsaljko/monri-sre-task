#!/usr/bin/env python3
"""
Monri SRE Task - Sample Payment API
A lightweight Flask application that exposes Prometheus metrics for monitoring.
"""

import time
import random
from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Prometheus Metrics - 3 Custom Metrics as required
payment_requests_total = Counter(
    'payment_requests_total',
    'Total number of payment requests processed',
    ['method', 'status']
)

payment_processing_duration_seconds = Histogram(
    'payment_processing_duration_seconds',
    'Time spent processing payment requests',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

active_transactions_gauge = Gauge(
    'active_transactions_gauge',
    'Number of currently active transactions'
)

# In-memory storage for demo purposes
payments = []
transactions = []
active_transaction_count = 0

def simulate_processing_time():
    """Simulate variable processing time"""
    return random.uniform(0.1, 3.0)

def simulate_error():
    """Simulate occasional errors (10% chance)"""
    return random.random() < 0.1

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'service': 'monri-payment-api'
    }), 200

@app.route('/api/payments', methods=['GET'])
def get_payments():
    """Get all payments"""
    start_time = time.time()
    
    try:
        # Simulate processing
        time.sleep(simulate_processing_time())
        
        if simulate_error():
            payment_requests_total.labels(method='GET', status='error').inc()
            return jsonify({'error': 'Internal server error'}), 500
        
        payment_requests_total.labels(method='GET', status='success').inc()
        
        response = {
            'payments': payments,
            'count': len(payments)
        }
        
        return jsonify(response), 200
    
    finally:
        processing_time = time.time() - start_time
        payment_processing_duration_seconds.observe(processing_time)

@app.route('/api/payments', methods=['POST'])
def create_payment():
    """Create a new payment"""
    global active_transaction_count
    start_time = time.time()
    
    try:
        # Simulate active transaction
        active_transaction_count += 1
        active_transactions_gauge.set(active_transaction_count)
        
        # Simulate processing
        time.sleep(simulate_processing_time())
        
        if simulate_error():
            payment_requests_total.labels(method='POST', status='error').inc()
            return jsonify({'error': 'Payment processing failed'}), 500
        
        # Create payment
        payment_data = request.get_json() or {}
        payment = {
            'id': len(payments) + 1,
            'amount': payment_data.get('amount', 100.0),
            'currency': payment_data.get('currency', 'EUR'),
            'status': 'completed',
            'timestamp': time.time()
        }
        
        payments.append(payment)
        payment_requests_total.labels(method='POST', status='success').inc()
        
        return jsonify(payment), 201
    
    finally:
        # Transaction completed
        active_transaction_count = max(0, active_transaction_count - 1)
        active_transactions_gauge.set(active_transaction_count)
        
        processing_time = time.time() - start_time
        payment_processing_duration_seconds.observe(processing_time)

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """Get all transactions"""
    start_time = time.time()
    
    try:
        # Simulate processing
        time.sleep(simulate_processing_time())
        
        if simulate_error():
            payment_requests_total.labels(method='GET', status='error').inc()
            return jsonify({'error': 'Database connection failed'}), 500
        
        # Generate some sample transactions
        sample_transactions = [
            {
                'id': i,
                'payment_id': (i % len(payments)) + 1 if payments else None,
                'type': random.choice(['authorization', 'capture', 'refund']),
                'status': random.choice(['pending', 'completed', 'failed']),
                'timestamp': time.time() - random.randint(0, 86400)
            }
            for i in range(1, 11)
        ]
        
        transactions.extend(sample_transactions)
        payment_requests_total.labels(method='GET', status='success').inc()
        
        response = {
            'transactions': sample_transactions,
            'count': len(sample_transactions)
        }
        
        return jsonify(response), 200
    
    finally:
        processing_time = time.time() - start_time
        payment_processing_duration_seconds.observe(processing_time)

@app.route('/metrics', methods=['GET'])
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        'service': 'Monri Payment API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'payments': '/api/payments',
            'transactions': '/api/transactions',
            'metrics': '/metrics'
        },
        'metrics': {
            'payment_requests_total': 'Counter - Total payment requests',
            'payment_processing_duration_seconds': 'Histogram - Processing time',
            'active_transactions_gauge': 'Gauge - Active transactions'
        }
    }), 200

if __name__ == '__main__':
    print("Starting Monri Payment API...")
    print("Endpoints:")
    print("  Health: http://localhost:5000/health")
    print("  Payments: http://localhost:5000/api/payments")
    print("  Transactions: http://localhost:5000/api/transactions")
    print("  Metrics: http://localhost:5000/metrics")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
