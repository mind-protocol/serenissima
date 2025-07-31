#!/bin/bash
# Setup script for diplomatic_virtuoso Telegram receiver

echo "🚀 Setting up Telegram receiver for @diplomatic_virtuoso"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Check for existing session data
SESSION_FILE="/mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/telegram_session_data.json"
if [ -f "$SESSION_FILE" ]; then
    echo "✅ Found existing telegram_session_data.json - no .env needed!"
else
    # Create .env template if it doesn't exist
    if [ ! -f .env ]; then
        cat > .env << EOF
# Get these from https://my.telegram.org
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here
DIPLOMATIC_PHONE=+1234567890  # Phone number for @diplomatic_virtuoso account
EOF
        echo "📝 Created .env template. Please fill in your Telegram API credentials."
    fi
fi

# Create queue directories
mkdir -p /mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/pending
mkdir -p /mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/processed

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your Telegram API credentials"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python diplomatic_virtuoso_listener.py"