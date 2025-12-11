import sys
import os
from dotenv import load_dotenv

# Añade el directorio de tu aplicación al path
sys.path.insert(0, "D:/Projects/sucesores-app/backend")

# Cargar el archivo .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


# Importa tu aplicación Flask
from app import app as application  # Cambiar 'app' si el nombre del archivo principal es diferente
