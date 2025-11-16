#!/bin/bash

# GPH Backend Deployment Script for Google Cloud VM
# Run this script on your Ubuntu server

set -e  # Exit on error

echo "=========================================="
echo "GPH Backend Deployment Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="gph-backend"
APP_DIR="/opt/$APP_NAME"
APP_USER="gph"
PYTHON_VERSION="python3.10"

echo -e "${GREEN}Step 1: Updating system packages...${NC}"
sudo apt update
sudo apt upgrade -y

echo -e "${GREEN}Step 2: Installing required packages...${NC}"
sudo apt install -y python3.10 python3.10-venv python3-pip nginx git

echo -e "${GREEN}Step 3: Creating application user...${NC}"
if id "$APP_USER" &>/dev/null; then
    echo "User $APP_USER already exists"
else
    sudo useradd -m -s /bin/bash $APP_USER
    echo "User $APP_USER created"
fi

echo -e "${GREEN}Step 4: Creating application directory...${NC}"
sudo mkdir -p $APP_DIR
sudo chown $APP_USER:$APP_USER $APP_DIR

echo -e "${GREEN}Step 5: Creating log directories...${NC}"
sudo mkdir -p /var/log/$APP_NAME
sudo chown $APP_USER:$APP_USER /var/log/$APP_NAME
sudo mkdir -p /var/run/$APP_NAME
sudo chown $APP_USER:$APP_USER /var/run/$APP_NAME

echo -e "${GREEN}Step 6: Copying application files...${NC}"
# Note: You should upload your files to the server first
# For now, we'll assume files are in current directory
sudo cp -r . $APP_DIR/
sudo chown -R $APP_USER:$APP_USER $APP_DIR

echo -e "${GREEN}Step 7: Setting up Python virtual environment...${NC}"
cd $APP_DIR
sudo -u $APP_USER $PYTHON_VERSION -m venv venv
sudo -u $APP_USER $APP_DIR/venv/bin/pip install --upgrade pip
sudo -u $APP_USER $APP_DIR/venv/bin/pip install -r requirements.txt
sudo -u $APP_USER $APP_DIR/venv/bin/pip install gunicorn

echo -e "${GREEN}Step 8: Creating .env file template...${NC}"
if [ ! -f "$APP_DIR/.env" ]; then
    cat > /tmp/.env << 'EOF'
# Database Configuration (Aiven MySQL)
DB_HOST=mysql-3050fe0b-sde2024-0c30.l.aivencloud.com
DB_PORT=16752
DB_USER=avnadmin
DB_PASSWORD=AVNS_t1kjGBiF83OqHaGxPpq
DB_NAME=defaultdb

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-change-this

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-change-this
JWT_EXPIRATION_HOURS=8

# CORS Configuration
CORS_ORIGINS=*

# Server Configuration
HOST=0.0.0.0
PORT=5000
FORCE_HTTPS=False

# Security Configuration
API_ADMIN_KEY=your-admin-key-change-this
MAX_QUERY_LENGTH=5000
ALLOW_WRITE_QUERIES=True

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/gph-backend/app.log
EOF
    sudo mv /tmp/.env $APP_DIR/.env
    sudo chown $APP_USER:$APP_USER $APP_DIR/.env
    sudo chmod 600 $APP_DIR/.env
    echo -e "${YELLOW}WARNING: Please edit $APP_DIR/.env and update SECRET_KEY and other credentials${NC}"
else
    echo ".env file already exists, skipping..."
fi

echo -e "${GREEN}Step 9: Creating systemd service...${NC}"
sudo tee /etc/systemd/system/$APP_NAME.service > /dev/null << EOF
[Unit]
Description=GPH Backend Flask Application
After=network.target

[Service]
Type=notify
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn --config gunicorn_config.py wsgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always

[Install]
WantedBy=multi-user.target
EOF

echo -e "${GREEN}Step 10: Configuring Nginx...${NC}"
sudo tee /etc/nginx/sites-available/$APP_NAME > /dev/null << 'EOF'
server {
    listen 80;
    server_name _;  # Replace with your domain or VM external IP

    # Increase client body size for file uploads
    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS headers (if needed)
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type' always;
        
        # Handle preflight requests
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type';
            add_header 'Content-Length' 0;
            add_header 'Content-Type' 'text/plain';
            return 204;
        }
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "OK";
        add_header Content-Type text/plain;
    }
}
EOF

# Enable the site
sudo ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

echo -e "${GREEN}Step 11: Testing Nginx configuration...${NC}"
sudo nginx -t

echo -e "${GREEN}Step 12: Enabling and starting services...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable $APP_NAME
sudo systemctl restart $APP_NAME
sudo systemctl restart nginx

echo -e "${GREEN}Step 13: Configuring firewall...${NC}"
sudo ufw allow 'Nginx Full'
sudo ufw allow 22/tcp  # SSH
sudo ufw --force enable

echo ""
echo "=========================================="
echo -e "${GREEN}Deployment Complete!${NC}"
echo "=========================================="
echo ""
echo "Service Status:"
sudo systemctl status $APP_NAME --no-pager
echo ""
echo "Useful Commands:"
echo "  View logs:        sudo journalctl -u $APP_NAME -f"
echo "  Restart service:  sudo systemctl restart $APP_NAME"
echo "  Stop service:     sudo systemctl stop $APP_NAME"
echo "  Start service:    sudo systemctl start $APP_NAME"
echo "  Nginx logs:       sudo tail -f /var/log/nginx/error.log"
echo "  App logs:         sudo tail -f /var/log/$APP_NAME/error.log"
echo ""
echo -e "${YELLOW}IMPORTANT:${NC}"
echo "1. Edit $APP_DIR/.env and update all credentials"
echo "2. Update Nginx server_name with your domain/IP"
echo "3. Then restart: sudo systemctl restart $APP_NAME nginx"
echo ""
