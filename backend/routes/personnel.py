from flask import Blueprint, request, jsonify
from core.database import get_db_connection
from openpyxl import Workbook
from io import BytesIO
from flask import request, jsonify, send_file
from psycopg2.extras import RealDictCursor
from datetime import time
from routes.faults_penalties import add_fault



personnel_bp = Blueprint("personnel", __name__)

#PAGINA FORMULARIO DEL PERSONAL

@personnel_bp.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        from flask import current_app
        data = request.json
        print(f"Datos recibidos /submit-form: {data}")

        conn = get_db_connection()
        cur = conn.cursor()

        observaciones = data.get('observaciones', None)

        # =============================
        # 1) INSERTAR INSPECCIÓN
        # =============================
        cur.execute(''' 
            INSERT INTO inspection 
            (fecha, turno, area, nombre_operario, manos_limpias, uniforme_limpio, no_objetos_personales, 
             heridas_protegidas, cofia_bien_puesta, mascarilla_bien_colocada, protector_auditivo, 
             unas_cortas, guantes_limpios, pestanas, barba_bigote, medicamento_autorizado, supervisor, observaciones, hora)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            data['fecha'], data['turno'], data['area'], data['nombre_operario'], data['manos_limpias'], 
            data['uniforme_limpio'], data['no_objetos_personales'], data['heridas_protegidas'], 
            data['cofia_bien_puesta'], data['mascarilla_bien_colocada'], data['protector_auditivo'], 
            data['unas_cortas'], data['guantes_limpios'], data['pestanas'], data['barba_bigote'], 
            data['medicamento_autorizado'], data['supervisor'], observaciones, data['hora']
        ))

        # =============================
        # 2) OBTENER EL ID DEL OPERARIO
        # =============================
        cur.execute("SELECT id FROM personnel WHERE name = %s", (data['nombre_operario'],))
        result = cur.fetchone()
        if not result:
            raise Exception(f"No se encontró el personal con nombre: {data['nombre_operario']}")

        personnel_id = result[0]

        conn.commit()
        cur.close()
        conn.close()


        # =============================
        # 3) REGISTRAR FALTAS USANDO /faults
        # =============================
        campos_a_verificar = {
            'manos_limpias': 'Manos limpias',
            'uniforme_limpio': 'Uniforme limpio',
            'no_objetos_personales': 'Objetos personales en el área',
            'heridas_protegidas': 'Heridas protegidas',
            'cofia_bien_puesta': 'Cofia bien puesta',
            'mascarilla_bien_colocada': 'Mascarilla bien colocada',
            'protector_auditivo': 'Protector auditivo',
            'unas_cortas': 'Uñas cortas',
            'guantes_limpios': 'Guantes limpios',
            'pestanas': 'Pestañas sin rimel',
            'barba_bigote': 'Barba o bigote',
            'medicamento_autorizado': 'Medicamento autorizado'
        }

        for campo, label in campos_a_verificar.items():
            if data.get(campo) == 'NO CUMPLE':

                descripcion = f"{label}: NO CUMPLE"
                supervisor = (data.get('supervisor') or '').strip().upper()

                payload_falta = {
                    "personnel_id": personnel_id,
                    "description": descripcion,
                    "responsible": supervisor,
                    "date": data["fecha"],
                    "fault_type_id": 1,
                    "severity": "LEVE"
                }

                print(f"[DEBUG] Registrando falta desde submit-form: {payload_falta}")

                # Llamada interna al endpoint /faults
                with current_app.test_request_context(
                    '/faults', method='POST', json=payload_falta
                ):
                    add_fault()

        return jsonify({"message": "Formulario registrado correctamente."}), 200

    except Exception as e:
        print(f"[ERROR] en /submit-form: {str(e)}")
        return jsonify({"error": str(e)}), 500

@personnel_bp.route('/download-inspection', methods=['GET']) #Método para descargar el registro de inpección del personal
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
            ORDER BY fecha DESC
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

#PAGINA DE GESTIÓN DE PERSONAL

@personnel_bp.route('/get-personnel', methods=['GET']) # Obtener la lista del personal
def get_personnel():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM personnel ORDER BY name ASC')
        data = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify({"personnel": data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@personnel_bp.route('/get-areas', methods=['GET']) # Listar areas de la planta
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

@personnel_bp.route('/get-roles', methods=['GET'])# Listar cargos del personal
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

@personnel_bp.route('/add-personnel', methods=['POST']) # Añadir una persona al personal
def add_personnel():
    try:
        data = request.json
        print(f"Datos recibidos para añadir personal: {data}")  # Ver los datos recibidos

        # Verifica que los datos que recibes son correctos
        if not all(key in data for key in ('name', 'role', 'id_area', 'identifier')):
            return jsonify({"error": "Faltan campos obligatorios."}), 400

        conn = get_db_connection()
        cur = conn.cursor()

        # Añadir los datos a la base de datos
        cur.execute('''
            INSERT INTO personnel (name, role, id_area, identifier)
            VALUES (%s, %s, %s, %s)
        ''', (data['name'], data['role'], data['id_area'], data['identifier']))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Personal agregado con éxito."}), 200

    except Exception as e:
        print(f"Error al añadir personal: {str(e)}")  # Mostrar el error
        return jsonify({"error": str(e)}), 500

@personnel_bp.route('/update-personnel/<int:id>', methods=['PUT']) # Editar informacion de una persona 
def update_personnel(id):
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(''' 
            UPDATE personnel
            SET name = %s, role = %s, id_area = %s, identifier = %s
            WHERE id = %s
        ''', (data['name'], data['role'], data['id_area'], data['identifier'], id))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Personal actualizado con éxito."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@personnel_bp.route('/delete-personnel/<id>', methods=['DELETE']) # Eliminar una persona del personal
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


#PAGINA FRECUENCIA DEL PERSONAL

@personnel_bp.route('/inspection-frequency', methods=['GET'])
def get_inspection_frequency():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM get_inspection_frequency()')
        data = cur.fetchall()

        results = [
            {
                'nombre_operario': row[0],
                'area': row[1], 
                'frecuencia': row[2],
                'ultima_inspeccion': row[3].strftime('%Y-%m-%d') if row[3] else None
            }
            for row in data
        ]

        cur.close()
        conn.close()

        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': f"Error interno del servidor: {str(e)}"}), 500


#PAGINA DE REVISION DE INSPECCION DEL PERSONAL

@personnel_bp.route('/inspection-register', methods=['GET'])
def inspection_register():
    try:
        print("🔍 Entrando al endpoint /inspection-register")
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM inspection;")
        products = cursor.fetchall()
        cursor.close()
        connection.close()

        # Convertir campos de tipo 'time' a string
        for row in products:
            for key, value in row.items():
                if isinstance(value, time):
                    row[key] = value.strftime('%H:%M')

        print("✅ Consulta realizada correctamente")
        return jsonify(products)
    except Exception as e:
        print(f"❌ Error en /inspection-register: {e}")
        return jsonify({"error": str(e)}), 500

@personnel_bp.route('/inspection-register/<int:id>', methods=['PUT']) # Editar registro | Ingreso de material de empaque
def update_inspection_register(id):
    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Generar los campos dinámicamente
    update_fields = ", ".join([f"{key} = %s" for key in data.keys()])
    values = list(data.values()) + [id]
    
    query = f"UPDATE inspection SET {update_fields} WHERE id = %s;"
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Registro actualizado exitosamente."})

@personnel_bp.route('/inspection-register/<int:id>', methods=['DELETE']) # Eliminar registro | Ingreso de material de empaque
def delete_inspection_register(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM inspection WHERE id = %s;", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Registro eliminado exitosamente."})


#PAGINA DE LOGIN 

@personnel_bp.route('/login', methods=['POST']) # Comparar informacion para el inicio de sesión
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

@personnel_bp.route('/login-supervisor', methods=['POST']) # Comparar informacion para el inicio de sesión (Teniendo en cuenta el area)
def login_supervisor():
    data = request.get_json()  # Recibe los datos del formulario (username, password, area)
    username = data.get('username')
    password = data.get('password')
    user_area = data.get('area')  # El área fija de la página, enviada automáticamente desde el frontend

    # Conectar a la base de datos y verificar el usuario
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM users WHERE username = %s AND area = %s", (username, user_area))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        return jsonify({
            'success': False,
            'message': 'Usuario no encontrado'
        }), 401

    # Verificar contraseña y área
    if user['password'] == password and user['area'] == user_area:
        return jsonify({
            'success': True,
            'user_id': user['id'],  # Suponiendo que cada usuario tiene un ID único
            'message': f"Bienvenido, {username}",  # Genera el token para la sesión
            'area': user['area']
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Usuario, contraseña o área incorrectos'
        }), 401
