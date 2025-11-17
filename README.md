# InsightHub

A FastAPI-based backend application with integrated Prometheus and Grafana for monitoring and visualization.

## 🏗️ Architecture

- **FastAPI**: Modern Python web framework for building APIs
- **PostgreSQL**: Database for application data
- **Redis**: Message queue for ML workers
- **MinIO**: S3-compatible object storage
- **ML Workers**: PyTorch and ONNX inference runners
- **Prometheus**: Metrics collection and time-series database
- **Grafana**: Metrics visualization and dashboards
- **Docker**: Containerized development environment

## 🚀 Quick Start

```bash
# Start all services
make up

# Stop services
make down

# View logs
make logs
```

## 📊 Monitoring Stack

### Prometheus
- Collects metrics from your API at `/metrics` endpoint
- Accessible at http://localhost:9090
- Stores time-series data for queries

### Grafana
- Pre-configured dashboard for API metrics
- Accessible at http://localhost:3000 (login: admin/admin)
- Visualizes:
  - Request rate
  - Request duration (latency)
  - Total requests
  - Status code distribution

### Available Metrics
- `http_requests_total` - Total number of HTTP requests
- `http_request_duration_seconds` - HTTP request latency histogram

## 📚 Documentation

- [Monitoring Guide](./MONITORING_GUIDE.md) - Complete guide for Prometheus & Grafana
- [API Docs](http://localhost:8000/docs) - Interactive API documentation (when running)
- [Prometheus UI](http://localhost:9090) - Query metrics directly
- [Grafana Dashboards](http://localhost:3000) - Visual metrics dashboard
