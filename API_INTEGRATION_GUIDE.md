# VIGIL-GOA-DASH API Integration Guide

## Backend Server Status ✅
**Backend is running at:** `http://localhost:5000`  
**Database:** Connected to Aiven MySQL  
**CORS:** Enabled for localhost:5173, localhost:3000, localhost:5000

---

## Frontend Configuration

### .env File (Already Set Up)
```env
VITE_API_BASE_URL=http://localhost:5000
```

**IMPORTANT:** 
- Do NOT add `/api` to the base URL
- The API client will automatically add `/api` prefix to all endpoints
- Final URLs will be: `http://localhost:5000/api/officers`, `http://localhost:5000/api/duties`, etc.

---

## Available API Endpoints

### 🔓 Public Endpoints (No Authentication Required)

#### Health Check
```http
GET http://localhost:5000/health
```
**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "database": "connected",
    "timestamp": "2025-11-16T17:15:00.000000Z"
  }
}
```

#### Get All Officers
```http
GET http://localhost:5000/officers
```
**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "GP02650",
      "staff_id": "GP02650",
      "staff_name": "Officer Name",
      "staff_designation": "Police Constable",
      "staff_nature_of_work": "Patrol Duty",
      "status": "active",
      "profilepic": "url",
      "created_at": "2025-11-16T...",
      "updated_at": "2025-11-16T..."
    }
  ]
}
```

#### Get Officer by ID
```http
GET http://localhost:5000/officers/{officer_id}
```

---

### 🔐 Protected API Endpoints (Require JWT Authentication)

All endpoints under `/api/*` require JWT token in Authorization header:
```http
Authorization: Bearer YOUR_JWT_TOKEN
```

#### Authentication

**Login / Get OTP**
```http
POST http://localhost:5000/api/auth/login
Content-Type: application/json

{
  "staff_id": "GP02650"
}
```
**Response:**
```json
{
  "success": true,
  "message": "OTP sent successfully",
  "data": {
    "staff_id": "GP02650",
    "otp_expires_at": "2025-11-16T17:20:00Z"
  }
}
```

**Verify OTP**
```http
POST http://localhost:5000/api/auth/verify-otp
Content-Type: application/json

{
  "staff_id": "GP02650",
  "otp": "123456"
}
```
**Response:**
```json
{
  "success": true,
  "data": {
    "token": "eyJhbGc...",
    "officer": {
      "id": "GP02650",
      "staff_name": "Officer Name",
      "staff_designation": "Police Constable"
    }
  }
}
```

---

#### Officers API

**Get All Officers**
```http
GET http://localhost:5000/api/officers
Authorization: Bearer YOUR_JWT_TOKEN
```

**Get Officer by ID**
```http
GET http://localhost:5000/api/officers/{officer_id}
Authorization: Bearer YOUR_JWT_TOKEN
```

**Create Officer**
```http
POST http://localhost:5000/api/officers
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "staff_id": "GP12345",
  "staff_name": "New Officer",
  "staff_designation": "Police Constable",
  "staff_nature_of_work": "Patrol",
  "status": "active"
}
```

**Update Officer**
```http
PUT http://localhost:5000/api/officers/{officer_id}
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "staff_name": "Updated Name",
  "status": "on-duty"
}
```

**Delete Officer**
```http
DELETE http://localhost:5000/api/officers/{officer_id}
Authorization: Bearer YOUR_JWT_TOKEN
```

---

#### Duties API

**Get All Duties**
```http
GET http://localhost:5000/api/duties
Authorization: Bearer YOUR_JWT_TOKEN
```

**Get Duty by ID**
```http
GET http://localhost:5000/api/duties/{duty_id}
Authorization: Bearer YOUR_JWT_TOKEN
```

**Get Officer's Duties**
```http
GET http://localhost:5000/api/duties/officer/{officer_id}
Authorization: Bearer YOUR_JWT_TOKEN
```

