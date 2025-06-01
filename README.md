# Dcerno VHD Camera Tracking API

## Tổng quan dự án

**Dcerno VHD Camera Tracking API** là một hệ thống tích hợp giữa hệ thống micro Dcerno và camera VHD, cho phép tự động điều khiển camera theo microphone đang hoạt động.

### Chức năng chính:
- **API RESTful**: Cung cấp các endpoint để quản lý camera và microphone
- **Auto Camera Tracking**: Tự động điều khiển camera theo microphone đang hoạt động
- **Real-time Monitoring**: Theo dõi trạng thái microphone và camera trong thời gian thực
- **Configuration Management**: Quản lý cấu hình mapping giữa microphone và camera

### Kiến trúc hệ thống:
- **FastAPI**: Web framework chính
- **MongoDB**: Database lưu trữ dữ liệu
- **Redis**: Cache và message broker
- **Celery**: Background task processing
- **Docker**: Containerization

## 📚 Documentation

### Quick Start
- [**QUICKSTART.md**](QUICKSTART.md) - Hướng dẫn bắt đầu nhanh (5 phút)

### Detailed Guides
- [**DEVELOPMENT.md**](DEVELOPMENT.md) - Hướng dẫn phát triển chi tiết
- [**API.md**](API.md) - API documentation với examples

### Setup & Configuration
- **README.md** (file này) - Tổng quan và hướng dẫn cơ bản
- `setup.py` - Script tự động setup môi trường development

## 🚀 Quick Setup

```bash
# 1. Clone và setup
git clone <repository-url>
cd dcerno_vhd_api
python setup.py

# 2. Start với Docker
docker-compose up -d

# 3. Test API
curl http://localhost:5000/v1/ping
```

**🔗 Chi tiết:** Xem [QUICKSTART.md](QUICKSTART.md)

## Cấu trúc thư mục

```
dcerno_vhd_api/
├── src/                      # Source code chính
│   ├── api/                  # API routes và endpoints
│   │   └── v1/              # API version 1
│   │       └── routes/      # Các route định nghĩa
│   │           ├── cameras/ # Camera management endpoints
│   │           ├── microphones/ # Microphone management endpoints
│   │           ├── settings/ # Configuration endpoints
│   │           ├── health_check/ # Health check endpoints
│   │           └── ping/    # Ping endpoints
│   ├── clients/             # External service clients
│   │   ├── dcerno.py       # Dcerno system client
│   │   └── vhd.py          # VHD camera client
│   ├── models/             # Data models
│   ├── services/           # Business logic services
│   ├── bases/              # Base classes và utilities
│   ├── workers/            # Celery workers
│   ├── cronjobs/          # Scheduled tasks
│   ├── databases/         # Database configurations
│   ├── common/            # Common utilities
│   └── core/              # Core functionality
├── migration/             # Database migrations
├── config.py             # Application configuration
├── schedule_tracking.py  # Background tracking script
├── setup.py              # Development setup script
├── pyproject.toml       # Poetry dependency management
├── docker-compose.yml   # Docker services configuration
├── Dockerfile          # Docker image configuration
├── env.yaml            # Environment configuration file
└── docs/               # Documentation files
    ├── QUICKSTART.md   # Quick start guide
    ├── DEVELOPMENT.md  # Development guide
    └── API.md         # API documentation
```

## Yêu cầu hệ thống

- **Python**: >= 3.10
- **Poetry**: >= 1.0.0
- **Docker**: >= 20.0.0 (optional)
- **MongoDB**: >= 5.0
- **Redis**: >= 6.0

## Cài đặt và chạy ứng dụng

### 1. Automated Setup (Recommended)

```bash
git clone <repository-url>
cd dcerno_vhd_api
python setup.py
```

Setup script sẽ:
- Kiểm tra system requirements
- Tạo file cấu hình mẫu
- Cài đặt dependencies
- Hướng dẫn next steps

### 2. Manual Setup

#### Clone repository
```bash
git clone <repository-url>
cd dcerno_vhd_api
```

#### Cài đặt dependencies
```bash
# Cài đặt Poetry (nếu chưa có)
curl -sSL https://install.python-poetry.org | python3 -

# Cài đặt dependencies
poetry install
```

#### Cấu hình environment
Tạo file `env.yaml` trong thư mục gốc với nội dung:

