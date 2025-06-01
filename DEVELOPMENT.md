# Development Guide - Dcerno VHD API

## Hướng dẫn phát triển chi tiết

### 1. Hiểu về Architecture

#### Application Flow
```
1. FastAPI nhận HTTP requests
2. Routes định tuyến đến Logic Handlers  
3. Logic Handlers xử lý business logic
4. Clients tương tác với external services (Dcerno, VHD)
5. Background script (`schedule_tracking.py`) chạy real-time monitoring
```

#### Key Components

**API Layer (`src/api/`)**
- `__init__.py`: Main app initialization với ApiGenerator
- `v1/`: API version 1 routes
- Routes được auto-discover từ `routes/` directory

**Business Logic (`src/api/v1/routes/*/logic_handlers.py`)**
- Mỗi endpoint có một LogicHandler class
- Kế thừa từ `src.bases.api.logic_handlers.LogicHandler`
- Handle method chứa business logic chính

**External Clients (`src/clients/`)**
- `dcerno.py`: Tương tác với Dcerno microphone system qua TCP/IP
- `vhd.py`: Điều khiển VHD cameras qua HTTP API

**Configuration (`config.py`)**
- Load config từ `env.yaml`
- Provide config objects cho các components

### 2. Code Structure Deep Dive

#### Adding New API Endpoint

**Step 1: Create Route Directory**
```bash
mkdir src/api/v1/routes/your_feature
cd src/api/v1/routes/your_feature
```

**Step 2: Create Route Definition (`__init__.py`)**
```python
from src.bases.api.routes import Route
from .logic_handlers import YourLogicHandler

class YourRoute(Route):
    auth = False                    # Set True nếu cần authentication
    path = "/your-endpoint"         # URL path
    method = "get"                  # HTTP method: get, post, put, delete
    logic_handler_class = YourLogicHandler

# Multiple routes trong cùng 1 file
class YourPostRoute(Route):
    auth = False
    path = "/your-endpoint"
    method = "post"
    logic_handler_class = YourPostLogicHandler
```

**Step 3: Create Logic Handler (`logic_handlers.py`)**
```python
from src.bases.api.logic_handlers import LogicHandler
from src.clients.dcerno import DcernoClient
from src.clients.vhd import VHDClient
from config import DCERNO_CONFIG, VHD_CONFIG

class YourLogicHandler(LogicHandler):
    def handle(self):
        # Access request data
        query_params = self.request_dto.args
        body_data = self.request_dto.json
        
        # Business logic
        result = self.process_business_logic()
        
        # Return response
        return {
            "message": "Success",
            "data": result
        }
    
    def process_business_logic(self):
        # Example: Interact with Dcerno
        dcerno_client = DcernoClient(
            host=DCERNO_CONFIG['host'],
            port=DCERNO_CONFIG['port']
        )
        
        # Example: Get microphone data
        micros = dcerno_client.get_all_units()
        
        return micros
```

#### Working with Clients

**Dcerno Client Usage:**
```python
from src.clients.dcerno import DcernoClient
from config import DCERNO_CONFIG

# Initialize client
client = DcernoClient(
    host=DCERNO_CONFIG['host'],
    port=DCERNO_CONFIG['port'],
    timeout=5
)

# Get all microphones
units = client.get_all_units()
# Returns: {"nam": "units", "s": [{"uid": "123", "stat": "1"}, ...]}

# Get specific microphone status  
status = client.get_microphone_status(uid="123")
```

**VHD Client Usage:**
```python
from src.clients.vhd import VHDClient

# Initialize client
camera = VHDClient(uri="192.168.0.88", logger=logger)

# Move camera to preset position
camera.call(action="poscall", position="1")

# Move camera to home position
camera.call(action="home", position="10", zoom="10")

# Ping camera
response = camera.ping()
```

### 3. Configuration Management

#### Environment Configuration (`env.yaml`)
```yaml
# Development
ENVIRONMENT: "development"
DEBUG: true

# Production  
ENVIRONMENT: "production"
DEBUG: false
```

#### Adding New Config
1. Thêm vào `env.yaml`:
```yaml
YOUR_NEW_CONFIG:
  setting1: "value1"
  setting2: "value2"
```

2. Thêm vào `config.py`:
```python
YOUR_NEW_CONFIG = data.get('YOUR_NEW_CONFIG', dict(
    setting1='default_value1',
    setting2='default_value2'
))
```

3. Sử dụng trong code:
```python
from config import YOUR_NEW_CONFIG

value = YOUR_NEW_CONFIG['setting1']
```

### 4. Background Processing

#### Schedule Tracking Script
File `schedule_tracking.py` chạy background monitoring:

