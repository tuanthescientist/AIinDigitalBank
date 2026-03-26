# Setup & Installation Guide

## System Requirements

- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.9 or higher
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 50GB free space
- **Database**: PostgreSQL 12+

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/tuanthescientist/AIinDigitalBank.git
cd AIinDigitalBank
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
# Edit .env
```

**Example .env:**
```
DATABASE_URL=postgresql://user:password@localhost:5432/aiidigitalbank
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
DEBUG=False
ENVIRONMENT=development
```

### 5. Database Setup

```bash
# Create database
createdb aiidigitalbank

# Run migrations
alembic upgrade head

# Load sample data (optional)
python src/data/load_sample_data.py
```

### 6. Run Application

```bash
# Development server
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Production server
gunicorn -w 4 -b 0.0.0.0:8000 src.api.main:app
```

### 7. Access Application

- **API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## Docker Setup

### Build Docker Image
```bash
docker build -t aiidigitalbank:latest .
```

### Run with Docker Compose
```bash
docker-compose up -d
```

Includes:
- FastAPI application
- PostgreSQL database
- Redis cache
- Jupyter notebook

---

## Development Setup

### Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

### Run Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html

# Specific test file
pytest tests/test_models.py -v
```

### Code Quality Tools

```bash
# Format code
black src/

# Lint
flake8 src/

# Type checking
mypy src/

# All checks
make lint
```

### Jupyter Notebooks

```bash
jupyter notebook notebooks/
```

---

## Configuration

### Production Configuration

**Environment Variables:**
```
DATABASE_URL=postgresql://prod-user:pwd@prod-db:5432/aiidigitalbank
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=INFO
```

### Monitoring Setup

#### Prometheus
```
http://localhost:9090
```

#### Grafana
```
http://localhost:3000
```

---

## Troubleshooting

### Port Already in Use
```bash
# Change port in uvicorn command
uvicorn src.api.main:app --port 8001
```

### Database Connection Error
```bash
# Check PostgreSQL is running
psql -U postgres

# Verify DATABASE_URL in .env
```

### Import Errors
```bash
# Reinstall dependencies
pip install --no-cache-dir -r requirements.txt
```

---

## Next Steps

1. Read [THESIS.md](../docs/THESIS.md) for project overview
2. Review [ARCHITECTURE.md](../docs/ARCHITECTURE.md) for system design
3. Explore [notebooks](../notebooks/) for examples
4. Check [API_DOCUMENTATION.md](../docs/API_DOCUMENTATION.md) for API details

---

## Support

- **Issues**: https://github.com/tuanthescientist/AIinDigitalBank/issues
- **Email**: tuantranscientist@gmail.com
- **Name**: Tuan Tran

---

## Version: 1.0
**Last Updated**: March 2026
