# API Documentation - Dcerno VHD Camera Tracking

## Overview

API này cung cấp các endpoint để quản lý và theo dõi hệ thống camera VHD dựa trên microphone Dcerno. Tất cả endpoints đều trả về JSON response với format chuẩn.

**Base URL**: `http://localhost:5000/v1`

## Authentication

Hiện tại tất cả endpoints đều không yêu cầu authentication (`auth = False`). Trong production có thể cần thêm authentication middleware.

## Response Format

### Success Response
```json
{
  "success": true,
  "data": {...},
  "message": "Success message",
  "errors": null
}
```

### Error Response
```json
{
  "success": false,
  "data": null,
  "message": "Error message",
  "errors": ["Error detail 1", "Error detail 2"]
}
```

## Endpoints

### 1. Health Check

#### `GET /health-check`

Kiểm tra trạng thái của API server.

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2023-12-01T10:30:00Z"
  },
  "message": "API is running",
  "errors": null
}
```

### 2. Ping

#### `GET /ping`

Ping đơn giản để kiểm tra kết nối API.

**Response:**
```json
{
  "success": true,
  "data": "pong",
  "message": "Ping successful",
  "errors": null
}
```

### 3. Camera Management

#### `GET /cameras`

Lấy danh sách tất cả cameras trong hệ thống.

**Response:**
```json
{
  "success": true,
  "data": {
    "cameras": [
      {
        "ip": "192.168.0.88",
        "status": "online",
        "model": "VHD"
      },
      {
        "ip": "192.168.0.89", 
        "status": "offline",
        "model": "VHD"
      }
    ]
  },
  "message": "Cameras retrieved successfully",
  "errors": null
}
```

#### `GET /cameras/ping`

Ping một camera cụ thể để kiểm tra kết nối.

**Query Parameters:**
- `ip` (required): IP address của camera

**Example Request:**
```
GET /cameras/ping?ip=192.168.0.88
```

**Response:**
```json
{
  "success": true,
  "data": {
    "ip": "192.168.0.88",
    "status": "online",
    "response_time": "120ms",
    "device_info": "VHD Camera Model X"
  },
  "message": "Camera ping successful",
  "errors": null
}
```

**Error Response:**
```json
{
  "success": false,
  "data": null,
  "message": "Camera ping failed",
  "errors": ["Connection timeout", "Camera not responding"]
}
```

### 4. Microphone Management

#### `GET /microphones`

Lấy thông tin về microphone(s) từ hệ thống Dcerno.

**Query Parameters:**
- `uid` (optional): UID của microphone cụ thể

**Example Request:**
```
GET /microphones?uid=12345
```

**Response:**
```json
{
  "success": true,
  "data": {
    "microphones": [
      {
        "uid": "12345",
        "status": "active",
        "name": "Microphone 1",
        "position": "1"
      }
    ]
  },
  "message": "Microphones retrieved successfully",
  "errors": null
}
```

**Get All Microphones:**
```
GET /microphones
```

**Response:**
```json
{
  "success": true,
  "data": {
    "microphones": [
      {
        "uid": "12345",
        "status": "active",
        "name": "Microphone 1"
      },
      {
        "uid": "67890",
        "status": "inactive", 
        "name": "Microphone 2"
      }
    ]
  },
  "message": "All microphones retrieved",
  "errors": null
}
```

#### `POST /microphones/call`

Gọi preset position cho microphone (điều khiển camera theo microphone).

**Request Body:**
```json
{
  "uid": "12345",
  "position": "1"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "uid": "12345",
    "position": "1",
    "camera_ip": "192.168.0.88",
    "action": "preset_called"
  },
  "message": "Microphone preset called successfully",
  "errors": null
}
```

**Error Response:**
```json
{
  "success": false,
  "data": null,
  "message": "Failed to call microphone preset",
  "errors": ["Microphone not found", "Camera not responding"]
}
```

#### `POST /microphones/preset`

Set/configure camera preset cho một microphone.

**Request Body:**
```json
{
  "uid": "12345",
  "camera_ip": "192.168.0.88",
  "position": "1"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "uid": "12345",
    "camera_ip": "192.168.0.88",
    "position": "1",
    "configured": true
  },
  "message": "Camera preset configured successfully",
  "errors": null
}
```

#### `GET /microphones/details`

Lấy thông tin chi tiết về microphone từ Dcerno system.

**Query Parameters:**
- `uid` (required): UID của microphone

**Example Request:**
```
GET /microphones/details?uid=12345
```

**Response:**
```json
{
  "success": true,
  "data": {
    "uid": "12345",
    "name": "Conference Room Mic 1",
    "status": "active",
    "battery_level": "85%",
    "signal_strength": "Strong",
    "last_active": "2023-12-01T10:25:00Z",
    "mapped_camera": {
      "ip": "192.168.0.88",
      "position": "1"
    }
  },
  "message": "Microphone details retrieved",
  "errors": null
}
```

### 5. Settings Management

#### `GET /tracking`

Lấy cấu hình tracking hiện tại (cameras nào được bật auto-tracking).

**Response:**
```json
{
  "success": true,
  "data": {
    "tracking_settings": {
      "192.168.0.88": true,
      "192.168.0.89": false,
      "192.168.0.90": true
    },
    "updated_at": "2023-12-01T09:00:00Z"
  },
  "message": "Tracking settings retrieved",
  "errors": null
}
```

#### `POST /tracking`

Cập nhật cấu hình tracking (bật/tắt auto-tracking cho cameras).

**Request Body:**
```json
{
  "192.168.0.88": true,
  "192.168.0.89": false,
  "192.168.0.90": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "tracking_settings": {
      "192.168.0.88": true,
      "192.168.0.89": false,
      "192.168.0.90": true
    },
    "updated_at": "2023-12-01T10:30:00Z"
  },
  "message": "Tracking settings updated successfully",
  "errors": null
}
```

## Error Codes

### Common HTTP Status Codes

- `200` - Success
- `400` - Bad Request (Invalid parameters)
- `404` - Not Found (Resource not found)
- `500` - Internal Server Error
- `503` - Service Unavailable (External service down)

### Custom Error Types

#### Connection Errors
```json
{
  "success": false,
  "data": null,
  "message": "Connection failed",
  "errors": ["Dcerno system not responding", "Check network connection"]
}
```

#### Validation Errors
```json
{
  "success": false,
  "data": null,
  "message": "Validation failed",
  "errors": ["UID is required", "Invalid camera IP format"]
}
```

#### Configuration Errors
```json
{
  "success": false,
  "data": null,
  "message": "Configuration error",
  "errors": ["Mapping file not found", "Invalid JSON format"]
}
```

## Rate Limiting

Hiện tại không có rate limiting, nhưng khuyến nghị:
- Maximum 100 requests/minute cho mỗi client
- Background tracking polling mỗi 0.5 giây

## Examples

### Python Client Example

```python
import requests

