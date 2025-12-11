import os
from flask import Flask, request, render_template
from flask_cors import CORS
from config import Config
from routes import register_routes

#Reiniciar servicio: httpd.exe -k restart -n "sucesores-app"

# Crear la app Flask
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object(Config)

# Configurar CORS
CORS(app, resources={r"/*": {"origins": ["http://192.168.0.251:8080"]}})

# Registrar todas las rutas
register_routes(app)

# Ruta base
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
