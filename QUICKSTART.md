# Quick Start Guide - Dcerno VHD API

## 🚀 Quick Setup (5 minutes)

### 1. Prerequisites
Đảm bảo bạn có:
- Python 3.10+
- Poetry
- Docker (optional)

### 2. Setup dự án
```bash
# Clone project
git clone <repository-url>
cd dcerno_vhd_api

# Run setup script
python setup.py
```

### 3. Start development
```bash
# Option 1: Docker (Recommended)
docker-compose up -d

# Option 2: Local development
poetry run uvicorn src.api:app --host=0.0.0.0 --port=5000 --reload
# In another terminal:
poetry run python schedule_tracking.py
```

### 4. Test API
```bash
curl http://localhost:5000/v1/ping
# Should return: {"success": true, "data": "pong", ...}
```

## 📝 Quick Configuration

### 1. Update env.yaml
```yaml
DCERNO_CONFIG:
  host: "YOUR_DCERNO_IP"  # e.g. "192.168.1.100"
  port: 5011

VHD_CONFIG:
  ips:
    - "http://YOUR_CAMERA_IP"  # e.g. "http://192.168.1.88"
```

### 2. Configure mapping (~/Documents/decerno_vhd_camera_config.json)
```json
{
  "microphone_uid_123": {
    "camera_ip": "192.168.1.88",
    "number": "1",
    "micro_id": "microphone_uid_123"
  }
}
```

### 3. Enable tracking (~/Documents/decerno_vhd_settings.json)
```json
{
  "192.168.1.88": true
}
```

## 🧪 Test the System

### 1. Test connections
```bash
# Test API
curl http://localhost:5000/v1/health-check

# Test camera ping
curl "http://localhost:5000/v1/cameras/ping?ip=192.168.1.88"

# Test microphones
curl http://localhost:5000/v1/microphones
```

### 2. Test camera control
```bash
curl -X POST http://localhost:5000/v1/microphones/call \
  -H "Content-Type: application/json" \
  -d '{"uid": "microphone_uid_123", "position": "1"}'
```

### 3. Check auto tracking
- Background script should automatically move cameras when microphones are active
- Check logs: `docker-compose logs -f schedule_tracking`

## 🔧 Development Workflow

### Adding new endpoint
1. Create directory: `src/api/v1/routes/my_feature/`
2. Create `__init__.py`:
```python
from src.bases.api.routes import Route
from .logic_handlers import MyLogicHandler

class MyRoute(Route):
    auth = False
    path = "/my-endpoint"
    method = "get"
    logic_handler_class = MyLogicHandler
```
3. Create `logic_handlers.py`:
```python
from src.bases.api.logic_handlers import LogicHandler

class MyLogicHandler(LogicHandler):
    def handle(self):
        return {"message": "Hello World"}
```

### Common tasks
```bash
# Format code
poetry run black src/

# Run tests
poetry run pytest

# Check logs
docker-compose logs -f app

# Restart services
docker-compose restart app
```

## 🐛 Quick Troubleshooting

### Connection Issues
- **Dcerno not connecting**: Check IP/port in env.yaml
- **Camera not responding**: Ping camera first
- **API not starting**: Check port 5000 is free

### Configuration Issues
- **Files not found**: Check ~/Documents/ has config files
- **Invalid JSON**: Validate JSON format
- **Wrong paths**: Check DECERNO_VHD_*_PATH in env.yaml

### Quick fixes
```bash
# Reset containers
docker-compose down && docker-compose up -d

# Recreate config files
python setup.py

# Check service status
docker-compose ps
```

## 📚 Next Steps

1. **Read full documentation**:
   - README.md - Complete setup guide
   - DEVELOPMENT.md - Development details
   - API.md - API documentation

2. **Explore the code**:
   - `src/clients/` - External integrations
   - `src/api/v1/routes/` - API endpoints
   - `schedule_tracking.py` - Background tracking

3. **Customize for your needs**:
   - Add authentication
   - Extend API endpoints
   - Improve error handling
   - Add monitoring

## 🆘 Need Help?

- Check logs: `docker-compose logs -f`
- Review configuration files
- Test connections individually
- Read error messages carefully

## 🎯 Key Files to Know

- `config.py` - Configuration loading
- `src/api/__init__.py` - API initialization
- `src/clients/dcerno.py` - Dcerno integration
- `src/clients/vhd.py` - VHD camera control
- `schedule_tracking.py` - Auto tracking logic 