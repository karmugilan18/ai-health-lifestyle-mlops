from prometheus_client import Counter, Histogram, Gauge
PREDICTIONS = Counter("health_demo_predictions_total", "Lifestyle demo predictions")
LATENCY = Histogram("health_demo_prediction_latency_seconds", "Prediction latency in seconds")
ERRORS = Counter("health_demo_api_errors_total", "API errors")
MODEL_READY = Gauge("health_demo_model_ready", "1 if model loaded")
