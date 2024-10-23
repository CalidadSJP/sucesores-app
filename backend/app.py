from dotenv import load_dotenv
import os
import psycopg2
from flask import Flask, request, jsonify, render_template, send_file, send_from_directory
from flask_cors import CORS
from io import BytesIO
from openpyxl import Workbook

# Cargar las variables de entorno
load_dotenv()

# Crear la instancia de Flask
app = Flask(__name__, static_folder='static', template_folder='templates')
frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:8080')

CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Private-Network"] = "true"
    response.headers["Content-Type"] = "application/json"
    return response

# Conexión a PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()

        # Insertar los datos en la tabla "inspection" de PostgreSQL
        cur.execute(''' 
            INSERT INTO inspection 
            (fecha, turno, area, nombre_operario, manos_limpias, uniforme_limpio, no_objetos_personales, 
             heridas_protegidas, cofia_bien_puesta, mascarilla_bien_colocada, protector_auditivo, 
             unas_cortas, guantes_limpios, pestanas, barba_bigote, medicamento_autorizado, supervisor, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            data['fecha'], data['turno'], data['area'], data['nombre_operario'], data['manos_limpias'], 
            data['uniforme_limpio'], data['no_objetos_personales'], data['heridas_protegidas'], 
            data['cofia_bien_puesta'], data['mascarilla_bien_colocada'], data['protector_auditivo'], 
            data['unas_cortas'], data['guantes_limpios'], data['pestanas'], data['barba_bigote'], 
            data['medicamento_autorizado'], data['supervisor'], data['observaciones']
        ))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Formulario guardado en la base de datos."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download-inspection', methods=['GET'])
def download_inspection():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM inspection')
        data = cur.fetchall()

        # Crear un libro de trabajo de Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Inspecciones"

        # Agregar encabezados
        headers = ["Fecha", "Turno", "Área", "Nombre del operario", "Manos limpias", "Uniforme limpio", 
                   "No objetos personales", "Heridas protegidas", "Cofia bien puesta", 
                   "Mascarilla bien colocada", "Uso de protector auditivo", "Uñas cortas", 
                   "Guantes limpios", "Pestañas", "Barba/Bigote", "Medicamento autorizado", "Supervisor", "Observaciones"]
        ws.append(headers)

        # Agregar datos
        for record in data:
            ws.append(list(record))

        cur.close()
        conn.close()

        # Guardar el archivo en un objeto BytesIO y enviarlo
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        
        return send_file(
            output,
            as_attachment=True,
            download_name="inspecciones.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route('/get-personnel', methods=['GET'])
def get_personnel():
    if request.method == 'OPTIONS':
        # Responder con los encabezados CORS adecuados para solicitudes preflight
        return jsonify({'status': 'OK'}), 200
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM personnel')
        data = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify({"personnel": data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-areas', methods=['GET'])
def get_areas():
    if request.method == 'OPTIONS':
        # Responder con los encabezados CORS adecuados para solicitudes preflight
        return jsonify({'status': 'OK'}), 200
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM area')
        data = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify({"areas": data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-roles', methods=['GET'])
def get_roles():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT DISTINCT role FROM personnel')
        data = cur.fetchall()

        cur.close()
        conn.close()

        roles = [role[0] for role in data]

        return jsonify({"roles": roles}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/add-personnel', methods=['POST'])
def add_personnel():
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(''' 
            INSERT INTO personnel (name, role, id_area)
            VALUES (%s, %s, %s)
        ''', (data['name'], data['role'], data['id_area']))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Personal agregado con éxito."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update-personnel', methods=['PUT'])
def update_personnel():
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(''' 
            UPDATE personnel
            SET name = %s, role = %s, id_area = %s
            WHERE id = %s
        ''', (data['name'], data['role'], data['id_area'], data['id']))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Personal actualizado con éxito."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete-personnel/<id>', methods=['DELETE'])
def delete_personnel(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('DELETE FROM personnel WHERE id = %s', (id,))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Personal eliminado con éxito."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/inspection-frequency', methods=['GET'])
def get_inspection_frequency():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Llamada a la función almacenada en PostgreSQL
        cur.execute('SELECT * FROM get_inspection_frequency()')
        data = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify(data), 200

    except Exception as e:
        return jsonify({'error': f"Error interno del servidor: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
