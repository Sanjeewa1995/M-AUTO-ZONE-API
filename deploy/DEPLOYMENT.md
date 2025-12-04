# DigitalOcean Droplet Deployment Guide

This guide will help you deploy the Vehicle Parts API Django application with MySQL database on a single DigitalOcean droplet.

## Prerequisites

- A DigitalOcean account
- A domain name (optional, but recommended for SSL)
- SSH access to your droplet

## Step 1: Create a DigitalOcean Droplet

1. Log in to your DigitalOcean account
2. Click "Create" → "Droplets"
3. Choose:
   - **Image**: Ubuntu 24.04 LTS (or latest LTS)
   - **Plan**: At least 2GB RAM / 1 vCPU (recommended: 4GB RAM / 2 vCPU for production)
   - **Datacenter**: Choose closest to your users
   - **Authentication**: SSH keys (recommended) or root password
4. Click "Create Droplet"

## Step 2: Initial Server Setup

### Connect to your droplet

```bash
ssh root@your-droplet-ip
# or
ssh root@your-domain.com
```

### Run the server setup script

1. Clone your repository:

```bash
cd /var/www
git clone https://github.com/your-username/vehicle-parts-api.git
cd vehicle-parts-api
```

2. Make scripts executable:

```bash
chmod +x deploy/*.sh
```

3. Run the server setup script:

```bash
# Set MySQL root password (optional, or use default)
export MYSQL_ROOT_PASSWORD="YourSecureRootPassword123!"
./deploy/setup-server.sh
```

This script will:
- Update system packages
- Install Python 3.13, MySQL, Nginx, and other dependencies
- Configure MySQL
- Set up firewall rules
- Create necessary directories

## Step 3: Configure Database

1. Run the database setup script:

```bash
./deploy/setup-database.sh
```

**Note**: The script will generate a random password for the database user. Save this password!

2. Alternatively, you can set environment variables before running:

```bash
export DB_NAME=vehicle_parts
export DB_USER=vehicle_parts_user
export DB_PASSWORD="YourSecurePassword123!"
export MYSQL_ROOT_PASSWORD="YourSecureRootPassword123!"
./deploy/setup-database.sh
```

## Step 4: Configure Environment Variables

1. Copy the example environment file:

```bash
cp deploy/.env.production.example .env
```

2. Edit the `.env` file with your production values:

```bash
nano .env
```

**Important values to update:**
- `SECRET_KEY`: Generate a new secret key (use `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `ALLOWED_HOSTS`: Add your domain name and IP address
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`: Use the values from database setup
- `EMAIL_*`: Configure your email settings
- Other service configurations as needed

## Step 5: Configure Nginx

1. Copy the Nginx configuration:

```bash
sudo cp deploy/nginx.conf /etc/nginx/sites-available/vehicle-parts-api
```

2. Edit the configuration to add your domain name:

```bash
sudo nano /etc/nginx/sites-available/vehicle-parts-api
```

Replace `server_name _;` with your domain name or IP address.

3. Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/vehicle-parts-api /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default  # Remove default site
```

4. Test Nginx configuration:

```bash
sudo nginx -t
```

5. Start Nginx:

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

## Step 6: Configure Systemd Service

1. Copy the systemd service file:

```bash
sudo cp deploy/vehicle-parts-api.service /etc/systemd/system/
```

2. Reload systemd and enable the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable vehicle-parts-api
```

## Step 7: Deploy the Application

1. Run the deployment script:

```bash
./deploy/deploy.sh
```

This script will:
- Create/activate Python virtual environment
- Install dependencies
- Collect static files
- Run database migrations
- Set proper permissions
- Restart services

## Step 8: Set Up SSL Certificate (Optional but Recommended)

1. Install Certbot (already installed by setup script):

```bash
sudo certbot --nginx -d your-domain.com
```

2. Follow the prompts to complete SSL setup

3. Update the Nginx configuration to uncomment the HTTPS section and update domain names

4. Test SSL renewal:

```bash
sudo certbot renew --dry-run
```

## Step 9: Verify Deployment

1. Check service status:

```bash
sudo systemctl status vehicle-parts-api
sudo systemctl status nginx
sudo systemctl status mysql
```

2. Check application logs:

```bash
sudo tail -f /var/log/vehicle-parts-api/error.log
sudo tail -f /var/log/nginx/vehicle-parts-api-error.log
```

3. Test the API:

```bash
curl http://your-domain.com/api/
# or
curl http://your-ip-address/api/
```

## Step 10: Create Superuser

To access the Django admin panel:

```bash
cd /var/www/vehicle-parts-api
source venv/bin/activate
python manage.py createsuperuser
```

## Updating the Application

When you need to update the application:

1. Pull latest changes:

```bash
cd /var/www/vehicle-parts-api
git pull origin main
```

2. Run deployment script:

```bash
./deploy/deploy.sh
```

## Troubleshooting

### Application not starting

1. Check service status:
```bash
sudo systemctl status vehicle-parts-api
```

2. Check logs:
```bash
sudo journalctl -u vehicle-parts-api -f
sudo tail -f /var/log/vehicle-parts-api/error.log
```

3. Check if port 8000 is in use:
```bash
sudo netstat -tlnp | grep 8000
```

### Database connection issues

1. Verify MySQL is running:
```bash
sudo systemctl status mysql
```

2. Test database connection:
```bash
mysql -u vehicle_parts_user -p vehicle_parts
```

3. Check database credentials in `.env` file

### Nginx issues

1. Test Nginx configuration:
```bash
sudo nginx -t
```

2. Check Nginx error logs:
```bash
sudo tail -f /var/log/nginx/error.log
```

3. Check if Nginx is running:
```bash
sudo systemctl status nginx
```

### Permission issues

1. Fix ownership:
```bash
sudo chown -R www-data:www-data /var/www/vehicle-parts-api
sudo chmod -R 755 /var/www/vehicle-parts-api
```

2. Fix media/static permissions:
```bash
sudo chmod -R 775 /var/www/vehicle-parts-api/media
sudo chmod -R 775 /var/www/vehicle-parts-api/staticfiles
```

## Security Best Practices

1. **Firewall**: The setup script configures UFW. Only SSH and HTTP/HTTPS ports are open.

2. **MySQL Security**: 
   - Change the root password
   - Use strong passwords for database users
   - Don't expose MySQL to the internet

3. **Django Security**:
   - Set `DEBUG=False` in production
   - Use a strong `SECRET_KEY`
   - Keep `ALLOWED_HOSTS` restricted to your domain

4. **SSL/TLS**: Always use HTTPS in production

5. **Regular Updates**:
   ```bash
   sudo apt-get update && sudo apt-get upgrade -y
   ```

6. **Backup**: Set up regular database backups:
   ```bash
   # Add to crontab
   0 2 * * * mysqldump -u vehicle_parts_user -p'password' vehicle_parts > /backup/vehicle_parts_$(date +\%Y\%m\%d).sql
   ```

## Monitoring

- Check application logs: `/var/log/vehicle-parts-api/`
- Check Nginx logs: `/var/log/nginx/`
- Monitor system resources: `htop`
- Check disk space: `df -h`

## Backup and Restore

### Backup Database

```bash
mysqldump -u vehicle_parts_user -p vehicle_parts > backup.sql
```

### Restore Database

```bash
mysql -u vehicle_parts_user -p vehicle_parts < backup.sql
```

## Support

For issues or questions, check:
- Django logs: `/var/log/vehicle-parts-api/`
- Nginx logs: `/var/log/nginx/`
- System logs: `sudo journalctl -u vehicle-parts-api`

