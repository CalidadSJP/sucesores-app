import sys
import os
from dotenv import load_dotenv

# Añade el directorio de tu aplicación al path
sys.path.insert(0, "D:/Projects/control_personal/backend")

# Cargar el archivo .env si existe
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


# Importa tu aplicación Flask
from app import app as application  # Cambia 'app' si el nombre de tu archivo principal es diferente