**Create Duty**
```http
POST http://localhost:5000/api/duties
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "type": "patrol",
  "location_polygon": {...},
  "start_time": "2025-11-16T09:00:00Z",
  "end_time": "2025-11-16T17:00:00Z",
  "assigned_officers": ["GP02650"],
  "assigned_vehicle": "GV1234"
}
```

**Update Duty**
```http
PUT http://localhost:5000/api/duties/{duty_id}
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "status": "completed",
  "comments": "Duty completed successfully"
}
```

**Delete Duty**
```http
DELETE http://localhost:5000/api/duties/{duty_id}
Authorization: Bearer YOUR_JWT_TOKEN
```

---

#### Vehicles API

**Get All Vehicles**
```http
GET http://localhost:5000/api/vehicles
Authorization: Bearer YOUR_JWT_TOKEN
```

**Get Vehicle by ID**
```http
GET http://localhost:5000/api/vehicles/{vehicle_id}
Authorization: Bearer YOUR_JWT_TOKEN
```

**Create Vehicle**
```http
POST http://localhost:5000/api/vehicles
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "vehicle_name": "Patrol Car",
  "vehicle_number": "GA-01-AB-1234",
  "status": "available"
}
```

**Update Vehicle**
```http
PUT http://localhost:5000/api/vehicles/{vehicle_id}
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "status": "assigned"
}
```

**Delete Vehicle**
```http
DELETE http://localhost:5000/api/vehicles/{vehicle_id}
Authorization: Bearer YOUR_JWT_TOKEN
```

---

#### Live Locations API

**Get All Live Locations**
```http
GET http://localhost:5000/api/live-locations
Authorization: Bearer YOUR_JWT_TOKEN
```

**Get Officer's Location**
```http
GET http://localhost:5000/api/live-locations/officer/{officer_id}
Authorization: Bearer YOUR_JWT_TOKEN
```

**Update Officer's Location**
```http
POST http://localhost:5000/api/live-locations/officer/{officer_id}
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "latitude": 15.4909,
  "longitude": 73.8278,
  "accuracy": 10
}
```

---

#### Check-ins API

**Get All Check-ins**
```http
GET http://localhost:5000/api/check-ins
Authorization: Bearer YOUR_JWT_TOKEN
```

**Get Officer's Check-ins**
```http
GET http://localhost:5000/api/check-ins/officer/{officer_id}
Authorization: Bearer YOUR_JWT_TOKEN
```

**Create Check-in**
```http
POST http://localhost:5000/api/check-ins
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "duty_id": "DUTY123",
  "officer_id": "GP02650",
  "type": "check-in",
  "latitude": 15.4909,
  "longitude": 73.8278,
  "photo_url": "https://..."
}
```

---

#### Activities API

**Get All Activities**
```http
GET http://localhost:5000/api/activities
Authorization: Bearer YOUR_JWT_TOKEN
```

**Get Officer's Activities**
```http
GET http://localhost:5000/api/activities/officer/{officer_id}
Authorization: Bearer YOUR_JWT_TOKEN
```

**Create Activity**
```http
POST http://localhost:5000/api/activities
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "duty_id": "DUTY123",
  "officer_id": "GP02650",
  "activity_type": "patrol",
  "description": "Routine patrol",
  "latitude": 15.4909,
  "longitude": 73.8278
}
```

---

#### Notifications API

**Get Officer's Notifications**
```http
GET http://localhost:5000/api/notifications/officer/{officer_id}
Authorization: Bearer YOUR_JWT_TOKEN
```

**Create Notification**
```http
POST http://localhost:5000/api/notifications
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "officer_id": "GP02650",
  "title": "New Duty Assigned",
  "message": "You have been assigned a new patrol duty",
  "type": "duty_assignment"
}
```

**Mark as Read**
```http
PUT http://localhost:5000/api/notifications/{notification_id}/read
Authorization: Bearer YOUR_JWT_TOKEN
```

**Delete Notification**
```http
DELETE http://localhost:5000/api/notifications/{notification_id}
Authorization: Bearer YOUR_JWT_TOKEN
```

---

#### Duty Locations API

