# 🚀 Quick Start - Deploy in 5 Minutes

## What You Need
- Your Google Cloud VM (already logged in)
- This code uploaded to the VM

## Step-by-Step Commands

### 1️⃣ Upload Code to VM
**From your local Windows machine:**
```powershell
cd C:\Users\91902\Documents\GPH-backend-main
gcloud compute scp --recurse . your-instance-name:~/gph-backend --zone=your-zone
```

**Or use Git on the VM:**
```bash
# On your VM
cd ~
git clone YOUR_REPO_URL gph-backend
cd gph-backend
```

### 2️⃣ Run Deployment Script
```bash
cd ~/gph-backend
chmod +x deploy.sh
sudo bash deploy.sh
```

⏳ Wait 2-3 minutes for installation...

### 3️⃣ Generate Secure Keys
```bash
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
python3 -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"
python3 -c "import secrets; print('API_ADMIN_KEY=' + secrets.token_urlsafe(32))"
```

### 4️⃣ Update Configuration
```bash
sudo nano /opt/gph-backend/.env
```

**Copy the keys from step 3 and paste into the .env file:**
- Update `SECRET_KEY`
- Update `JWT_SECRET_KEY`
- Update `API_ADMIN_KEY`

Press `Ctrl+X`, then `Y`, then `Enter` to save.

### 5️⃣ Restart Service
```bash
sudo systemctl restart gph-backend
sudo systemctl restart nginx
```

### 6️⃣ Get Your Server IP
```bash
curl ifconfig.me
```

Copy this IP address! ✅

### 7️⃣ Test Your API
```bash
# Test locally on VM
curl http://localhost:5000/api/officers

# Test from outside (use IP from step 6)
curl http://YOUR_IP_HERE/api/officers
```

### 8️⃣ Configure Google Cloud Firewall
1. Go to Google Cloud Console
2. Navigate to **VPC Network** → **Firewall**
3. Click **Create Firewall Rule**
4. Settings:
   - Name: `allow-http`
   - Targets: `All instances in the network`
   - Source IP ranges: `0.0.0.0/0`
   - Protocols: Check **tcp** and enter `80`
5. Click **Create**

### 9️⃣ Update Frontend
In your frontend project `vigil-goa-dash/src/config/api.ts`:
```typescript
export const API_BASE_URL = 'http://YOUR_VM_IP';
```

### 🎉 Done!

Your backend is now live at: `http://YOUR_VM_IP`

## Test Endpoints
- Health: `http://YOUR_VM_IP/api/health`
- Officers: `http://YOUR_VM_IP/api/officers`
- Duties: `http://YOUR_VM_IP/api/duties`

## View Logs
```bash
# Real-time logs
sudo journalctl -u gph-backend -f

# Application errors
sudo tail -f /var/log/gph-backend/error.log
```

## Common Commands
```bash
# Restart app
sudo systemctl restart gph-backend

# View status
sudo systemctl status gph-backend

# Stop app
sudo systemctl stop gph-backend

# Start app
sudo systemctl start gph-backend
```

## Need Help?
Check the full guide: `DEPLOYMENT_GUIDE.md`

## Troubleshooting

**Service won't start?**
```bash
sudo journalctl -u gph-backend -n 50
```

**Can't connect from outside?**
- Check firewall rules in Google Cloud Console
- Verify: `sudo ufw status`
- Test locally first: `curl http://localhost:5000/api/health`

**Database connection failed?**
- Verify credentials in `/opt/gph-backend/.env`
- Test connection: `mysql -h mysql-3050fe0b-sde2024-0c30.l.aivencloud.com -P 16752 -u avnadmin -p`
