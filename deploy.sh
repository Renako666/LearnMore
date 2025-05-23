#!/bin/bash

# Exit on error
set -e

echo "Starting deployment..."

# Update system
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages if not installed
echo "Installing required packages..."
sudo apt install -y python3-pip python3-venv nginx nodejs npm gzip

# Create and activate virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt
pip install gunicorn

# Install Node.js dependencies and build frontend
echo "Setting up frontend..."
cd app
npm install
npm run build
cd ..

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Database migrations
echo "Running database migrations..."
python manage.py migrate

# Setting database file permissions
echo "Setting database file permissions..."
sudo chown -R ubuntu:ubuntu .
chmod 644 db.sqlite3
chmod 755 backups logs

# Setting database backup
echo "Setting up database backup..."
chmod +x backup_db.sh
# Adding daily backup to crontab
(crontab -l 2>/dev/null; echo "0 2 * * * $(pwd)/backup_db.sh") | crontab -

# Setup Nginx
echo "Configuring Nginx..."
sudo cp learning_platform_nginx.conf /etc/nginx/sites-available/learning_platform
sudo ln -sf /etc/nginx/sites-available/learning_platform /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Setup Gunicorn service
echo "Setting up Gunicorn service..."
sudo tee /etc/systemd/system/gunicorn.service << EOF
[Unit]
Description=Gunicorn daemon for Django Learning Platform
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 learning_platform.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Start Gunicorn
echo "Starting Gunicorn service..."
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# Setup PM2 for Next.js
echo "Setting up PM2 for Next.js..."
sudo npm install -g pm2
cd app
pm2 start npm --name "nextjs" -- start
pm2 save
pm2 startup
cd ..

echo "Deployment completed successfully!"
echo "Your application is running at http://13.54.212.183"
echo "Database backups will be created daily at 2 AM" 