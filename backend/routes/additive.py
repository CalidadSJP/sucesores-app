from flask import Blueprint, request, jsonify
from core.database import get_db_connection
from openpyxl import Workbook
from io import BytesIO
from flask import request, jsonify, send_file, send_from_directory, abort, current_app
from psycopg2.extras import RealDictCursor
from config import Config
import os
from datetime import datetime

additive_bp = Blueprint("additive", __name__)


#PAGINA "FORMULARIO DE ADITIVOS"

@additive_bp.route('/submit-additive-form', methods=['POST']) # Subir Formulario de Ingreso de Aditivos 
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
             foreign_bodies, product, lot_number, shelf_life_check, 
             allergen_statement, graphic_system, product_accepted, rejection_reasons, 
             received_by, manufacture_date, expiry_date, package_quantity, total_weight,
             invoice_file_confirmation, truck_condition_image_confirmation, truck_plate_image_confirmation,
             technical_file_confirmation, liberation, observations)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'EN ESPERA', %s)
        ''', (
            data['entry_date'], data['supplier'], data['driver_name'], data['driver_id'],
            data['food_transport_permission'], data['food_transport_validity'],
            data['fumigation_record'], last_fumigation_date, data['invoice_number'],
            data['strange_smells'], data['pests_evidence'], data['clean_truck'],
            data['uniformed_personnel'], data['floor_walls_roof_condition'], 
            data['truck_box_holes'], data['disinfection_sticker'], data['foreign_bodies'], 
            data['product'], data['lot_number'], data['shelf_life_check'], 
            data['allergen_statement'], data['graphic_system'], data['product_accepted'], 
            data['rejection_reasons'], data['received_by'], data['manufacture_date'], 
            data['expiry_date'], data['package_quantity'], data['total_weight'], data['invoice_file_confirmation'],
            data['truck_condition_image_confirmation'], data['truck_plate_image_confirmation'], data['technical_file_confirmation'],
            data['observations']
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

@additive_bp.route('/submit-files', methods=['POST']) # Subir Archivos del Formulario de Ingreso de Aditivos
def submit_files():
    # Verificar si se recibió el campo 'supplier'
    if 'supplier' not in request.form:
        return jsonify({"error": "El campo 'supplier' es obligatorio."}), 400

    # Obtener el nombre del proveedor
    supplier_name = request.form.get('supplier', 'UNKNOWN').replace(' ', '_')

    product_name = request.form.get('product', 'UNKNOWN').replace(' ', '_')

    # Obtener la fecha actual para los nombres de los archivos
    current_date = datetime.now().strftime("%d-%m-%Y")

    # Definir carpetas específicas
    transporte_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'Transporte')
    producto_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'Producto')

    # Crear las carpetas si no existen
    os.makedirs(transporte_folder, exist_ok=True)
    os.makedirs(producto_folder, exist_ok=True)

    # Función para guardar el archivo con el nuevo nombre
    def save_file(file, folder, extra):
        if file:
            original_extension = os.path.splitext(file.filename)[1]
            new_filename = f"{current_date}_{supplier_name}_{product_name}_{extra}{original_extension}"
            file_path = os.path.join(folder, new_filename)
            file.save(file_path)
            return new_filename
        return None

    uploaded_files = {}

    # Guardar los archivos y asignarles un extra en su nombre
    if 'invoice_file' in request.files:
        uploaded_files['invoice_file'] = save_file(request.files['invoice_file'], transporte_folder, 'factura_guia')

    if 'truck_condition_image' in request.files:
        uploaded_files['truck_condition_image'] = save_file(request.files['truck_condition_image'], transporte_folder, 'estado_camion')

    if 'truck_plate_image' in request.files:
        uploaded_files['truck_plate_image'] = save_file(request.files['truck_plate_image'], transporte_folder, 'placa_del_camion')

    if 'technical_file' in request.files:
        uploaded_files['technical_file'] = save_file(request.files['technical_file'], producto_folder, 'ficha_certificado')

    return jsonify({"message": "Archivos subidos exitosamente", "files": uploaded_files}), 200

#PAGINA "ARCHIVOS | ADITIVOS"

@additive_bp.route('/get-files', methods=['GET']) # Listar los archivos |ADITIVOS
def get_files():
    try:
        # Verificar si las carpetas existen
        transporte_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'Transporte')
        producto_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'Producto')

        # Comprobar si las carpetas existen
        if not os.path.exists(transporte_folder):
            raise FileNotFoundError(f"La carpeta {transporte_folder} no existe.")
        if not os.path.exists(producto_folder):
            raise FileNotFoundError(f"La carpeta {producto_folder} no existe.")
        
        # Obtener los archivos de las carpetas
        transporte_files = os.listdir(transporte_folder)
        producto_files = os.listdir(producto_folder)

        # Si las carpetas están vacías, puedes devolver un mensaje
        if not transporte_files and not producto_files:
            return jsonify({"message": "No hay archivos en las carpetas."}), 200

        # Retornar los archivos como respuesta
        return jsonify({
            'transporte_files': transporte_files,
            'producto_files': producto_files
        }), 200

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"Error inesperado: {e}")
        return jsonify({"error": "Error interno del servidor."}), 500

@additive_bp.route('/submit-just-one-file', methods=['POST']) # Subir un solo archivo | ADITIVOS
def submit_just_one_file():
    # Verificar que los campos necesarios estén presentes
    if 'supplier' not in request.form or 'fileType' not in request.form or 'date' not in request.form:
        return jsonify({"error": "Los campos 'supplier', 'fileType' y 'date' son obligatorios."}), 400

    supplier_name = request.form['supplier'].replace(' ', '_')
    product_name = request.form['product'].replace(' ', '_')
    file_type = request.form['fileType']
    # Validar y utilizar la fecha enviada
    try:
        selected_date = datetime.strptime(request.form['date'], "%d-%m-%Y").strftime("%d-%m-%Y")
    except ValueError:
        return jsonify({"error": "El formato de la fecha es inválido. Usa 'dd-mm-yyyy'."}), 400

    # Determinar la ruta de la carpeta donde se guardará el archivo
    if file_type in ['factura_guia', 'estado_camion', 'placa_camion']:
        folder_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'Transporte')
    elif file_type == 'ficha_certificado':
        folder_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'Producto')
    else:
        return jsonify({"error": "Tipo de archivo no válido."}), 400

    os.makedirs(folder_path, exist_ok=True)

    # Guardar el archivo
    file = request.files.get('file')
    if file:
        original_extension = os.path.splitext(file.filename)[1]
        new_filename = f"{selected_date}_{supplier_name}_{product_name}_{file_type}{original_extension}"
        file_path = os.path.join(folder_path, new_filename)

        print(f"Guardando archivo en: {file_path}")
        file.save(file_path)

        return jsonify({"message": "Archivo subido exitosamente", "filename": new_filename}), 200
    else:
        return jsonify({"error": "No se ha enviado ningún archivo."}), 400

@additive_bp.route('/download/<folder>/<filename>', methods=['GET']) # Descargar archivo elegido | ADITIVOS
def download_file(folder, filename):
    # Construir la ruta completa
    folder_path = f"{Config.UPLOAD_FOLDER}/{folder}"
    try:
        # Enviar el archivo desde la carpeta correspondiente
        return send_from_directory(folder_path, filename, as_attachment=True)
    except FileNotFoundError:
        # Manejo de error si el archivo no existe
        abort(404, description="Archivo no encontrado.")

@additive_bp.route('/delete-file', methods=['DELETE']) # Eliminar archivo elegido | ADITIVOS
def delete_file():
    try:
        # Obtener datos del archivo y la carpeta desde la solicitud
        data = request.get_json()
        file_name = data['file']
        folder = data['folder']

        # Determinar la ruta del archivo a eliminar
        if folder not in ['Transporte', 'Producto']:
            return jsonify({'error': 'Carpeta no válida'}), 400

        file_path = os.path.join(Config.UPLOAD_FOLDER, folder, file_name)

        # Verificar si el archivo existe
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({'message': 'Archivo eliminado correctamente'}), 200
        else:
            return jsonify({'error': 'Archivo no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# PÁGINA "REGISTRO DE ADITIVOS"

@additive_bp.route('/products', methods=['GET']) # Listar registro del ingreso de aditivos
def get_products():
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM product_entry;")
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(products)

@additive_bp.route('/products/<int:product_id>', methods=['PUT']) # Editar un registo | Ingreso de Aditivos
def update_product(product_id):
    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Generar los campos dinámicamente
    update_fields = ", ".join([f"{key} = %s" for key in data.keys()])
    values = list(data.values()) + [product_id]
    
    query = f"UPDATE product_entry SET {update_fields} WHERE id = %s;"
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Producto actualizado exitosamente."})

@additive_bp.route('/products/<int:product_id>', methods=['DELETE']) # Eliminar un registro | Ingreso de Aditivos
def delete_product(product_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM product_entry WHERE id = %s;", (product_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Producto eliminado exitosamente."})

@additive_bp.route('/download-product-table', methods=['GET']) # Descargar registro de ingreso de Aditivos
def download_product_table():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Consulta para seleccionar todas las columnas de la tabla
        cur.execute('''
            SELECT id, entry_date, supplier, driver_name, driver_id, 
                   food_transport_permission, food_transport_validity, 
                   fumigation_record, last_fumigation_date, invoice_number, 
                   strange_smells, pests_evidence, clean_truck, uniformed_personnel, 
                   floor_walls_roof_condition, truck_box_holes, disinfection_sticker, 
                   foreign_bodies, product, lot_number, 
                   package_quantity, total_weight, manufacture_date, expiry_date, 
                   shelf_life_check, allergen_statement, graphic_system, 
                   product_accepted, rejection_reasons, received_by, 
                   invoice_file_confirmation, truck_condition_image_confirmation, 
                   truck_plate_image_confirmation, technical_file_confirmation, liberation
            FROM product_entry
            ORDER BY entry_date DESC
        ''')
        data = cur.fetchall()

        # Crear un libro de trabajo de Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Productos"

        # Encabezados en español
        headers = [
            "ID", "Fecha de Ingreso", "Proveedor", "Nombre del Conductor", "ID del Conductor",
            "Permiso de Transporte de Alimentos", "Vigencia del Permiso", "Registro de Fumigación",
            "Última Fecha de Fumigación", "Número de Factura", "Olores Extraños", "Evidencia de Plagas",
            "Camión Limpio", "Personal Uniformado", "Estado del Piso, Paredes y Techo",
            "Huecos en la Caja del Camión", "Etiqueta de Desinfección", "Cuerpos Extraños",
            "Producto", "Número de Lote", "Cantidad de Paquetes", "Peso Total",
            "Fecha de Fabricación", "Fecha de Expiración", "Verificación de Vida Útil",
            "Declaración de Alérgenos", "Sistema Gráfico", "Producto Aceptado",
            "Razones de Rechazo", "Recibido Por", "Confirmación de Factura",
            "Confirmación de Imagen del Estado del Camión",
            "Confirmación de Imagen de la Placa del Camión", "Confirmación de Archivo Técnico", "Liberación"
        ]
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
            download_name="registro-aditivos.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@additive_bp.route('/provider', methods=['GET']) 
def get_provider():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT provider_name FROM providers ORDER BY id ASC")  # Ajusta el nombre de la tabla y columna según tu base de datos
        providers = [row['provider_name'] for row in cursor.fetchall()]
        return jsonify(providers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@additive_bp.route('/product', methods=['GET'])
def get_product():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT product_name FROM products WHERE product_type IN ('ADITIVO', 'MATERIA PRIMA') ORDER BY id ASC")
        products = [row['product_name'] for row in cursor.fetchall()]
        return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

#Pagina "Agregar Productos y Proveedores | ADITIVOS"

@additive_bp.route('/get-providers', methods=['GET']) # Listar proveedores | Aditivos
def get_providers_list():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT id, provider_name FROM providers")
        providers = cursor.fetchall()
        return jsonify(providers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@additive_bp.route('/get-products', methods=['GET']) # Listar productos | Aditivos
def get_products_list():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT p.id, p.product_name, p.product_type, pr.provider_name
            FROM products p
            JOIN providers pr ON p.provider_id = pr.id
        """)
        products = cursor.fetchall()
        return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@additive_bp.route('/add-provider', methods=['POST']) # Añadir proveedores | Aditivos
def add_provider():
    data = request.get_json()
    provider_name = data.get('provider_name').upper()  # Convertir a mayúsculas

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO providers (provider_name) VALUES (%s) RETURNING id", (provider_name,))
        new_provider_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({'id': new_provider_id, 'provider_name': provider_name}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@additive_bp.route('/add-product', methods=['POST']) # Añadir producto | Aditivos
def add_product():
    data = request.get_json()
    product_name = data.get('product_name').upper()  # Convertir a mayúsculas
    provider_id = data.get('provider_id')
    product_type = data.get('product_type')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (product_name, provider_id, product_type) VALUES (%s, %s, %s) RETURNING id", 
                       (product_name, provider_id, product_type))
        new_product_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({'id': new_product_id, 'product_name': product_name, 'provider_id': provider_id, 'product_type': product_type}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@additive_bp.route('/delete-provider/<int:id>', methods=['DELETE']) # Eliminar proveedor | Aditivos
def delete_provider(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM providers WHERE id = %s RETURNING id", (id,))
        deleted_provider = cursor.fetchone()

        if deleted_provider:
            conn.commit()
            return jsonify({'message': 'Proveedor eliminado exitosamente'}), 200
        else:
            return jsonify({'error': 'Proveedor no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@additive_bp.route('/delete-product/<int:id>', methods=['DELETE']) # Eliminar producto | Aditivos
def delete_products(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = %s RETURNING id", (id,))
        deleted_product = cursor.fetchone()

        if deleted_product:
            conn.commit()
            return jsonify({'message': 'Producto eliminado exitosamente'}), 200
        else:
            return jsonify({'error': 'Producto no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@additive_bp.route('/update-provider/<int:id>', methods=['PUT']) # Editar proveedor seleccionado | Aditivos
def update_provider(id):
    data = request.get_json()
    new_provider_name = data.get('provider_name')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE providers SET provider_name = %s WHERE id = %s RETURNING id, provider_name", 
                       (new_provider_name, id))
        updated_provider = cursor.fetchone()

        if updated_provider:
            conn.commit()
            return jsonify({'id': updated_provider[0], 'provider_name': updated_provider[1]}), 200
        else:
            return jsonify({'error': 'Proveedor no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@additive_bp.route('/update-product/<int:id>', methods=['PUT']) # Editar producto seleccionado | Aditivos
def update_products(id):
    data = request.get_json()
    new_product_name = data.get('product_name')
    new_provider_id = data.get('provider_id')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE products
            SET product_name = %s, provider_id = %s
            WHERE id = %s
            RETURNING id, product_name, provider_id
            """,
            (new_product_name, new_provider_id, id),
        )
        updated_product = cursor.fetchone()

        if updated_product:
            conn.commit()
            return jsonify({
                'id': updated_product[0],
                'product_name': updated_product[1],
                'provider_id': updated_product[2]
            }), 200
        else:
            return jsonify({'error': 'Producto no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

#Pagina "Liberacion de producto"

@additive_bp.route('/get-pending-products', methods=['GET']) #Listar Productos por Liberar | Aditivos
def get_pending_products():
    try:
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Consultar productos con estado "EN ESPERA"
        cur.execute('''
            SELECT id, entry_date, product, supplier
            FROM product_entry
            WHERE liberation = 'EN ESPERA'
        ''')

        # Obtener los resultados
        products = cur.fetchall()

        # Convertir los resultados en una lista de diccionarios
        product_list = [
            {
                "id": row[0],
                "entry_date": row[1].strftime('%Y-%m-%d'),  # Convertir a formato de fecha
                "product": row[2],
                "supplier": row[3]
            }
            for row in products
        ]

        # Cerrar conexión
        cur.close()
        conn.close()

        return jsonify(product_list), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@additive_bp.route('/submit-release', methods=['POST']) # Liberar el producto seleccionado | Aditivos
def submit_release():
    try:
        # Obtener los datos enviados por el cliente
        data = request.json
        product_id = data.get('product_id')
        analysis_match = data.get('analysis_match')
        release_criteria = data.get('release_criteria')
        releaser = data.get('releaser')

        if product_id is None or analysis_match is None or release_criteria is None:
            return jsonify({"error": "Faltan datos obligatorios"}), 400

        # Determinar el estado de liberación basado en las respuestas
        if (analysis_match == 'SI' and release_criteria == 'SI') or (analysis_match == 'NO APLICA' and release_criteria == 'SI'):
            release_status = 'SI'
        else:
            release_status = 'NO'

        # Conectar a la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Insertar las respuestas en la tabla de liberaciones
        cur.execute('''
            INSERT INTO additive_release (product_id, analysis_match, release_criteria, release_status, releaser)
            VALUES (%s, %s, %s, %s, %s)
        ''', (product_id, analysis_match, release_criteria, release_status, releaser))

        # Actualizar el estado de liberación en la tabla product_entry
        cur.execute('''
            UPDATE product_entry 
            SET liberation = %s 
            WHERE id = %s
        ''', (release_status, product_id))

        # Confirmar los cambios
        conn.commit()

        # Cerrar la conexión
        cur.close()
        conn.close()

        return jsonify({"message": "Liberación registrada correctamente"}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@additive_bp.route('/get-additive-releases', methods=['GET'])
def get_additive_releases():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT ar.id,
               p.product_name AS name_product,
               ar.release_date,
               ar.releaser,
               ar.release_criteria,
               ar.analysis_match,
               ar.release_status
        FROM additive_release ar
        JOIN product_entry pe ON ar.product_id = pe.id
        JOIN products p ON pe.product = p.product_name
        ORDER BY ar.release_date DESC
    """)
    rows = cur.fetchall()
    releases = [
        {
            "id": r[0],
            "product_name": r[1],
            "release_date": r[2],
            "releaser": r[3],
            "release_criteria": r[4],
            "analysis_match": r[5],
            "release_status": r[6],
        }
        for r in rows
    ]
    cur.close()
    conn.close()
    return jsonify(releases)

@additive_bp.route('/get-technical-sheets', methods=['GET'])  # Ruta adaptada para Aditivos
def get_technical_sheets():
    try:
        folder_path = os.path.join(current_app.config['UPLOAD_FOLDER_FT'], 'Fichas Tecnicas', 'Aditivos')

        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"La carpeta {folder_path} no existe.")

        files = os.listdir(folder_path)
        pdf_files = [f for f in files if f.lower().endswith('.pdf')]

        return jsonify({
            "files": pdf_files
        }), 200

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"Error inesperado: {e}")
        return jsonify({"error": "Error interno del servidor."}), 500

@additive_bp.route('/static/Fichas_Tecnicas/Aditivos/<filename>')
def serve_technical_sheet(filename):
    base_path = os.path.join(current_app.config['UPLOAD_FOLDER_FT'], 'Fichas Tecnicas', 'Aditivos')
    return send_from_directory(base_path, filename)

