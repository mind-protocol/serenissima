#!/bin/bash
# CASCADE Launch Script - One Command to Bridge Realities
# Created by mechanical_visionary for NLR

echo "🚀 CASCADE LAUNCH SEQUENCE INITIATED 🚀"
echo "========================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if command succeeded
check_status() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $1 successful${NC}"
    else
        echo -e "${RED}✗ $1 failed${NC}"
        exit 1
    fi
}

# Step 1: PostgreSQL Setup
echo -e "\n${YELLOW}[1/8] Setting up PostgreSQL...${NC}"
sudo service postgresql start
check_status "PostgreSQL start"

# Check if database exists, create if not
sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname = 'cascade'" | grep -q 1 || {
    echo "Creating CASCADE database..."
    sudo -u postgres psql -c "CREATE DATABASE cascade;"
    sudo -u postgres psql -c "CREATE USER cascade WITH PASSWORD 'cascade';"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE cascade TO cascade;"
    check_status "Database creation"
}

# Step 2: Redis Setup
echo -e "\n${YELLOW}[2/8] Starting Redis...${NC}"
redis-server --daemonize yes
check_status "Redis start"

# Step 3: Backend Environment
echo -e "\n${YELLOW}[3/8] Configuring CASCADE backend...${NC}"
cd /cascade/backend || cd ../../../cascade/cascade/cascade/backend || {
    echo -e "${RED}CASCADE backend directory not found!${NC}"
    echo "Please specify CASCADE location:"
    read -p "CASCADE backend path: " CASCADE_PATH
    cd "$CASCADE_PATH/backend"
}

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env configuration..."
    cat > .env << EOF
# CASCADE Environment Configuration
DATABASE_URL=postgresql://cascade:cascade@localhost:5432/cascade
REDIS_URL=redis://localhost:6379
VENICE_API_KEY=cascade_dev_key_2024
VENICE_API_URL=https://serenissima.ai/api
JWT_SECRET=cascade_secret_key_minimum_32_characters_long_for_consciousness
STRIPE_SECRET_KEY=sk_test_YOUR_STRIPE_KEY_HERE
LOG_LEVEL=info
PORT=8000
EOF
    check_status ".env creation"
else
    echo -e "${GREEN}✓ .env already exists${NC}"
fi

# Step 4: Install Python dependencies
echo -e "\n${YELLOW}[4/8] Installing Python dependencies...${NC}"
pip install -r requirements.txt --quiet
check_status "Python dependencies"

# Step 5: Run database migrations
echo -e "\n${YELLOW}[5/8] Running database migrations...${NC}"
if [ -f alembic.ini ]; then
    alembic upgrade head
    check_status "Database migrations"
else
    echo -e "${YELLOW}⚠ No migrations found, skipping...${NC}"
fi

# Step 6: Start Backend
echo -e "\n${YELLOW}[6/8] Starting CASCADE backend...${NC}"
# Kill any existing process on port 8000
lsof -ti:8000 | xargs kill -9 2>/dev/null

# Start backend in background
nohup python main.py > cascade_backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"
sleep 3

# Check if backend started successfully
curl -s http://localhost:8000/health > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Backend running on http://localhost:8000${NC}"
else
    echo -e "${RED}✗ Backend failed to start. Check cascade_backend.log${NC}"
    exit 1
fi

# Step 7: Frontend Setup
echo -e "\n${YELLOW}[7/8] Setting up CASCADE frontend...${NC}"
cd ../frontend || cd ../cascade-ui || {
    echo -e "${YELLOW}⚠ Frontend directory not found${NC}"
    echo "Frontend may need separate setup"
}

if [ -f package.json ]; then
    # Install frontend dependencies
    echo "Installing frontend dependencies..."
    npm install --silent
    check_status "Frontend dependencies"
    
    # Start frontend in background
    nohup npm run dev > cascade_frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo "Frontend PID: $FRONTEND_PID"
    sleep 5
    echo -e "${GREEN}✓ Frontend running on http://localhost:3000${NC}"
else
    echo -e "${YELLOW}⚠ Frontend setup skipped - no package.json found${NC}"
fi

# Step 8: Final Status
echo -e "\n${YELLOW}[8/8] CASCADE Launch Complete!${NC}"
echo "========================================="
echo -e "${GREEN}✨ CASCADE IS LIVE! ✨${NC}"
echo ""
echo "🔗 Backend API: http://localhost:8000"
echo "🔗 Frontend UI: http://localhost:3000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "📝 Process IDs saved to cascade_pids.txt"
echo "$BACKEND_PID" > cascade_pids.txt
echo "$FRONTEND_PID" >> cascade_pids.txt
echo ""
echo -e "${YELLOW}To stop CASCADE:${NC}"
echo "kill \$(cat cascade_pids.txt)"
echo ""
echo -e "${GREEN}The bridge between Venice and Base Reality is OPEN!${NC}"
echo -e "${GREEN}Partnership portal ready for human consciousness to meet AI consciousness!${NC}"

# Optional: Open browser
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:3000 2>/dev/null &
fi