import os
import django
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command # <--- Esto arregla el error de 'call_command'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'managejaasc.settings')

# 1. Inicializamos Django
django.setup()

# 2. Creamos la aplicación
application = get_wsgi_application()

# 3. Ejecutamos migraciones PRIMERO
try:
    print("Iniciando migraciones...")
    call_command('migrate', interactive=False)
    print("Migraciones completadas.")
except Exception as e:
    print(f"Error en migraciones: {e}")

# 4. Creamos el superusuario DESPUÉS (Solo si no existe)
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'junta@jaassc.org', '010325')
        print("Superusuario creado.")
except Exception as e:
    print(f"Error creando superusuario: {e}")

# 5. Punto de entrada para Vercel
app = application