"""
WSGI config for managejaasc project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'managejaasc.settings')

application = get_wsgi_application()

try:
    print("Iniciando migraciones...")
    call_command('migrate', interactive=False)
except Exception as e:
    print(f"Error en migraciones: {e}")

from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'junta', '010325')

app = application