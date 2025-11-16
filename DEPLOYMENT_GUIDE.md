# GPH Backend Deployment Guide for Google Cloud

## Prerequisites
- Google Cloud VM running Ubuntu 22.04
- MySQL database configured (Aiven Cloud - already done)
- SSH access to the VM
- Domain name (optional, can use IP address)

## Quick Deployment Steps

### 1. Connect to Your Google Cloud VM
```bash
# From your local machine
gcloud compute ssh your-vm-name --zone=your-zone
# OR use the SSH button in Google Cloud Console
```

### 2. Upload Your Code to the VM

**Option A: Using Git (Recommended)**
```bash
# On your VM
cd ~
git clone https://github.com/yourusername/GPH-backend-main.git
cd GPH-backend-main
```

**Option B: Using SCP from your local machine**
```bash
# From your local machine (Windows PowerShell)
cd C:\Users\91902\Documents\GPH-backend-main
gcloud compute scp --recurse . your-vm-name:~/GPH-backend-main --zone=your-zone
```

**Option C: Using the Cloud Console Upload**
1. In Google Cloud Console, use the "Upload File" feature
2. Upload all files to `/home/yourusername/GPH-backend-main`

### 3. Run the Deployment Script
```bash
# On your VM
cd ~/GPH-backend-main
chmod +x deploy.sh
sudo bash deploy.sh
```

The script will:
- Install all required packages (Python, Nginx, etc.)
- Create application user and directories
- Set up Python virtual environment
- Install dependencies
- Create systemd service for auto-start
- Configure Nginx as reverse proxy
- Configure firewall

### 4. Update Configuration
```bash
# Edit the .env file with your actual credentials
sudo nano /opt/gph-backend/.env
```

Update these values:
```env
SECRET_KEY=generate-a-strong-random-key-here
JWT_SECRET_KEY=generate-another-strong-random-key-here
API_ADMIN_KEY=your-admin-api-key-here
```

Generate secure keys:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Update Frontend API URL
```bash
# Get your VM's external IP
curl ifconfig.me
```

Update your frontend `config/api.ts`:
```typescript
export const API_BASE_URL = 'http://YOUR_VM_EXTERNAL_IP';
```

### 6. Restart Services
```bash
sudo systemctl restart gph-backend
sudo systemctl restart nginx
```

### 7. Verify Deployment
```bash
# Check service status
sudo systemctl status gph-backend

# Test the API
curl http://localhost:5000/api/health
curl http://YOUR_VM_EXTERNAL_IP/api/health
```

## Firewall Configuration

### Google Cloud Firewall Rules
1. Go to **VPC Network** → **Firewall**
2. Create a new rule:
   - Name: `allow-http`
   - Targets: All instances in network
   - Source IP ranges: `0.0.0.0/0`
   - Protocols and ports: `tcp:80`
3. Click **Create**

### Test from Your Browser
```
http://YOUR_VM_EXTERNAL_IP/api/health
```

## Monitoring & Logs

### View Application Logs
```bash
# Real-time logs
sudo journalctl -u gph-backend -f

# Last 100 lines
sudo journalctl -u gph-backend -n 100

# Gunicorn logs
sudo tail -f /var/log/gph-backend/error.log
sudo tail -f /var/log/gph-backend/access.log
```

### View Nginx Logs
```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Check Service Status
```bash
# Application status
sudo systemctl status gph-backend

# Nginx status
sudo systemctl status nginx
```

## Common Management Commands

### Restart Application
```bash
sudo systemctl restart gph-backend
```

### Stop Application
```bash
sudo systemctl stop gph-backend
```

### Start Application
```bash
sudo systemctl start gph-backend
```

### Update Code
```bash
cd /opt/gph-backend
sudo -u gph git pull origin main
sudo systemctl restart gph-backend
```

### Install New Dependencies
```bash
cd /opt/gph-backend
sudo -u gph /opt/gph-backend/venv/bin/pip install -r requirements.txt
sudo systemctl restart gph-backend
```

## SSL/HTTPS Configuration (Optional but Recommended)

### Using Let's Encrypt (Free SSL)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate (replace with your domain)
sudo certbot --nginx -d yourdomain.com

# Auto-renewal is configured automatically
```

Update your `.env`:
```env
FORCE_HTTPS=True
```

## Troubleshooting

### Application Won't Start
```bash
# Check logs for errors
sudo journalctl -u gph-backend -n 50

# Check if port is already in use
sudo lsof -i :5000

# Verify .env file exists and has correct permissions
ls -la /opt/gph-backend/.env
```

### Database Connection Issues
```bash
# Test MySQL connection
mysql -h mysql-3050fe0b-sde2024-0c30.l.aivencloud.com -P 16752 -u avnadmin -p

# Check firewall
sudo ufw status
```

### Nginx Configuration Issues
```bash
# Test Nginx configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

### Permission Issues
```bash
# Fix ownership
sudo chown -R gph:gph /opt/gph-backend
sudo chown -R gph:gph /var/log/gph-backend
```

## Performance Tuning

### For Production Use
Edit `/opt/gph-backend/gunicorn_config.py`:
```python
# Adjust workers based on your VM specs
workers = (2 * CPU_COUNT) + 1

# For 1 CPU VM: workers = 3
# For 2 CPU VM: workers = 5
# For 4 CPU VM: workers = 9
```

### Monitor Resource Usage
```bash
# CPU and Memory
htop

# Disk usage
df -h

# Network connections
sudo netstat -tuln | grep 5000
```

## Database Backup (Recommended)

```bash
# Create backup script
sudo tee /opt/backup-db.sh > /dev/null << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

mysqldump -h mysql-3050fe0b-sde2024-0c30.l.aivencloud.com \
  -P 16752 \
  -u avnadmin \
  -pAVNS_t1kjGBiF83OqHaGxPpq \
  defaultdb > $BACKUP_DIR/backup_$DATE.sql

# Keep only last 7 days
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
EOF

sudo chmod +x /opt/backup-db.sh

# Run daily at 2 AM
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/backup-db.sh") | crontab -
```

## Security Best Practices

1. **Change default credentials** in `.env`
2. **Enable firewall**: `sudo ufw enable`
3. **Use HTTPS** with Let's Encrypt
4. **Regular updates**: `sudo apt update && sudo apt upgrade`
5. **Monitor logs** regularly
6. **Backup database** daily
7. **Use strong passwords** for admin API key
8. **Restrict CORS** to your frontend domain in production

## Support & Resources

- Application logs: `/var/log/gph-backend/`
- Nginx logs: `/var/log/nginx/`
- Service status: `sudo systemctl status gph-backend`
- Configuration: `/opt/gph-backend/.env`

## Quick Reference

| Action | Command |
|--------|---------|
| View logs | `sudo journalctl -u gph-backend -f` |
| Restart app | `sudo systemctl restart gph-backend` |
| Edit config | `sudo nano /opt/gph-backend/.env` |
| Check status | `sudo systemctl status gph-backend` |
| Update code | `cd /opt/gph-backend && sudo -u gph git pull` |
| Restart Nginx | `sudo systemctl restart nginx` |
