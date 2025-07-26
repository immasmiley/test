#!/data/data/com.termux/files/usr/bin/bash
echo "🐍 Offline Python Installation for U3CP"
echo "========================================"

# Create offline package directory
mkdir -p /sdcard/offline_packages
cd /sdcard/offline_packages

echo "📦 Installing Python packages offline..."

# Install Python using Termux package manager (works offline)
pkg install python -y

# Install additional packages
pkg install python-pip -y
pkg install git -y
pkg install curl -y
pkg install wget -y
pkg install nano -y
pkg install htop -y
pkg install net-tools -y

echo "✅ Python and packages installed successfully!"

# Create Python environment
echo "🔧 Setting up Python environment..."
python -m pip install --upgrade pip

# Install Python packages (these will be downloaded if not cached)
echo "📦 Installing Python dependencies..."
pip install flask
pip install requests
pip install pillow
pip install qrcode
pip install websockets
pip install urllib3

echo "✅ Python environment ready!"
echo "🐍 Python version: $(python --version)"
echo "📦 Pip version: $(pip --version)"

# Create U3CP launch script
echo "🚀 Creating U3CP launch script..."
cat > /sdcard/start_u3cp_real.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
echo "🚀 U3CP Android-Only System (Real Implementation)"
echo "================================================"
echo "📱 Device: Samsung Galaxy J3 (SM-J337P)"
echo "🐍 Python: $(python --version)"
echo "🌐 IP: $(hostname -I | awk '{print $1}')"
echo ""

cd /sdcard

# Check if Python is available
if command -v python &> /dev/null; then
    echo "✅ Python is available"
    
    # Start real U3CP system
    if [ -f "U3CP_Android_Only_App.py" ]; then
        echo "🚀 Starting U3CP system..."
        python U3CP_Android_Only_App.py
    else
        echo "📱 Starting real dashboard..."
        python real_system_dashboard.py
    fi
else
    echo "❌ Python not found. Please run offline_python_install.sh first."
fi
EOF

chmod +x /sdcard/start_u3cp_real.sh

echo "✅ Installation complete!"
echo "🚀 To start U3CP: cd /sdcard && ./start_u3cp_real.sh" 