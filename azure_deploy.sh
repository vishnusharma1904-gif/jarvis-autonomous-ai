#!/bin/bash

# ========================================
# Jarvis AI - Azure Deployment Script
# ========================================

set -e  # Exit on error

echo "🚀 Starting Jarvis AI Deployment on Azure..."

# ========================================
# 1. Update System
# ========================================
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# ========================================
# 2. Install Essential Tools
# ========================================
echo "🔧 Installing essential tools..."
sudo apt install -y git curl wget build-essential software-properties-common

# ========================================
# 3. Install Python (Uses default system Python, 3.12 on Ubuntu 24.04)
# ========================================
echo "🐍 Installing Python..."
sudo apt install -y python3 python3-venv python3-pip python3-dev

# ========================================
# 4. Install Node.js 20.x
# ========================================
echo "📗 Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# ========================================
# 5. Install Ollama
# ========================================
echo "🤖 Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
sudo systemctl start ollama
sudo systemctl enable ollama

# Wait for Ollama to start
sleep 5

# Pull capable model (Upgraded for 16GB RAM VM)
echo "📥 Pulling AI model (llama3.1:8b)..."
ollama pull llama3.1:8b

# ========================================
# 6. Clone Jarvis Repository
# ========================================
echo "📂 Cloning Jarvis repository..."
cd ~
if [ -d "jarvis-autonomous-ai" ]; then
    echo "Repository already exists, updating..."
    cd jarvis-autonomous-ai
    git pull
else
    git clone https://github.com/vishnusharma1904-gif/jarvis-autonomous-ai.git
    cd jarvis-autonomous-ai
fi

# ========================================
# 7. Set Up Backend
# ========================================
echo "⚙️ Setting up backend..."
cd ~/jarvis-autonomous-ai/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env << 'EOF'
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=llama3.1:8b

# Server Configuration
HOST=0.0.0.0
PORT=5000

# Optional: Add your API keys here
# GROQ_API_KEY=your_key_here
# GEMINI_API_KEY=your_key_here
EOF
fi

# Create data directories
mkdir -p data/audio data/uploads data/chroma_db data/sandbox

# ========================================
# 8. Set Up Frontend
# ========================================
echo "🎨 Setting up frontend..."
cd ~/jarvis-autonomous-ai/frontend

# Install dependencies
npm install

# Build for production
npm run build

# ========================================
# 9. Install Nginx
# ========================================
echo "🌐 Installing and configuring Nginx..."
sudo apt install -y nginx

# Configure Nginx
sudo tee /etc/nginx/sites-available/jarvis << 'EOF'
server {
    listen 80;
    server_name _;

    # Frontend
    root /home/azureuser/jarvis-autonomous-ai/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket support
    location /ws {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
    }
}
EOF

# Enable site
sudo ln -sf /etc/nginx/sites-available/jarvis /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test and restart Nginx
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx

# ========================================
# 10. Create Systemd Service for Backend
# ========================================
echo "🔄 Creating systemd service..."
sudo tee /etc/systemd/system/jarvis-backend.service << 'EOF'
[Unit]
Description=Jarvis AI Backend
After=network.target ollama.service

[Service]
Type=simple
User=azureuser
WorkingDirectory=/home/azureuser/jarvis-autonomous-ai/backend
Environment="PATH=/home/azureuser/jarvis-autonomous-ai/backend/venv/bin"
ExecStart=/home/azureuser/jarvis-autonomous-ai/backend/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start service
sudo systemctl daemon-reload
sudo systemctl enable jarvis-backend
sudo systemctl start jarvis-backend

# ========================================
# 11. Configure Firewall (if enabled)
# ========================================
echo "🔥 Configuring firewall..."
if sudo ufw status | grep -q "Status: active"; then
    sudo ufw allow 22/tcp   # SSH
    sudo ufw allow 80/tcp   # HTTP
    sudo ufw allow 443/tcp  # HTTPS
    sudo ufw reload
fi

# ========================================
# 12. Display Status
# ========================================
echo ""
echo "========================================="
echo "✅ Deployment Complete!"
echo "========================================="
echo ""
echo "📊 Service Status:"
sudo systemctl status jarvis-backend --no-pager -l | head -n 10
echo ""
echo "🌐 Access Jarvis at:"
echo "   http://$(curl -s ifconfig.me)"
echo ""
echo "🔍 Useful Commands:"
echo "   Check backend logs:  sudo journalctl -u jarvis-backend -f"
echo "   Restart backend:     sudo systemctl restart jarvis-backend"
echo "   Check Nginx logs:    sudo tail -f /var/log/nginx/error.log"
echo "   Interact with model: ollama run llama3.1:8b"
echo ""
echo "📁 Project location: /home/azureuser/jarvis-autonomous-ai"
echo "========================================="
