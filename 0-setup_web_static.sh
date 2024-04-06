#!/usr/bin/env bash

# Install Nginx if not already installed
sudo apt-get update
sudo apt-get install -y nginx

# Create necessary directories
sudo mkdir -p /data/web_static/{releases/test,shared}

# Create fake HTML file for testing
echo "<html><head><title>Test Page</title></head><body>This is a test page</body></html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create or recreate symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ to ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
nginx_config="/etc/nginx/sites-available/default"
sudo sed -i '/^server {/a \ \ \ \ location /hbnb_static/ {\n\ \ \ \ \ \ alias /data/web_static/current/;\n\ \ \ \ \ \ index index.html;\n\ \ \ \ }' $nginx_config

# Restart Nginx
sudo service nginx restart

exit 0
