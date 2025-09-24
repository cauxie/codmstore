#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "🚀 Starting deployment process..."

# 1. Install Python packages
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# 2. Setup database structure
echo "🗄️ Setting up database..."
python manage.py migrate

# 3. Create admin user
echo "👑 Creating admin account..."
python manage.py create_admin

# 4. Collect CSS/JS files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

echo "🎉 Deployment completed successfully!"