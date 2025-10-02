#!/usr/bin/env bash
<<<<<<< HEAD
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
=======
# build.sh
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('=== SUPERUSER CREATED ===')
    print('Username: admin')
    print('Password: admin123')
    print('=== CHANGE PASSWORD IMMEDIATELY ===')
else:
    print('Superuser already exists')
"

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Build completed successfully!"
>>>>>>> f258faa3926d10b85ec5ca34f809db4866899fff
