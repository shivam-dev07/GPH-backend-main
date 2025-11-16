# Police Patrolling App - Backend Server

Production-ready Flask backend with MVC architecture for Goa Police patrol management system.

## 🏗️ Architecture

This backend follows a modular MVC (Model-View-Controller) pattern with clear separation of concerns:

```
backend/
├── app.py                      # Main entry point (Flask factory)
├── config.py                   # Configuration loader
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
│
├── models/                    # Data access layer
│   ├── db.py                 # Database connection with SSL
│   ├── admin_model.py        # Admin SQL execution
│   └── officer_model.py      # Officer data access
│
├── controllers/               # Business logic layer
│   ├── admin_controller.py   # Admin operations
│   └── public_controller.py  # Public API operations
│
├── routes/                    # API routing layer
│   ├── admin_routes.py       # Admin endpoints
│   └── public_routes.py      # Public endpoints
│
├── utils/                     # Shared utilities
│   ├── logger.py             # Logging utilities
│   ├── responses.py          # JSON response helpers
│   └── security.py           # Security checks
│
└── tests/                     # Test suite
    ├── test_admin.py
    ├── test_public.py
    └── test_db.py
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your Aiven MySQL credentials and admin key.

### 3. Run the Server

```bash
python app.py
```

The server will start on `http://0.0.0.0:5000`

## 📡 API Endpoints

### Public Endpoints

#### Health Check
```http
GET /health
```

Response:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "database": "connected",
    "timestamp": "2025-11-15T04:48:00.000000Z"
  }
}
```

#### Get All Officers
```http
GET /officers
```

Response:
```json
{
  "success": true,
  "data": [
    {
      "id": "GP02650",
      "staff_id": "GP02650",
      "staff_name": "John Doe",
      "staff_designation": "Police Constable",
      "staff_nature_of_work": "Patrol Duty",
      "status": "active",
      "created_at": "...",
      "updated_at": "..."
    }
  ]
}
```

#### Get Officer by ID
```http
GET /officers/{officer_id}
```

Response:
```json
{
  "success": true,
  "data": {
    "id": "GP02650",
    "staff_id": "GP02650",
    "staff_name": "John Doe",
    ...
  }
}
```

### Admin Endpoints

#### Execute SQL
```http
POST /admin/execute-sql
Headers:
  x-admin-key: <API_ADMIN_KEY>
  Content-Type: application/json
  
Body:
{
  "query": "SELECT * FROM officers LIMIT 10"
}
```

Response (SELECT):
```json
{
  "success": true,
  "type": "select",
  "rows": [...]
}
```

Response (INSERT/UPDATE/DELETE):
```json
{
  "success": true,
  "type": "write",
  "rows_affected": 5
}
```

## 🔒 Security Features

### 1. Admin Authentication
- All admin endpoints require `x-admin-key` header
- Unauthorized attempts are logged

### 2. Dangerous Query Protection
Automatically blocks:
- `DROP DATABASE`
- `DROP TABLE`
- `TRUNCATE`
- `ALTER USER`
- `GRANT`
- `REVOKE`
- `FLUSH PRIVILEGES`

### 3. SQL Injection Prevention
- All public endpoints use parameterized queries
- No raw SQL construction in controllers

### 4. Query Length Limit
- Maximum query length: 10,000 characters
- Prevents resource exhaustion

### 5. SSL/TLS Database Connection
- Required SSL mode for Aiven MySQL
- Encrypted database connections

### 6. Comprehensive Logging
- All requests logged with timestamp, IP, query/path, status
- Errors logged without exposing stack traces
- Logs written to `sql_queries.log` and stdout

## 🛠️ Development

### Running Tests

```bash
cd backend
python -m pytest tests/
```

### Adding New Endpoints

1. **Model** - Add data access function in `models/`
2. **Controller** - Add business logic in `controllers/`
3. **Route** - Define endpoint in `routes/`
4. **Test** - Add tests in `tests/`

Example:
```python
# models/duty_model.py
class DutyModel:
    @staticmethod
    def get_all_duties():
        with get_connection() as conn:
            # ... query logic

# controllers/public_controller.py
class PublicController:
    @staticmethod
    def get_all_duties():
        duties = DutyModel.get_all_duties()
        return ResponseHelper.success_data(duties)

# routes/public_routes.py
@public_bp.route('/duties', methods=['GET'])
def get_duties():
    return PublicController.get_all_duties()
```

## 📊 Database Structure

The backend connects to MySQL database with the following main tables:
- `officers` - Officer information
- `duties` - Duty assignments
- `check_ins` - Officer check-in records
- `activities` - Activity logs
- `vehicles` - Vehicle information
- `notifications` - System notifications

See database schema documentation for complete structure.

## 🌐 Deployment

### Google Cloud Compute Engine

1. **Set up VM** with Python 3.9+
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Configure .env** with production credentials
4. **Use production WSGI server** (Gunicorn recommended):

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

5. **Set up systemd service** for auto-restart
6. **Configure nginx** as reverse proxy
7. **Enable HTTPS** with Let's Encrypt

### Environment Variables for Production

```bash
FORCE_HTTPS=true
DEBUG_MODE=false
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

## 📝 Configuration Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | MySQL host | - |
| `DB_PORT` | MySQL port | 3306 |
| `DB_USER` | MySQL username | - |
| `DB_PASSWORD` | MySQL password | - |
| `DB_NAME` | Database name | defaultdb |
| `API_ADMIN_KEY` | Admin authentication key | - |
| `ALLOWED_ORIGINS` | CORS origins | * |
| `FORCE_HTTPS` | Enforce HTTPS | false |
| `ALLOW_WRITE_QUERIES` | Allow write operations | true |
| `SERVER_HOST` | Server bind address | 0.0.0.0 |
| `SERVER_PORT` | Server port | 5000 |
| `DEBUG_MODE` | Flask debug mode | false |

## 🤝 Contributing

1. Create feature branch
2. Add tests for new features
3. Ensure all tests pass
4. Follow existing code structure
5. Update documentation

## 📄 License

Proprietary - Goa Police Department

## 🆘 Support

For issues or questions, contact the development team.