**Main Flow:**
1. Kết nối Dcerno client để get active microphones
2. Đọc mapping config từ JSON file
3. Đọc tracking settings từ JSON file  
4. Auto điều khiển camera dựa trên microphone active
5. Loop liên tục với delay 0.5s

**Key Functions:**
- Monitor active microphones từ Dcerno
- Map microphone → camera theo config
- Auto call camera presets
- Handle camera home position khi microphone inactive

### 5. Database Integration

#### MongoDB (Optional - hiện tại chưa dùng)
Cấu hình đã có sẵn nhưng chưa được sử dụng:
```python
# Trong src/api/__init__.py
generator = ApiGenerator(
    # mongo_config=MONGO_URI,  # Commented out
    router_modules=[v1],
    redis_config=REDIS,
    # ...
)
```

#### Redis Integration
Được cấu hình để dùng với Celery và caching:
```python
from config import REDIS

# Redis config format
REDIS = {
    'password': '813417',
    'host': 'localhost', 
    'port': 6379,
}
```

### 6. Error Handling

#### Client Errors
```python
from src.bases.error.client import ClientError

try:
    result = dcerno_client.get_all_units()
except ClientError as e:
    # Handle client-specific errors
    print(f"Client error: {e.message}")
    print(f"Meta info: {e.meta}")
```

#### API Error Response
```python
class YourLogicHandler(LogicHandler):
    def handle(self):
        try:
            # Your logic
            return {"success": True, "data": result}
        except Exception as e:
            # Return error response
            return {
                "success": False,
                "message": str(e),
                "errors": [str(e)]
            }
```

### 7. Testing Strategy

#### Unit Tests
```python
# tests/test_logic_handlers.py
import pytest
from src.api.v1.routes.your_feature.logic_handlers import YourLogicHandler

class TestYourLogicHandler:
    def test_handle_success(self):
        handler = YourLogicHandler()
        # Mock request_dto
        handler.request_dto = MockRequestDto()
        
        result = handler.handle()
        assert result["success"] == True
```

#### Integration Tests  
```python
# tests/test_clients.py
import pytest
from src.clients.dcerno import DcernoClient

class TestDcernoClient:
    def test_get_all_units(self):
        client = DcernoClient("localhost", 5011)
        units = client.get_all_units()
        assert "s" in units
```

#### API Tests
```python
# tests/test_api.py
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

def test_ping():
    response = client.get("/v1/ping")
    assert response.status_code == 200
```

### 8. Deployment Practices

#### Development
```bash
# Local development với hot reload
poetry run uvicorn src.api:app --host=0.0.0.0 --port=5000 --reload

# Background script
poetry run python schedule_tracking.py
```

#### Docker Development
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f app
docker-compose logs -f schedule_tracking

# Restart specific service
docker-compose restart app
```

#### Production Considerations
1. **Logging**: Configure proper log levels
2. **Error Tracking**: Set up Sentry DSN
3. **Health Checks**: Implement proper health checks
4. **Monitoring**: Monitor Dcerno/VHD connections
5. **Performance**: Tune socket timeouts và connection pools

### 9. Common Development Tasks

#### Debug Connection Issues
```python
# Test Dcerno connection
from src.clients.dcerno import DcernoClient
client = DcernoClient("192.168.0.20", 5011, timeout=5)
try:
    units = client.get_all_units()
    print("Dcerno connected:", units)
except Exception as e:
    print("Dcerno error:", e)

# Test VHD camera
from src.clients.vhd import VHDClient
camera = VHDClient(uri="192.168.0.88", logger=None)
try:
    result = camera.ping()
    print("Camera connected:", result)
except Exception as e:
    print("Camera error:", e)
```

#### Update Configuration Files
```python
import json

# Update mapping config
mapping = {
    "micro_123": {
        "camera_ip": "192.168.0.88",
        "number": "1", 
        "micro_id": "micro_123"
    }
}
with open("decerno_vhd_camera_config.json", "w") as f:
    json.dump(mapping, f, indent=2)

# Update tracking settings
settings = {
    "192.168.0.88": True,
    "192.168.0.89": False
}
with open("decerno_vhd_settings.json", "w") as f:
    json.dump(settings, f, indent=2)
```

### 10. Best Practices

#### Code Style
- Follow PEP 8
- Use type hints where possible
- Add docstrings for complex functions
- Keep functions small and focused

#### Error Handling
- Always handle client connection errors
- Provide meaningful error messages
- Log errors properly for debugging

#### Performance
- Use connection pooling cho external services
- Cache frequently accessed data
- Optimize polling intervals trong background script

#### Security
- Validate all input data
- Use environment variables cho sensitive config
- Implement proper authentication nếu cần

#### Monitoring
- Add logging cho important events
- Monitor external service availability
- Track performance metrics 