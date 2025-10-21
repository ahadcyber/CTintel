#!/bin/bash
# Production startup script for Linux/Mac

echo "🚀 Starting CTI Dashboard in production mode..."

# Create logs directory
mkdir -p logs

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "Please create .env file with required configuration"
    exit 1
fi

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Set production environment
export FLASK_ENV=production

# Check MongoDB connection
echo "🔍 Checking MongoDB connection..."
python -c "from db.mongo import db_manager; exit(0 if db_manager.connect() else 1)"
if [ $? -ne 0 ]; then
    echo "❌ MongoDB connection failed"
    exit 1
fi
echo "✅ MongoDB connected"

# Start with Gunicorn
echo "🌟 Starting Gunicorn server..."
gunicorn \
    --config gunicorn_config.py \
    --bind 0.0.0.0:${PORT:-5000} \
    --workers ${WORKERS:-4} \
    --timeout 120 \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    wsgi:application

# Alternative: Start with Waitress (Windows-friendly)
# echo "🌟 Starting Waitress server..."
# waitress-serve --port=${PORT:-5000} --threads=4 wsgi:application
