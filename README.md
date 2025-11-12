# InsightHub

A FastAPI-based backend application with integrated Prometheus and Grafana for monitoring and visualization.

## 🏗️ Architecture

- **FastAPI**: Modern Python web framework for building APIs
- **PostgreSQL**: Database for application data
- **Prometheus**: Metrics collection and time-series database
- **Grafana**: Metrics visualization and dashboards
- **Docker**: Containerized development environment

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)

### 1. Environment Setup

Create a `.env` file in the project root:

```bash
# Database
PG_USER=postgres
PG_PASSWORD=your_secure_password
PG_DB=insighthub
PG_EXPOSE_PORT=5432

# API
API_PORT=8000

# Grafana (optional)
GRAFANA_USER=admin
GRAFANA_PASSWORD=admin
```

### 2. Start Services

```bash
cd infra
docker-compose up -d
```

This starts:
- **API**: http://localhost:8000
- **Grafana**: http://localhost:3000
- **Prometheus**: http://localhost:9090
- **PostgreSQL**: localhost:5432

### 3. Verify Setup

```bash
# Check API health
curl http://localhost:8000/health

# View metrics endpoint
curl http://localhost:8000/metrics

# Access Grafana
open http://localhost:3000
# Default login: admin / admin

# Access Prometheus
open http://localhost:9090
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

## 🛠️ Development

### Local Development (without Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Run API locally
cd apps/api
uvicorn app.main:app --reload --port 8000
```

### Project Structure

```
InsightHub/
├── apps/
│   └── api/              # FastAPI application
│       ├── app/
│       │   ├── core/     # Configuration
│       │   ├── db/       # Database setup
│       │   └── routers/  # API routes
│       └── Dockerfile
├── infra/
│   ├── docker-compose.yml
│   ├── prometheus/       # Prometheus configuration
│   └── grafana/          # Grafana dashboards and provisioning
├── requirements.txt
└── README.md
```

## 📚 Documentation

- [Monitoring Guide](./MONITORING_GUIDE.md) - Complete guide for Prometheus & Grafana
- [API Docs](http://localhost:8000/docs) - Interactive API documentation (when running)
- [Prometheus UI](http://localhost:9090) - Query metrics directly
- [Grafana Dashboards](http://localhost:3000) - Visual metrics dashboard

## 🔧 Useful Commands

```bash
# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Rebuild after dependency changes
docker-compose up -d --build

# Access database
docker exec -it ih-postgres psql -U postgres -d insighthub
```

## 🧪 API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics endpoint
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

## 📝 License

[Your License Here]