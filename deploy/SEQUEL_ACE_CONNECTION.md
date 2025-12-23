# Connecting to MySQL Database using Sequel Ace

## Method 1: SSH Tunnel (Recommended - Secure)

Since MySQL is running on `localhost` on the server, you need to use SSH tunneling to connect.

### Step 1: Create SSH Tunnel

Open Terminal and run:

```bash
ssh -i ~/.ssh/id_ed25519_digitalocean -L 3307:localhost:3306 root@206.189.137.79 -N
```

**Explanation:**
- `-L 3307:localhost:3306` - Creates a tunnel from your local port 3307 to the server's localhost:3306
- `-N` - Don't execute any commands, just keep the tunnel open
- Keep this terminal window open while using Sequel Ace

### Step 2: Configure Sequel Ace

1. Open **Sequel Ace**
2. Click **"Add Favorite"** or **"+"** button
3. Fill in the connection details:

   **Connection Settings:**
   - **Name**: `Vehicle Parts API (Production)`
   - **Host**: `127.0.0.1` (or `localhost`)
   - **Username**: `vehicle_parts_user`
   - **Password**: `your-secure-database-password-here` (check .env file)
   - **Database**: `vehicle_parts`
   - **Port**: `3307` (the local port from the SSH tunnel)
   - **SSH Host**: `206.189.137.79`
   - **SSH User**: `root`
   - **SSH Key**: `~/.ssh/id_ed25519_digitalocean`
   - **SSH Port**: `22`

4. Click **"Test Connection"** to verify
5. Click **"Add to Favorites"** to save

### Alternative: Use Sequel Ace's Built-in SSH Tunnel

Sequel Ace has built-in SSH tunneling support:

1. Open Sequel Ace
2. Click **"Add Favorite"**
3. Fill in:

   **MySQL Settings:**
   - **Name**: `Vehicle Parts API`
   - **Host**: `localhost` (or `127.0.0.1`)
   - **Username**: `vehicle_parts_user`
   - **Password**: `VehicleParts123!`
   - **Database**: `vehicle_parts`
   - **Port**: `3306`
   - **SSL**: Disable or set to "None" (not required for localhost via SSH tunnel)

   **SSH Settings (Enable SSH Tunnel):**
   - Check **"Use SSH"**
   - **SSH Host**: `206.189.137.79`
   - **SSH User**: `root`
   - **SSH Key**: Click "Choose..." and select `~/.ssh/id_ed25519_digitalocean`
   - **SSH Port**: `22`

4. Click **"Test Connection"**
5. Click **"Add to Favorites"**

## Method 2: Direct Connection (Not Recommended - Requires MySQL Remote Access)

⚠️ **Security Warning**: This exposes MySQL to the internet. Only use for development/testing.

### Enable Remote MySQL Access (on server):

```bash
ssh -i ~/.ssh/id_ed25519_digitalocean root@206.189.137.79

# Edit MySQL config
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf

# Find and comment out or change:
# bind-address = 127.0.0.1
# to:
# bind-address = 0.0.0.0

# Restart MySQL
sudo systemctl restart mysql

# Grant remote access (optional, for specific IP)
mysql -u root -p
GRANT ALL PRIVILEGES ON vehicle_parts.* TO 'vehicle_parts_user'@'%' IDENTIFIED BY 'password';
FLUSH PRIVILEGES;
EXIT;
```

### Then in Sequel Ace:
- **Host**: `206.189.137.79`
- **Port**: `3306`
- **Username**: `vehicle_parts_user`
- **Password**: `your-secure-database-password-here`
- **Database**: `vehicle_parts`

## Quick Reference

### Database Credentials:
- **Host**: `localhost` (via SSH tunnel) or `206.189.137.79` (direct)
- **Port**: `3306`
- **Database**: `vehicle_parts`
- **Username**: `vehicle_parts_user`
- **Password**: `VehicleParts123!`
- **SSL**: Disabled (using mysql_native_password authentication)

### To get the actual password:
```bash
ssh -i ~/.ssh/id_ed25519_digitalocean root@206.189.137.79
cd /var/www/vehicle-parts-api
cat .env | grep DB_PASSWORD
```

## Troubleshooting

### Connection Refused
- Make sure the SSH tunnel is running (Method 1)
- Check if MySQL is running: `sudo systemctl status mysql` on server

### Authentication Failed
- Verify the password in `.env` file
- Check if the user exists: `mysql -u root -p -e "SELECT User, Host FROM mysql.user WHERE User='vehicle_parts_user';"`

### Can't Connect via SSH
- Verify SSH key permissions: `chmod 600 ~/.ssh/id_ed25519_digitalocean`
- Test SSH connection: `ssh -i ~/.ssh/id_ed25519_digitalocean root@206.189.137.79`