```yaml
ENVIRONMENT: "development"
DEBUG: true
SECRET_KEY: "your-secret-key"
VERSION: "v1"

# Database Configuration
MONGO_URI: "mongodb://localhost:27017"
MONGO_DB_NAME: "camera_tracking"

# Redis Configuration
REDIS:
  password: "813417"
  host: "localhost"
  port: 6379

# Dcerno Configuration
DCERNO_CONFIG:
  host: "192.168.0.20"
  port: 5011

# VHD Camera Configuration
VHD_CONFIG:
  ips:
    - "http://192.168.0.88"

# File paths for configuration
DECERNO_VHD_MAPPING_PATH: "/path/to/decerno_vhd_camera_config.json"
DECERNO_VHD_SETTING_PATH: "/path/to/decerno_vhd_settings.json"

# Optional: Sentry DNS for error tracking
SENTRY_DNS: ""
```

### 3. Khởi động services

#### Docker (Recommended)
```bash
# Khởi động tất cả services
docker-compose up -d

# Xem logs
docker-compose logs -f

# Dừng services
docker-compose down
```

#### Manual (Local development)
```bash
# Khởi động MongoDB và Redis trước:
# MongoDB
mongod --dbpath /path/to/your/db

# Redis
redis-server --requirepass 813417

# Chạy API server:
poetry run uvicorn src.api:app --host=0.0.0.0 --port=5000 --reload

# Chạy background tracking script:
poetry run python schedule_tracking.py
```

## API Endpoints

### Base URL
```
http://localhost:5000/v1
```

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ping` | Test API connection |
| GET | `/health-check` | Check API health |
| GET | `/cameras` | List all cameras |
| GET | `/cameras/ping?ip=<ip>` | Ping specific camera |
| GET | `/microphones` | Get microphone status |
| POST | `/microphones/call` | Call microphone preset |
| POST | `/microphones/preset` | Set camera preset |
| GET | `/tracking` | Get tracking settings |
| POST | `/tracking` | Update tracking settings |

**🔗 Chi tiết:** Xem [API.md](API.md) để có full documentation và examples

## Cấu hình hệ thống

### 1. Mapping Configuration

File `decerno_vhd_camera_config.json` định nghĩa mapping giữa microphone và camera:

```json
{
  "microphone_uid_1": {
    "camera_ip": "192.168.0.88",
    "number": "1",
    "micro_id": "microphone_uid_1"
  },
  "microphone_uid_2": {
    "camera_ip": "192.168.0.89", 
    "number": "2",
    "micro_id": "microphone_uid_2"
  }
}
```

### 2. Tracking Settings

File `decerno_vhd_settings.json` định nghĩa camera nào được bật auto-tracking:

```json
{
  "192.168.0.88": true,
  "192.168.0.89": false
}
```

## Development

### Quick Development Workflow

```bash
# Add new API endpoint
mkdir src/api/v1/routes/my_feature
# Create __init__.py and logic_handlers.py

# Format code
poetry run black src/

# Test API
curl http://localhost:5000/v1/my-endpoint

# Check logs
docker-compose logs -f app
```

**🔗 Chi tiết:** Xem [DEVELOPMENT.md](DEVELOPMENT.md) để có hướng dẫn phát triển đầy đủ

### Testing

```bash
# Chạy tests
poetry run pytest

# Coverage report
poetry run pytest --cov=src
```

### Code Style

```bash
# Format code
poetry run black src/

# Check formatting
poetry run black --check src/
```

## Monitoring và Logging

### Logs
```bash
# Docker logs
docker-compose logs -f app
docker-compose logs -f schedule_tracking

# Check specific service
docker-compose logs -f <service_name>
```

### Health Monitoring
- API health check: `GET /health-check`
- Camera ping: `GET /cameras/ping?ip=<camera_ip>`
- Microphone status qua Dcerno client

## Troubleshooting

### Quick Fixes
```bash
# Reset everything
docker-compose down && docker-compose up -d

# Recreate config files
python setup.py

# Check service status
docker-compose ps
```

### Common Issues
- **Connection issues**: Check IP/port configurations
- **Config file errors**: Validate JSON format
- **Port conflicts**: Ensure port 5000 is free

**🔗 Chi tiết:** Xem troubleshooting section trong [README.md](README.md)

## Production Deployment

### Environment Variables
Set production values trong `env.yaml`:
```yaml
ENVIRONMENT: "production"
DEBUG: false
# Update all database and service URLs
```

### Docker Production
```bash
# Build production image
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

## Contributing

1. Fork repository
2. Tạo feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -am 'Add some feature'`
4. Push branch: `git push origin feature/your-feature`
5. Submit Pull Request

**Development guidelines:** Xem [DEVELOPMENT.md](DEVELOPMENT.md)


## Support

### Documentation
- [Quick Start Guide](QUICKSTART.md)
- [Development Guide](DEVELOPMENT.md)
- [API Documentation](API.md)

---

**🎯 New to this project?** Start with [QUICKSTART.md](QUICKSTART.md) for a 5-minute setup guide!