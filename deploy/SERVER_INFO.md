# Server Information & Credentials

**Last Updated**: December 4, 2025

## 🚀 Quick Reference

| Item | Value |
|------|-------|
| **Server IP** | `206.189.137.79` |
| **SSH** | `ssh -i ~/.ssh/id_ed25519_digitalocean root@206.189.137.79` |
| **Application URL** | http://206.189.137.79 |
| **Admin URL** | http://206.189.137.79/admin/ |
| **Admin Phone** | `+94771234567` |
| **Admin Password** | `Admin123!` |
| **MySQL Root Password** | `TempRootPass123!` |
| **Project Path** | `/var/www/vehicle-parts-api` |

## 🖥️ Server Details

- **Provider**: DigitalOcean
- **IP Address**: `206.189.137.79`
- **SSH Command**: 
  ```bash
  ssh -i ~/.ssh/id_ed25519_digitalocean root@206.189.137.79
  ```
- **SSH Key Location**: `~/.ssh/id_ed25519_digitalocean`
- **Operating System**: Ubuntu 24.04 LTS
- **Application Directory**: `/var/www/vehicle-parts-api`

---

## 🔐 Database Credentials

### MySQL Root User
- **Username**: `root`
- **Password**: `TempRootPass123!`
- **Host**: `localhost`
- **Port**: `3306`

### Application Database
- **Database Name**: `vehicle_parts`
- **Database User**: `vehicle_parts_user`
- **Database Password**: `your-secure-database-password-here` *(Check actual password in .env file)*
- **Host**: `localhost`
- **Port**: `3306`

**To view actual database password:**
```bash
ssh -i ~/.ssh/id_ed25519_digitalocean root@206.189.137.79
cd /var/www/vehicle-parts-api
cat .env | grep DB_PASSWORD
```

**Note**: The password in .env may be a placeholder. If migrations ran successfully, the actual password was set during database setup. Check the server logs or update the password if needed.

---

## 👤 Django Superuser Credentials

- **Phone Number**: `+94771234567` (Login username)
- **Email**: `admin@vehicleparts.com`
- **Password**: `Admin123!`
- **Name**: Admin User

**⚠️ IMPORTANT**: 
- Change the password after first login!
- Login uses phone number, not email
- Admin panel: http://206.189.137.79/admin/

---

## 🌐 Application URLs

- **Main Application**: http://206.189.137.79
- **Django Admin**: http://206.189.137.79/admin/
- **API Base**: http://206.189.137.79/api/

---

## 📁 Important File Paths

### Application Files
- **Project Root**: `/var/www/vehicle-parts-api`
- **Environment File**: `/var/www/vehicle-parts-api/.env`
- **Virtual Environment**: `/var/www/vehicle-parts-api/venv`
- **Static Files**: `/var/www/vehicle-parts-api/staticfiles`
- **Media Files**: `/var/www/vehicle-parts-api/media`

### Configuration Files
- **Nginx Config**: `/etc/nginx/sites-available/vehicle-parts-api`
- **Systemd Service**: `/etc/systemd/system/vehicle-parts-api.service`
- **Nginx Enabled**: `/etc/nginx/sites-enabled/vehicle-parts-api`

### Log Files
- **Application Logs**: `/var/log/vehicle-parts-api/error.log`
- **Application Access Logs**: `/var/log/vehicle-parts-api/access.log`
- **Nginx Error Logs**: `/var/log/nginx/vehicle-parts-api-error.log`
- **Nginx Access Logs**: `/var/log/nginx/vehicle-parts-api-access.log`

---

## 🔧 Service Management

### Check Service Status
```bash
sudo systemctl status vehicle-parts-api
sudo systemctl status nginx
sudo systemctl status mysql
```

### Restart Services
```bash
sudo systemctl restart vehicle-parts-api
sudo systemctl restart nginx
sudo systemctl restart mysql
```

### View Logs
```bash
# Application logs
sudo tail -f /var/log/vehicle-parts-api/error.log
sudo tail -f /var/log/vehicle-parts-api/access.log

# Nginx logs
sudo tail -f /var/log/nginx/vehicle-parts-api-error.log
sudo tail -f /var/log/nginx/vehicle-parts-api-access.log

# System logs
sudo journalctl -u vehicle-parts-api -f
```

---

## 🗄️ Database Management

### Connect to MySQL
```bash
mysql -u root -p
# Password: TempRootPass123!
```

### Connect as Application User
```bash
mysql -u vehicle_parts_user -p vehicle_parts
# Password: (check .env file)
```

### Backup Database
```bash
mysqldump -u vehicle_parts_user -p vehicle_parts > backup_$(date +%Y%m%d).sql
```

### Restore Database
```bash
mysql -u vehicle_parts_user -p vehicle_parts < backup_YYYYMMDD.sql
```

---

## 🚀 Deployment Commands

### Update Application
```bash
cd /var/www/vehicle-parts-api
git pull origin main
./deploy/deploy.sh
```

### Run Migrations
```bash
cd /var/www/vehicle-parts-api
source venv/bin/activate
python manage.py migrate
```

### Collect Static Files
```bash
cd /var/www/vehicle-parts-api
source venv/bin/activate
python manage.py collectstatic --noinput
```

