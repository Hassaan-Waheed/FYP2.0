"""
@file test_monitoring.py
@brief Test suite for monitoring components
@author [Your Name]
@date [Current Date]
@version 1.0
@copyright [Your Organization]

This module contains test cases for the monitoring components of the
Crypto Investment Analysis System. It includes unit tests for model
performance monitoring, system health monitoring, and alert generation.
"""

import pytest
import numpy as np
import pandas as pd
from monitoring.model_monitor import ModelMonitor
from monitoring.system_monitor import SystemMonitor
from monitoring.alert_manager import AlertManager
from datetime import datetime, timedelta
import psutil
import os

# Test data
SAMPLE_PREDICTIONS = pd.DataFrame({
    'timestamp': pd.date_range(start='2023-01-01', periods=100, freq='H'),
    'predicted': np.random.rand(100),
    'actual': np.random.rand(100),
    'confidence': np.random.rand(100)
})

SAMPLE_METRICS = {
    'accuracy': 0.85,
    'precision': 0.82,
    'recall': 0.88,
    'f1_score': 0.85
}

def test_model_performance_monitoring():
    """
    @brief Test model performance monitoring
    """
    monitor = ModelMonitor()
    
    # Update metrics
    monitor.update_metrics(SAMPLE_METRICS)
    
    # Check metrics
    current_metrics = monitor.get_current_metrics()
    assert isinstance(current_metrics, dict)
    assert all(metric in current_metrics for metric in SAMPLE_METRICS)
    assert all(0 <= value <= 1 for value in current_metrics.values())

def test_performance_threshold_alerts():
    """
    @brief Test performance threshold alerts
    """
    monitor = ModelMonitor()
    
    # Set thresholds
    monitor.set_thresholds({
        'accuracy': 0.8,
        'precision': 0.8,
        'recall': 0.8,
        'f1_score': 0.8
    })
    
    # Update metrics
    monitor.update_metrics(SAMPLE_METRICS)
    
    # Check alerts
    alerts = monitor.check_thresholds()
    assert isinstance(alerts, list)
    assert all(isinstance(alert, dict) for alert in alerts)

def test_performance_trend_analysis():
    """
    @brief Test performance trend analysis
    """
    monitor = ModelMonitor()
    
    # Add historical metrics
    for i in range(10):
        metrics = {
            'accuracy': 0.8 + 0.01 * i,
            'precision': 0.8 + 0.01 * i,
            'recall': 0.8 + 0.01 * i,
            'f1_score': 0.8 + 0.01 * i
        }
        monitor.update_metrics(metrics)
    
    # Analyze trends
    trends = monitor.analyze_trends()
    assert isinstance(trends, dict)
    assert all(metric in trends for metric in SAMPLE_METRICS)
    assert all(isinstance(trend, str) for trend in trends.values())

def test_system_resource_monitoring():
    """
    @brief Test system resource monitoring
    """
    monitor = SystemMonitor()
    
    # Get system metrics
    metrics = monitor.get_system_metrics()
    
    # Check metrics
    assert isinstance(metrics, dict)
    assert 'cpu_usage' in metrics
    assert 'memory_usage' in metrics
    assert 'disk_usage' in metrics
    assert all(0 <= value <= 100 for value in metrics.values())

def test_system_health_checks():
    """
    @brief Test system health checks
    """
    monitor = SystemMonitor()
    
    # Perform health check
    health_status = monitor.check_system_health()
    
    # Check health status
    assert isinstance(health_status, dict)
    assert 'status' in health_status
    assert health_status['status'] in ['healthy', 'degraded', 'critical']
    assert 'details' in health_status

def test_alert_generation():
    """
    @brief Test alert generation
    """
    alert_manager = AlertManager()
    
    # Generate test alert
    alert = alert_manager.generate_alert(
        level='warning',
        message='Test alert',
        source='test',
        details={'test': 'data'}
    )
    
    # Check alert
    assert isinstance(alert, dict)
    assert 'timestamp' in alert
    assert 'level' in alert
    assert 'message' in alert
    assert 'source' in alert
    assert 'details' in alert

def test_alert_aggregation():
    """
    @brief Test alert aggregation
    """
    alert_manager = AlertManager()
    
    # Generate multiple alerts
    for i in range(5):
        alert_manager.generate_alert(
            level='warning',
            message=f'Test alert {i}',
            source='test',
            details={'test': f'data_{i}'}
        )
    
    # Get aggregated alerts
    aggregated = alert_manager.get_aggregated_alerts()
    
    # Check aggregation
    assert isinstance(aggregated, dict)
    assert 'warning' in aggregated
    assert 'error' in aggregated
    assert 'critical' in aggregated
    assert len(aggregated['warning']) == 5

def test_alert_notification():
    """
    @brief Test alert notification
    """
    alert_manager = AlertManager()
    
    # Generate test alert
    alert = alert_manager.generate_alert(
        level='critical',
        message='Test critical alert',
        source='test',
        details={'test': 'data'}
    )
    
    # Check notification
    notification = alert_manager.send_notification(alert)
    assert isinstance(notification, dict)
    assert 'status' in notification
    assert notification['status'] in ['sent', 'failed']

def test_monitoring_persistence():
    """
    @brief Test monitoring data persistence
    """
    monitor = ModelMonitor()
    
    # Update metrics
    monitor.update_metrics(SAMPLE_METRICS)
    
    # Save metrics
    monitor.save_metrics('test_metrics.json')
    
    # Load metrics
    loaded_metrics = monitor.load_metrics('test_metrics.json')
    
    # Check persistence
    assert isinstance(loaded_metrics, dict)
    assert all(metric in loaded_metrics for metric in SAMPLE_METRICS)
    assert all(loaded_metrics[metric] == SAMPLE_METRICS[metric] for metric in SAMPLE_METRICS)

def test_monitoring_cleanup():
    """
    @brief Test monitoring cleanup
    """
    monitor = ModelMonitor()
    
    # Add test data
    monitor.update_metrics(SAMPLE_METRICS)
    
    # Cleanup old data
    monitor.cleanup_old_data(days=1)
    
    # Check cleanup
    metrics = monitor.get_historical_metrics()
    assert isinstance(metrics, pd.DataFrame)
    assert len(metrics) <= 1  # Only current metrics should remain 