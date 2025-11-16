# 🔧 VIGIL-GOA-DASH Connection Fix - Complete Guide

## ✅ What Was Fixed

### Problem
The frontend was showing connection errors because the API URLs were incorrectly configured with duplicate `/api` prefixes.

**Before (WRONG):**
- Frontend `.env`: `VITE_API_BASE_URL=http://localhost:5000/api`
- API client adds: `/officers`
- Final URL: `http://localhost:5000/api/officers` ❌ (Backend doesn't have this route)

**After (CORRECT):**
- Frontend `.env`: `VITE_API_BASE_URL=http://localhost:5000`
- API client adds: `/api/officers`
- Final URL: `http://localhost:5000/api/officers` ✅ (Matches backend routes)

### Files Changed

1. **Frontend `.env`** (`c:\Users\91902\Desktop\vigil-goa-dash\.env`)
   ```env
   VITE_API_BASE_URL=http://localhost:5000
   ```

2. **API Service** (`src/services/api.ts`)
   - Changed base URL from `http://localhost:5000/api` to `http://localhost:5000`
   - Added `/api` prefix to all endpoint paths

3. **API Config** (`src/config/api.ts`)
   - Changed base URL from `http://localhost:5000/api` to `http://localhost:5000`
   - Added `/api` prefix to all endpoint paths

---

## 🚀 How to Test the Fix

### Step 1: Verify Backend is Running

The backend should already be running. Check terminal output for:
```
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.8:5000
```

### Step 2: Open Test Page

Open this file in your browser:
```
c:\Users\91902\Documents\GPH-backend-main\test-connection.html
```

It will automatically test the connection and show you:
- ✅ Which endpoints are working
- ❌ Which endpoints have issues
- Detailed JSON responses

### Step 3: Restart Your Frontend Development Server

If your frontend (Vite) is running, **restart it** to pick up the new `.env` changes:

1. Stop the frontend server (Ctrl+C)
2. Start it again:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

### Step 4: Check Browser Console

Open your dashboard and check the browser console (F12):
- Look for successful API calls to `http://localhost:5000/api/...`
- No more 404 or CORS errors

---

## 📋 Correct API Endpoint Structure

### Backend Routes (Flask)

```python
# Public routes (no /api prefix)
GET  /health                    # Health check
GET  /officers                  # All officers (legacy, deprecated)
GET  /officers/{id}             # Single officer (legacy, deprecated)

# Protected routes (with /api prefix) - THESE ARE THE MAIN ROUTES
GET  /api/officers              # All officers
GET  /api/officers/{id}         # Single officer
POST /api/officers              # Create officer
PUT  /api/officers/{id}         # Update officer
DELETE /api/officers/{id}       # Delete officer

GET  /api/duties                # All duties
GET  /api/duties/{id}           # Single duty
POST /api/duties                # Create duty
PUT  /api/duties/{id}           # Update duty
DELETE /api/duties/{id}         # Delete duty

GET  /api/vehicles              # All vehicles
GET  /api/vehicles/{id}         # Single vehicle
POST /api/vehicles              # Create vehicle
PUT  /api/vehicles/{id}         # Update vehicle
DELETE /api/vehicles/{id}       # Delete vehicle

GET  /api/activities            # All activities
GET  /api/activities/officer/{id}  # Officer's activities
POST /api/activities            # Create activity

GET  /api/live-locations        # All locations
GET  /api/live-locations/officer/{id}  # Officer's location
POST /api/live-locations/officer/{id}  # Update location

GET  /api/check-ins             # All check-ins
GET  /api/check-ins/duty/{id}   # Duty's check-ins
POST /api/check-ins             # Create check-in

GET  /api/notifications/officer/{id}  # Officer's notifications
POST /api/notifications         # Create notification
PUT  /api/notifications/{id}/read  # Mark as read
DELETE /api/notifications/{id}  # Delete notification

GET  /api/duty-locations        # All duty locations
GET  /api/duty-locations/{id}   # Single duty location
POST /api/duty-locations        # Create duty location
DELETE /api/duty-locations/{id} # Delete duty location

GET  /api/compliance            # All compliance logs
GET  /api/compliance/duty/{id}  # Duty's compliance
POST /api/compliance            # Create compliance log
```

### Frontend API Client

```typescript
// Correct setup
const BASE_URL = 'http://localhost:5000';  // NO /api suffix

const endpoints = {
  officers: '/api/officers',     // WITH /api prefix
  duties: '/api/duties',         // WITH /api prefix
  vehicles: '/api/vehicles',     // WITH /api prefix
  // ... etc
};

// Results in: http://localhost:5000/api/officers ✅
```

---

## 🔍 Troubleshooting

### Issue: "Connection refused" or "Network error"

**Check:**
1. Is the backend running? Look for terminal with Flask server
2. Is it on port 5000? Check terminal output
3. Test with: Open `test-connection.html` in browser

**Fix:**
```bash
cd C:\Users\91902\Documents\GPH-backend-main
C:/Users/91902/Documents/GPH-backend-main/.venv/Scripts/python.exe run.py
```

### Issue: "404 Not Found"

**Check:**
- URL format in browser console
- Should be: `http://localhost:5000/api/officers`
- NOT: `http://localhost:5000/api/api/officers`
- NOT: `http://localhost:5000/officers/api`

**Fix:**
- Verify `.env` has NO `/api` suffix: `VITE_API_BASE_URL=http://localhost:5000`
- Restart frontend dev server

### Issue: "CORS policy error"

**Check:**
- Backend `.env` has correct CORS setting:
  ```env
  CORS_ORIGINS=http://localhost:5173, http://localhost:3000, http://localhost:5000
  ```

**Fix:**
- Add your frontend port to CORS_ORIGINS
- Restart backend server

### Issue: "Empty data" or "No officers/duties shown"

**Check:**
1. Is database populated?
2. Are API calls successful? (Check browser Network tab)
3. Is response format correct?

**Test:**
- Open `test-connection.html` and click "Test All Endpoints"
- Check which endpoints return empty arrays vs errors

---

## 📊 Database Setup

If you need to populate the database with test data:

```bash
cd C:\Users\91902\Documents\GPH-backend-main

# Create tables
C:/Users/91902/Documents/GPH-backend-main/.venv/Scripts/python.exe -c "
from models.db import get_connection
with open('schema.sql', 'r') as f:
    sql = f.read()
conn = get_connection()
cursor = conn.cursor()
for statement in sql.split(';'):
    if statement.strip():
        cursor.execute(statement)
conn.commit()
conn.close()
print('Database schema created!')
"
```

---

## ✨ Quick Reference

### Environment Variables

**Backend** (`GPH-backend-main/.env`):
```env
DB_HOST=goa12-sv520413-a84d.k.aivencloud.com
DB_PORT=20063
DB_USER=avnadmin
DB_PASSWORD=AVNS_pwhnLU3DS8B456aa8Le
DB_NAME=defaultdb
SERVER_HOST=0.0.0.0
SERVER_PORT=5000
CORS_ORIGINS=http://localhost:5173, http://localhost:3000, http://localhost:5000
```

**Frontend** (`vigil-goa-dash/.env`):
```env
VITE_API_BASE_URL=http://localhost:5000
```

### Start Servers

**Backend:**
```bash
cd C:\Users\91902\Documents\GPH-backend-main
C:/Users/91902/Documents/GPH-backend-main/.venv/Scripts/python.exe run.py
```

**Frontend:**
```bash
cd C:\Users\91902\Desktop\vigil-goa-dash
npm run dev
# Opens on http://localhost:5173
```

---

## 🎯 Expected Behavior After Fix

1. ✅ Frontend loads without connection errors
2. ✅ Dashboard shows officers, duties, vehicles (if data exists)
3. ✅ Map displays live locations (if data exists)
4. ✅ No CORS errors in browser console
5. ✅ API calls shown in Network tab as successful (200 OK)

---

## 📞 Next Steps

1. **Restart frontend dev server** to apply `.env` changes
2. **Test with `test-connection.html`** to verify all endpoints
3. **Check browser console** for any remaining errors
4. **Populate database** if tables are empty
5. **Start using the dashboard!**

---

## 🐛 Still Having Issues?

Check these in order:

1. **Backend Status**
   - Is it running? Check terminal
   - Any errors in `app.log`?
   - Test: `http://localhost:5000/health` in browser

2. **Frontend Status**
   - Did you restart after changing `.env`?
   - Check browser console (F12)
   - Check Network tab for API calls

3. **Database Status**
   - Can backend connect to database?
   - Are tables created? (`schema.sql`)
   - Is there test data?

4. **CORS Configuration**
   - Backend allows your frontend port?
   - Check CORS_ORIGINS in backend `.env`

---

**Your connection should now be working! 🎉**

If you still see errors, check the browser console and compare the API URLs being called with the backend routes listed above.