### Create New Superuser
```bash
cd /var/www/vehicle-parts-api
source venv/bin/activate
python manage.py createsuperuser
```

---

## 🔒 Security Information

### Firewall Status
- **UFW**: Enabled
- **Open Ports**: 
  - SSH (22)
  - HTTP (80)
  - HTTPS (443) - *To be configured with SSL*

### Change MySQL Root Password
```bash
sudo mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'YourNewPassword';
FLUSH PRIVILEGES;
```

### Change Django Secret Key
1. Generate new key:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
2. Update in `/var/www/vehicle-parts-api/.env`:
   ```
   SECRET_KEY=your-new-secret-key-here
   ```
3. Restart service:
   ```bash
   sudo systemctl restart vehicle-parts-api
   ```

---

## 📧 Email Configuration

Email settings are configured in `/var/www/vehicle-parts-api/.env`:
- **EMAIL_BACKEND**: `django.core.mail.backends.smtp.EmailBackend`
- **EMAIL_HOST**: *(Check .env file)*
- **EMAIL_PORT**: `587`
- **EMAIL_USE_TLS**: `True`
- **EMAIL_HOST_USER**: *(Check .env file)*
- **EMAIL_HOST_PASSWORD**: *(Check .env file)*

---

## ☁️ DigitalOcean Spaces Configuration (If Used)

DigitalOcean Spaces settings are in `/var/www/vehicle-parts-api/.env`:
- **USE_SPACES**: `True` (set to `False` to disable)
- **SPACES_ACCESS_KEY_ID**: *(Check .env file)*
- **SPACES_SECRET_ACCESS_KEY**: *(Check .env file)*
- **SPACES_BUCKET_NAME**: *(Check .env file)*
- **SPACES_REGION_NAME**: *(Check .env file)*
- **SPACES_ENDPOINT_URL**: *(Check .env file)*

---

## 📱 Twilio/WhatsApp Configuration (If Used)

Twilio settings are in `/var/www/vehicle-parts-api/.env`:
- **TWILIO_WHATSAPP_ENABLED**: `False` (set to `True` to enable)
- **TWILIO_ACCOUNT_SID**: *(Check .env file)*
- **TWILIO_AUTH_TOKEN**: *(Check .env file)*
- **TWILIO_ENVIRONMENT**: `sandbox` or `production`
- **TWILIO_WHATSAPP_FROM**: *(Check .env file)*

---

## 🔍 Troubleshooting

### Application Not Starting
```bash
# Check service status
sudo systemctl status vehicle-parts-api

# Check logs
sudo journalctl -u vehicle-parts-api -n 50

# Check if port is in use
sudo netstat -tlnp | grep 8000
```

### Database Connection Issues
```bash
# Test MySQL connection
sudo systemctl status mysql
mysql -u vehicle_parts_user -p vehicle_parts

# Check database credentials in .env
cat /var/www/vehicle-parts-api/.env | grep DB_
```

### Nginx Issues
```bash
# Test Nginx configuration
sudo nginx -t

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log

# Reload Nginx
sudo systemctl reload nginx
```

### Permission Issues
```bash
# Fix ownership
sudo chown -R www-data:www-data /var/www/vehicle-parts-api

# Fix permissions
sudo chmod -R 755 /var/www/vehicle-parts-api
sudo chmod -R 775 /var/www/vehicle-parts-api/media
sudo chmod -R 775 /var/www/vehicle-parts-api/staticfiles
```

---

## 📝 Quick Reference Commands

```bash
# SSH into server
ssh -i ~/.ssh/id_ed25519_digitalocean root@206.189.137.79

# Navigate to project
cd /var/www/vehicle-parts-api

# Activate virtual environment
source venv/bin/activate

# View environment variables
cat .env

# Restart all services
sudo systemctl restart vehicle-parts-api nginx mysql

# View all logs
sudo tail -f /var/log/vehicle-parts-api/error.log /var/log/nginx/vehicle-parts-api-error.log
```

---

## 🔄 Backup Strategy

### Daily Database Backup (Recommended)
Add to crontab:
```bash
0 2 * * * mysqldump -u vehicle_parts_user -p'PASSWORD' vehicle_parts > /backup/vehicle_parts_$(date +\%Y\%m\%d).sql
```

### Manual Backup
```bash
# Database
mysqldump -u vehicle_parts_user -p vehicle_parts > backup.sql

# Media files
tar -czf media_backup_$(date +%Y%m%d).tar.gz /var/www/vehicle-parts-api/media
```

---

## 📞 Support & Maintenance

- **Server Monitoring**: Check logs regularly
- **Updates**: Run `sudo apt-get update && sudo apt-get upgrade` monthly
- **Backups**: Ensure daily database backups are running
- **SSL Certificate**: Set up SSL with Let's Encrypt for production

---

## ⚠️ Security Reminders

1. **Change default passwords** (MySQL root, Django superuser)
2. **Keep Django SECRET_KEY** secure and never commit to git
3. **Use strong passwords** for all services
4. **Enable SSL/HTTPS** for production
5. **Regular security updates**: `sudo apt-get update && sudo apt-get upgrade`
6. **Firewall**: Only open necessary ports
7. **Backup regularly**: Database and media files

---

**Note**: This document contains sensitive information. Keep it secure and do not commit to public repositories.


