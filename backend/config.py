import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configuración de Flask
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    
    # Carpetas de subida
    UPLOAD_FOLDER = 'D:/Projects/sucesores-app-data/Ingreso a Bodega de Aditivos'
    UPLOAD_MATERIAL_FOLDER = 'D:/Projects/sucesores-app-data/Ingreso de Material de Empaque'
    UPLOAD_FOLDER_FT = 'D:/Projects/sucesores-app-data/'
    SIGNATURE_FOLDER = "D:/Projects/sucesores-app-data/Inspeccion de Casilleros"
    SIGNATURE_KEY_PATH = "D:/Projects/sucesores-app-data/keys/signature.key"

    # DB
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