**Get All Duty Locations**
```http
GET http://localhost:5000/api/duty-locations
Authorization: Bearer YOUR_JWT_TOKEN
```

**Get Duty Location by ID**
```http
GET http://localhost:5000/api/duty-locations/{location_id}
Authorization: Bearer YOUR_JWT_TOKEN
```

**Create Duty Location**
```http
POST http://localhost:5000/api/duty-locations
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "name": "Panaji Market Area",
  "center_lat": 15.4909,
  "center_lng": 73.8278,
  "radius": 500,
  "polygon": {...}
}
```

---

#### Compliance API

**Get Compliance Records**
```http
GET http://localhost:5000/api/compliance
Authorization: Bearer YOUR_JWT_TOKEN
```

**Get Officer's Compliance**
```http
GET http://localhost:5000/api/compliance/officer/{officer_id}
Authorization: Bearer YOUR_JWT_TOKEN
```

**Create Compliance Record**
```http
POST http://localhost:5000/api/compliance
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "duty_id": "DUTY123",
  "officer_id": "GP02650",
  "compliance_type": "on_time",
  "status": "compliant"
}
```

---

### 🔑 Admin Endpoints

**Execute SQL Query**
```http
POST http://localhost:5000/admin/execute-sql
x-admin-key: gph-admin-secret-key-2024
Content-Type: application/json

{
  "query": "SELECT * FROM officers LIMIT 10"
}
```

---

## Frontend Integration Examples

### Setting up API client (axios example)

```typescript
// api/client.ts
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add JWT token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('jwt_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;
```

### Example API calls

```typescript
// Get all officers
const getOfficers = async () => {
  const response = await apiClient.get('/api/officers');
  return response.data;
};

// Login
const login = async (staffId: string) => {
  const response = await apiClient.post('/api/auth/login', {
    staff_id: staffId,
  });
  return response.data;
};

// Verify OTP
const verifyOtp = async (staffId: string, otp: string) => {
  const response = await apiClient.post('/api/auth/verify-otp', {
    staff_id: staffId,
    otp: otp,
  });
  // Store token
  localStorage.setItem('jwt_token', response.data.data.token);
  return response.data;
};

// Create duty
const createDuty = async (dutyData: any) => {
  const response = await apiClient.post('/api/duties', dutyData);
  return response.data;
};

// Update officer location
const updateLocation = async (officerId: string, lat: number, lng: number) => {
  const response = await apiClient.post(
    `/api/live-locations/officer/${officerId}`,
    {
      latitude: lat,
      longitude: lng,
      accuracy: 10,
    }
  );
  return response.data;
};
```

---

## Response Format

All API responses follow this structure:

**Success Response:**
```json
{
  "success": true,
  "data": {...},
  "message": "Optional success message"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message",
  "code": 400
}
```

---

## Common HTTP Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized (missing/invalid token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `500` - Internal Server Error

---

## Database Schema

The backend uses the following main tables:
- `officers` - Officer information
- `duties` - Duty assignments
- `vehicles` - Vehicle information
- `duty_locations` - Predefined duty locations
- `check_ins` - Officer check-in/check-out records
- `activities` - Activity logs
- `live_locations` - Real-time officer locations
- `notifications` - System notifications
- `compliance` - Compliance tracking

See `schema.sql` for complete database structure.

---

## Testing the Backend

### Quick Health Check
```bash
curl http://localhost:5000/health
```

### Test with Postman or Thunder Client
Import the endpoints above and start testing!

---

## Next Steps

1. ✅ Backend is running on `http://localhost:5000`
2. ✅ Frontend `.env` configured with `VITE_API_BASE_URL=http://localhost:5000`
3. 📝 Set up your frontend API client (see examples above)
4. 🔐 Implement authentication flow (login → verify OTP → store JWT)
5. 🚀 Start making API calls from your frontend

---

## Support

- Backend logs are in `app.log`
- Check console output for real-time server logs
- All database credentials are in `.env` file
- CORS is configured for localhost:5173 (Vite default)

**Your backend is ready to use! 🎉**