base_url = "http://localhost:5000/v1"

# Check API health
response = requests.get(f"{base_url}/health-check")
print(response.json())

# Get all microphones
response = requests.get(f"{base_url}/microphones")
microphones = response.json()['data']['microphones']

# Call preset for active microphone
for mic in microphones:
    if mic['status'] == 'active':
        payload = {
            "uid": mic['uid'],
            "position": "1"
        }
        response = requests.post(f"{base_url}/microphones/call", json=payload)
        print(f"Called preset for {mic['uid']}: {response.json()}")

# Update tracking settings
tracking_config = {
    "192.168.0.88": True,
    "192.168.0.89": False
}
response = requests.post(f"{base_url}/tracking", json=tracking_config)
print(f"Tracking updated: {response.json()}")
```

### cURL Examples

```bash
# Health check
curl -X GET http://localhost:5000/v1/health-check

# Ping camera
curl -X GET "http://localhost:5000/v1/cameras/ping?ip=192.168.0.88"

# Get microphones
curl -X GET http://localhost:5000/v1/microphones

# Call microphone preset
curl -X POST http://localhost:5000/v1/microphones/call \
  -H "Content-Type: application/json" \
  -d '{"uid": "12345", "position": "1"}'

# Update tracking settings
curl -X POST http://localhost:5000/v1/tracking \
  -H "Content-Type: application/json" \
  -d '{"192.168.0.88": true, "192.168.0.89": false}'
```

### JavaScript/Fetch Example

```javascript
const baseUrl = 'http://localhost:5000/v1';

// Get tracking settings
async function getTrackingSettings() {
  try {
    const response = await fetch(`${baseUrl}/tracking`);
    const data = await response.json();
    
    if (data.success) {
      console.log('Tracking settings:', data.data.tracking_settings);
    } else {
      console.error('Error:', data.message);
    }
  } catch (error) {
    console.error('Network error:', error);
  }
}

// Call microphone preset
async function callMicrophonePreset(uid, position) {
  try {
    const response = await fetch(`${baseUrl}/microphones/call`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ uid, position })
    });
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error calling preset:', error);
    return { success: false, message: error.message };
  }
}
```

## Monitoring

### Health Check Endpoint

Sử dụng `/health-check` endpoint để monitor:
- API server status
- Database connections (nếu có)
- External service connections

### Logging

API tự động log:
- Request/response times
- Error occurrences
- External service calls
- Configuration changes

Check logs với:
```bash
# Docker logs
docker-compose logs -f app

# Local logs
tail -f logs/api.log
```

### Metrics

Key metrics để monitor:
- Response times
- Error rates
- External service availability
- Active microphone count
- Camera response times 