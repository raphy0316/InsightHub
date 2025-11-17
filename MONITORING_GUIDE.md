# Monitoring Guide - Prometheus & Grafana

This guide explains how to use the monitoring stack for InsightHub.

## 🚀 Quick Start

### 1. Start the Stack

```bash
cd infra
docker-compose up -d
```

This starts:
- **API** (port 8000) - with `/metrics` endpoint
- **Prometheus** (port 9090) - metrics collection
- **Grafana** (port 3000) - visualization
- **PostgreSQL** (port 5432) - database

### 2. Access the Services

- **Grafana**: http://localhost:3000 (login: admin/admin)
- **Prometheus**: http://localhost:9090
- **API Metrics**: http://localhost:8000/metrics

## 📊 Using Grafana

### First Login

1. Open http://localhost:3000
2. Login with: `admin` / `admin`
3. You'll see the pre-configured "InsightHub API Metrics" dashboard

### Pre-configured Dashboard

The dashboard includes:
- **Request Rate**: Requests per second over time
- **Total Requests**: Cumulative request count
- **Request Duration**: p50 and p95 latency
- **Status Codes**: Distribution by HTTP status

### Creating Custom Dashboards

1. Click "+" → "Dashboard" → "Add visualization"
2. Select "Prometheus" as datasource
3. Enter a PromQL query (see examples below)
4. Customize the visualization
5. Save the dashboard

## 🔍 Prometheus Queries (PromQL)

### Basic Queries

```promql
# Current request rate
rate(http_requests_total[1m])

# Total requests
sum(http_requests_total)

# Requests by endpoint
sum by (endpoint) (http_requests_total)

# Requests by status code
sum by (status) (http_requests_total)

# Error rate (5xx responses)
sum(rate(http_requests_total{status=~"5.."}[1m]))

# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Average latency
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])
```

### Advanced Queries

```promql
# Request rate per endpoint
sum by (endpoint) (rate(http_requests_total[1m]))

# Success rate (2xx/3xx)
sum(rate(http_requests_total{status=~"[23].."}[1m])) 
/ 
sum(rate(http_requests_total[1m]))

# Error rate percentage
100 * sum(rate(http_requests_total{status=~"[45].."}[1m])) 
/ 
sum(rate(http_requests_total[1m]))

# Requests per minute by method
sum by (method) (increase(http_requests_total[1m]))
```

## 📈 Custom Metrics

### Adding Custom Metrics to Your API

Edit `apps/api/app/main.py`:

```python
from prometheus_client import Counter, Gauge, Histogram

# Example: Track user signups
user_signups = Counter('user_signups_total', 'Total user signups')

# Example: Track active connections
active_connections = Gauge('active_connections', 'Number of active connections')

# Example: Track database query time
db_query_duration = Histogram(
    'db_query_duration_seconds',
    'Database query duration',
    ['query_type']
)

# In your route:
@app.post("/signup")
def signup():
    user_signups.inc()  # Increment counter
    # ... signup logic
    return {"status": "success"}

@app.get("/data")
def get_data():
    with db_query_duration.labels(query_type='select').time():
        # ... database query
        pass
    return {"data": "..."}
```

### Metric Types

1. **Counter**: Monotonically increasing value (requests, errors)
2. **Gauge**: Value that can go up or down (memory, connections)
3. **Histogram**: Observations with buckets (latency, size)
4. **Summary**: Similar to histogram but with quantiles

## 🎯 Monitoring Best Practices

### What to Monitor

**API Health**
- Request rate
- Error rate
- Response time (p50, p95, p99)
- Status code distribution

**Resource Usage**
- Memory usage
- CPU usage
- Database connections
- Disk I/O

**Business Metrics**
- User signups
- API key usage
- Feature usage
- Model predictions (for ML apps)

### Setting Up Alerts

1. In Grafana, go to Alerting → Alert Rules
2. Create a new alert rule
3. Set conditions (e.g., error rate > 5%)
4. Configure notification channels (email, Slack, etc.)

Example alert: High error rate
```promql
sum(rate(http_requests_total{status=~"5.."}[5m])) > 0.05
```

## 🔧 Configuration

### Prometheus Configuration

Location: `infra/prometheus/prometheus.yml`

```yaml
scrape_configs:
  - job_name: 'insighthub-api'
    scrape_interval: 5s
    static_configs:
      - targets: ['api:8000']
    metrics_path: '/metrics'
```

### Grafana Datasource

Location: `infra/grafana/provisioning/datasources/prometheus.yml`

Prometheus is automatically configured as the default datasource.

## 🐛 Troubleshooting

### Metrics Not Showing in Grafana

1. Check if Prometheus is scraping your API:
   - Open http://localhost:9090/targets
   - Verify "insighthub-api" target is UP

2. Check if metrics are being generated:
   - Visit http://localhost:8000/metrics
   - Make some API requests
   - Refresh and verify metrics appear

3. Check Grafana datasource:
   - Grafana → Configuration → Data Sources
   - Test the Prometheus connection

### Prometheus Not Scraping

```bash
# Check Prometheus logs
docker logs ih-prometheus

# Check API logs
docker logs ih-api

# Verify network connectivity
docker exec ih-prometheus wget -O- http://api:8000/metrics
```

### Grafana Dashboard Not Loading

```bash
# Check Grafana logs
docker logs ih-grafana

# Restart Grafana
docker-compose restart grafana
```

## 📚 Additional Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [PromQL Guide](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/naming/)

## 🎓 Example Use Cases

### Monitor API Performance

Track API endpoint performance to identify slow endpoints:

```promql
# Slowest endpoints by p95 latency
topk(5, histogram_quantile(0.95, 
  sum by (endpoint) (rate(http_request_duration_seconds_bucket[5m]))
))
```

### Monitor Error Rates

Track and alert on error spikes:

```promql
# Errors per minute
sum(rate(http_requests_total{status=~"[45].."}[1m])) * 60
```

### Capacity Planning

Monitor request trends to plan scaling:

```promql
# Requests per hour (hourly average)
sum(rate(http_requests_total[1h])) * 3600
```

### User Activity

Track user engagement:

```python
# Add custom metric
from prometheus_client import Counter

user_logins = Counter('user_logins_total', 'Total user logins')

@app.post("/login")
def login():
    user_logins.inc()
    # ... login logic
```

Query in Grafana:
```promql
increase(user_logins_total[1h])
```

