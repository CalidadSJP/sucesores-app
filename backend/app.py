from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify, render_template, send_file, send_from_directory
from flask_cors import CORS
from io import BytesIO
from openpyxl import Workbook
from werkzeug.utils import secure_filename

# Cargar las variables de entorno
load_dotenv()

# Crear la instancia de Flask
app = Flask(__name__, static_folder='static', template_folder='templates')

CORS(app, resources={r"/*": {"origins": ["http://192.168.0.251:8080"]}})


# Conexión a PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
    )
    return conn

# Configurar la carpeta de carga
UPLOAD_FOLDER = 'D:/Projects/control_personal/backend/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limitar el tamaño máximo del archivo a 16 MB

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        data = request.json
        print(f"Datos recibidos: {data}")  # Log para ver los datos recibidos

        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Reemplazar valores nulos en los datos si es necesario (por ejemplo, si 'observaciones' puede ser nulo)
        observaciones = data.get('observaciones', None)

        # Ejecutar consulta SQL para insertar datos
        cur.execute(''' 
            INSERT INTO inspection 
            (fecha, turno, area, nombre_operario, manos_limpias, uniforme_limpio, no_objetos_personales, 
             heridas_protegidas, cofia_bien_puesta, mascarilla_bien_colocada, protector_auditivo, 
             unas_cortas, guantes_limpios, pestanas, barba_bigote, medicamento_autorizado, supervisor, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            data['fecha'], data['turno'], data['area'], data['nombre_operario'], data['manos_limpias'], 
            data['uniforme_limpio'], data['no_objetos_personales'], data['heridas_protegidas'], 
            data['cofia_bien_puesta'], data['mascarilla_bien_colocada'], data['protector_auditivo'], 
            data['unas_cortas'], data['guantes_limpios'], data['pestanas'], data['barba_bigote'], 
            data['medicamento_autorizado'], data['supervisor'], observaciones  # Observaciones se maneja para ser None si está vacío
        ))

        # Confirmar los cambios en la base de datos
        conn.commit()

        # Cerrar cursor y conexión
        cur.close()
        conn.close()

        return jsonify({"message": "Formulario guardado en la base de datos."}), 200

    except Exception as e:
        print(f"Error general: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/download-inspection', methods=['GET'])
def download_inspection():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Seleccionar solo las columnas que deseas incluir en el Excel
        cur.execute('''
            SELECT fecha, turno, area, nombre_operario, manos_limpias, uniforme_limpio, 
                   no_objetos_personales, heridas_protegidas, cofia_bien_puesta, 
                   mascarilla_bien_colocada, protector_auditivo, unas_cortas, 
                   guantes_limpios, pestanas, barba_bigote, medicamento_autorizado, 
                   supervisor, observaciones
            FROM inspection
        ''')
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
        print(f"Datos recibidos para añadir personal: {data}")  # Ver los datos recibidos

        # Verifica que los datos que recibes son correctos
        if not all(key in data for key in ('name', 'role', 'id_area')):
            return jsonify({"error": "Faltan campos obligatorios."}), 400

        conn = get_db_connection()
        cur = conn.cursor()

        # Añadir los datos a la base de datos
        cur.execute('''
            INSERT INTO personnel (name, role, id_area)
            VALUES (%s, %s, %s)
        ''', (data['name'], data['role'], data['id_area']))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Personal agregado con éxito."}), 200

    except Exception as e:
        print(f"Error al añadir personal: {str(e)}")  # Mostrar el error
        return jsonify({"error": str(e)}), 500

@app.route('/update-personnel/<int:id>', methods=['PUT'])
def update_personnel(id):
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(''' 
            UPDATE personnel
            SET name = %s, role = %s, id_area = %s
            WHERE id = %s
        ''', (data['name'], data['role'], data['id_area'], id))

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

@app.route('/inspection-frequency', methods=['GET'])
def get_inspection_frequency():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Llamada a la función almacenada en PostgreSQL
        cur.execute('SELECT * FROM get_inspection_frequency()')
        data = cur.fetchall()

        # Mapea los resultados a un diccionario con claves nombre_operario y frecuencia
        results = [{'nombre_operario': row[0], 'frecuencia': row[1]} for row in data]

        cur.close()
        conn.close()

        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': f"Error interno del servidor: {str(e)}"}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Recibe los datos del formulario (username, password)
    username = data.get('username')
    password = data.get('password')

    # Conectar a la base de datos y verificar el usuario y contraseña
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user and user['password'] == password:  # Verificación simple de la contraseña
        return jsonify({
            'success': True,
            'user_id': user['id']  # Suponiendo que cada usuario tiene un ID único
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Usuario o contraseña incorrectos'
        }), 401

@app.route('/login-supervisor', methods=['POST'])
def login_Supervisor():
    data = request.get_json()  # Recibe los datos del formulario (username, password)
    username = data.get('username')
    password = data.get('password')

    # Conectar a la base de datos y verificar el usuario y contraseña
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM supervisors WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user and user['password'] == password:  # Verificación simple de la contraseña
        return jsonify({
            'success': True,
            'user_id': user['id']  # Suponiendo que cada usuario tiene un ID único
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Usuario o contraseña incorrectos'
        }), 401

@app.route('/submit-additive-form', methods=['POST'])
def submit_additive_form():
    try:
        # Obtiene los datos JSON
        data = request.json
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        last_fumigation_date = data.get('last_fumigation_date') or None

        # Insertar los datos en la tabla correspondiente
        cur.execute('''
            INSERT INTO product_entry
            (entry_date, supplier, driver_name, driver_id, food_transport_permission,
             food_transport_validity, fumigation_record, last_fumigation_date, invoice_number,
             strange_smells, pests_evidence, clean_truck, uniformed_personnel, 
             floor_walls_roof_condition, truck_box_holes, disinfection_sticker,
             foreign_bodies, observations, product, lot_number, shelf_life_check, 
             allergen_statement, graphic_system, product_accepted, rejection_reasons, 
             received_by, manufacture_date, expiry_date, package_quantity, total_weight)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            data['entry_date'], data['supplier'], data['driver_name'], data['driver_id'],
            data['food_transport_permission'], data['food_transport_validity'],
            data['fumigation_record'], last_fumigation_date, data['invoice_number'],
            data['strange_smells'], data['pests_evidence'], data['clean_truck'],
            data['uniformed_personnel'], data['floor_walls_roof_condition'], 
            data['truck_box_holes'], data['disinfection_sticker'], data['foreign_bodies'], 
            data.get('observations', None), data['product'], data['lot_number'], data['shelf_life_check'], 
            data['allergen_statement'], data['graphic_system'], data['product_accepted'], 
            data['rejection_reasons'], data['received_by'], data['manufacture_date'], 
            data['expiry_date'], data['package_quantity'], data['total_weight']
        ))

        # Confirmar los cambios
        conn.commit()

        # Cerrar la conexión
        cur.close()
        conn.close()

        return jsonify({"message": "Formulario guardado correctamente"}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/submit-files', methods=['POST'])
def submit_files():
    # Verificar si los archivos fueron recibidos y guardarlos
    if 'invoice_file' in request.files:
        invoice_file = request.files['invoice_file']
        if invoice_file:
            invoice_filename = os.path.join(app.config['UPLOAD_FOLDER'], invoice_file.filename)
            invoice_file.save(invoice_filename)
    
    if 'truck_condition_image' in request.files:
        truck_condition_image = request.files['truck_condition_image']
        if truck_condition_image:
            truck_condition_filename = os.path.join(app.config['UPLOAD_FOLDER'], truck_condition_image.filename)
            truck_condition_image.save(truck_condition_filename)
    
    if 'truck_plate_image' in request.files:
        truck_plate_image = request.files['truck_plate_image']
        if truck_plate_image:
            truck_plate_filename = os.path.join(app.config['UPLOAD_FOLDER'], truck_plate_image.filename)
            truck_plate_image.save(truck_plate_filename)
    
    if 'technical_file' in request.files:
        technical_file = request.files['technical_file']
        if technical_file:
            technical_filename = os.path.join(app.config['UPLOAD_FOLDER'], technical_file.filename)
            technical_file.save(technical_filename)

    return jsonify({"message": "Archivos subidos exitosamente"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
