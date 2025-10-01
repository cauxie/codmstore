#!/usr/bin/env bash
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
