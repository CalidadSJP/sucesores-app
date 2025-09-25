from flask import Blueprint, request, jsonify
from core.database import get_db_connection
from openpyxl import Workbook
from io import BytesIO
from flask import request, jsonify, send_file, send_from_directory, abort, current_app
from psycopg2.extras import RealDictCursor
from config import Config
import os
from datetime import datetime

packaging_bp = Blueprint("packaging", __name__)


#Pagina "Añadir Proveedores o Material de Empaque"

@packaging_bp.route('/add-brand', methods=['POST']) # Añadir proveedores | Aditivos
def add_brand():
    data = request.get_json()
    brand_name = data.get('brand_name').upper()  # Convertir a mayúsculas

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO brand (brand_name) VALUES (%s) RETURNING id", (brand_name,))
        new_brand_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({'id': new_brand_id, 'provider_name': brand_name}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@packaging_bp.route('/get-providers-material', methods=['GET']) # Listar proveedores | Material de empaque
def get_providers_material_list():

    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT id, provider_name FROM providers_material ORDER BY provider_name ASC")
        providers = cursor.fetchall()
        return jsonify(providers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@packaging_bp.route('/get-brand-material', methods=['GET']) # Obtener los nombres de las marcas | Material de Empaque
def get_brand_material():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT id, brand_name FROM brand ORDER BY brand_name ASC")
        providers = cursor.fetchall()
        return jsonify(providers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@packaging_bp.route('/get-materials', methods=['GET']) # Listar Material de Empaque
def get_products_material_list():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT m.id, m.code, m.code_sap, m.material_name, m.material_type, prm.provider_name, b.brand_name
            FROM materials m
            JOIN providers_material prm ON m.provider_id = prm.id
            JOIN brand b ON m.brand_id = b.id; 

        """)
        materials = cursor.fetchall()
        return jsonify(materials)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@packaging_bp.route('/add-provider-material', methods=['POST']) # Añadir proveedor | Material de Empaque 
def add_provider_material():
    data = request.get_json()
    provider_name = data.get('provider_name').upper()  # Convertir a mayúsculas

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO providers_material (provider_name) VALUES (%s) RETURNING id", (provider_name,))
        new_provider_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({'id': new_provider_id, 'provider_name': provider_name}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@packaging_bp.route('/add-material', methods=['POST']) # Añadir nuevo material de empaque
def add_material():
    data = request.get_json()
    material_name = data.get('material_name').upper()  # Convertir a mayúsculas
    provider_id = data.get('provider_id')
    code = data.get('code')
    code_sap = data.get('code_sap')
    material_type = data.get('material_type').upper()
    brand_id = data.get('brand_id')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO materials (code, code_sap, material_name, provider_id, material_type, brand_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id", 
                       (code, code_sap, material_name, provider_id, material_type, brand_id))
        new_material_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({'message': 'Material guardado exitosamente','id': new_material_id,'code': code, 'code_sap': code_sap, 'product_name': material_name, 'provider_id': provider_id, 'material_type': material_type, 'brand_id': brand_id}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@packaging_bp.route('/delete-provider-material/<int:id>', methods=['DELETE']) # Eliminar proveedor | Material de empaque
def delete_provider_material(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM providers_material WHERE id = %s RETURNING id", (id,))
        deleted_provider_material = cursor.fetchone()

        if deleted_provider_material:
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

@packaging_bp.route('/delete-material/<int:id>', methods=['DELETE']) # Eliminar material seleccionado
def delete_material(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM materials WHERE id = %s RETURNING id", (id,))
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

@packaging_bp.route('/update-provider-material/<int:id>', methods=['PUT']) # Editar proveedor | Material de empaque
def update_provider_material(id):
    data = request.get_json()
    new_provider_name = data.get('provider_name')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE providers_material SET provider_name = %s WHERE id = %s RETURNING id, provider_name", 
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

@packaging_bp.route('/update-material/<int:id>', methods=['PUT']) # Editar material de empaque seleccionado
def update_materials(id):
    data = request.get_json()
    new_material_name = data.get('material_name')
    new_provider_id = data.get('provider_id')
    new_code = data.get('code')
    new_code_sap = data.get('code_sap')
    new_material_type = data.get('material_type')
    new_brand_id = data.get('brand_id')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE materials
            SET code = %s, code_sap = %s, material_name = %s, provider_id = %s, material_type = %s, brand_id = %s
            WHERE id = %s
            RETURNING id, code, code_sap, material_name, provider_id, material_type, brand_id
            """,
            (new_code, new_code_sap, new_material_name, new_provider_id, new_material_type, new_brand_id, id),
        )
        updated_material = cursor.fetchone()

        if updated_material:
            conn.commit()
            return jsonify({
                'id': updated_material[0],
                'code': updated_material[1],
                'code_sap': updated_material[2],
                'material_name': updated_material[3],
                'provider_id': updated_material[4],
                'material_type': updated_material[5],
                'brand_id': updated_material[6]               
            }), 200
        else:
            return jsonify({'error': 'Producto no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

#Página "Formulario de ingreso Material de Empaque"

@packaging_bp.route('/submit-material-form', methods=['POST']) # Subir formulario material de empaque
def submit_material_form():
    try:
        # Obtiene los datos JSON
        data = request.json
        # Establecer conexión con la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Insertar los datos en la tabla correspondiente
        cur.execute('''
            INSERT INTO material_entry
            (entry_date, supplier, driver_name, driver_id, invoice_number,
             strange_smells, pests_evidence, clean_truck, uniformed_personnel, 
             floor_walls_roof_condition, truck_box_holes,
             foreign_bodies, brand, product, lot_number, shelf_life_check, 
             allergen_statement, product_accepted, rejection_reasons, 
             received_by, manufacture_date, package_quantity, unit_quantity, total_weight,
             invoice_file_confirmation, truck_condition_image_confirmation, truck_plate_image_confirmation,
             technical_file_confirmation)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )
        ''', (
            data['entry_date'], data['supplier'], data['driver_name'], data['driver_id'],
            data['invoice_number'],
            data['strange_smells'], data['pests_evidence'], data['clean_truck'],
            data['uniformed_personnel'], data['floor_walls_roof_condition'], 
            data['truck_box_holes'], data['foreign_bodies'], data['brand'],
            data['product'], data['lot_number'], data['shelf_life_check'], 
            data['allergen_statement'], data['product_accepted'], 
            data['rejection_reasons'], data['received_by'], data['manufacture_date'], 
            data['package_quantity'], data['unit_quantity'], data['total_weight'], data['invoice_file_confirmation'],
            data['truck_condition_image_confirmation'], data['truck_plate_image_confirmation'], data['technical_file_confirmation']
            
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

@packaging_bp.route('/submit-materials-files', methods=['POST']) # Subir archivos | Material de empaque
def submit_material_files():
    # Verificar si se recibió el campo 'supplier'
    if 'supplier' not in request.form:
        return jsonify({"error": "El campo 'supplier' es obligatorio."}), 400

    # Obtener el nombre del proveedor
    supplier_name = request.form.get('supplier', 'UNKNOWN').replace(' ', '_')

    # Obtener el nombre del producto
    product_name = request.form.get('product', 'UNKNOWN').replace(' ', '_')

    # Obtener el nombre de la marca (agregar este paso)
    brand_name = request.form.get('brand', 'UNKNOWN').replace(' ', '_')  # Asegúrate de que este campo esté presente en el formulario

    provided_date = request.form.get('entry_date', None)
    if provided_date:
        # Validar el formato de la fecha (YYYY-MM-DD)
        try:
            formatted_date = datetime.strptime(provided_date, "%Y-%m-%d").strftime("%d-%m-%Y")
        except ValueError:
            return jsonify({"error": "El formato de la fecha es inválido. Use 'YYYY-MM-DD'."}), 400
    else:
        formatted_date = datetime.now().strftime("%d-%m-%Y")
    

    # Definir carpetas específicas
    transporte_folder = os.path.join(current_app.config['UPLOAD_MATERIAL_FOLDER'], 'Transporte')
    producto_folder = os.path.join(current_app.config['UPLOAD_MATERIAL_FOLDER'], 'Producto')

    # Crear las carpetas si no existen
    os.makedirs(transporte_folder, exist_ok=True)
    os.makedirs(producto_folder, exist_ok=True)

    # Función para guardar el archivo con el nuevo nombre
    def save_file(file, folder, extra):
        if file:
            original_extension = os.path.splitext(file.filename)[1]
            new_filename = f"{formatted_date}_{supplier_name}_{brand_name}_{product_name}_{extra}{original_extension}"  # Incluir la marca aquí
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

@packaging_bp.route('/providers-material', methods=['GET']) # Listar proveedores | Material de empaque
def get_providers_material():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT provider_name FROM providers_material ORDER BY provider_name ASC")  # Ajusta el nombre de la tabla y columna según tu base de datos
        providers = [row['provider_name'] for row in cursor.fetchall()]
        return jsonify(providers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@packaging_bp.route('/brand', methods=['GET']) # Listar marcas | Material de empaque
def get_brand():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT brand_name FROM brand ORDER BY brand_name ASC")
        brands = [row['brand_name'] for row in cursor.fetchall()]
        return jsonify(brands)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@packaging_bp.route('/get-code', methods=['GET']) # Listar codigos de cada material
def get_code():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT code FROM materials")
        codes = [row['code'] for row in cursor.fetchall()]
        return jsonify(codes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@packaging_bp.route('/get-product-type/<code>', methods=['GET']) # Mostrar el tipo de material de empaque elegido
def get_product_type_by_code(code):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT material_type FROM materials WHERE code = %s", (code,))
        result = cursor.fetchone()
        if result:
            return jsonify(result)  # Devuelve {"material_name": "Nombre del producto"}
        else:
            return jsonify({'error': 'Código no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@packaging_bp.route('/get-product-name/<code>', methods=['GET']) # Mostrar el nombre del material de empaque elegido
def get_product_name_by_code(code):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT material_name FROM materials WHERE code = %s", (code,))
        result = cursor.fetchone()
        if result:
            return jsonify(result)  # Devuelve {"material_name": "Nombre del producto"}
        else:
            return jsonify({'error': 'Código no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@packaging_bp.route('/get-products-by-brand/<brand>', methods=['GET']) 
def get_products_by_brand(brand):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT m.code
            FROM materials m
            JOIN brand b ON m.brand_id = b.id
            WHERE b.brand_name = %s
        """, (brand,))
        products = cursor.fetchall()
        return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@packaging_bp.route('/get-products-by-brand-provider/<brand>/<provider>', methods=['GET']) # Listar materiales de acuerdo a la marca y proveedor elegidos
def get_products_by_brand_provider(brand, provider):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = """
            SELECT p.code
            FROM materials p
            INNER JOIN brand b ON p.brand_id = b.id
            INNER JOIN providers_material pr ON p.provider_id = pr.id
            WHERE b.brand_name = %s AND pr.provider_name = %s
        """
        params = [brand, provider]

        query += " ORDER BY p.code ASC"

        cursor.execute(query, params)
        products = cursor.fetchall()

        print("Productos devueltos:", products)

        return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()


#"Pagina de archivos Material de empaque"

@packaging_bp.route('/get-material-files', methods=['GET']) # Listar archivos | Material de empaque
def get_material_files():
    try:
        # Verificar si las carpetas existen
        transporte_folder = os.path.join(current_app.config['UPLOAD_MATERIAL_FOLDER'], 'Transporte')
        producto_folder = os.path.join(current_app.config['UPLOAD_MATERIAL_FOLDER'], 'Producto')

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

@packaging_bp.route('/submit-just-one-file-material', methods=['POST']) # Subir un archivo | Material de empaque
def submit_just_one_file_material():
    # Verificar que los campos necesarios estén presentes
    if 'supplier' not in request.form or 'fileType' not in request.form or 'date' not in request.form or 'brand' not in request.form:
        return jsonify({"error": "Los campos 'supplier', 'fileType' y 'date' son obligatorios."}), 400

    supplier_name = request.form['supplier'].replace(' ', '_')
    product_name = request.form['product'].replace(' ', '_')
    brand_name = request.form['brand'].replace(' ', '_')
    file_type = request.form['fileType']
    # Validar y utilizar la fecha enviada
    try:
        selected_date = datetime.strptime(request.form['date'], "%d-%m-%Y").strftime("%d-%m-%Y")
    except ValueError:
        return jsonify({"error": "El formato de la fecha es inválido. Usa 'dd-mm-yyyy'."}), 400

    # Determinar la ruta de la carpeta donde se guardará el archivo
    if file_type in ['estado_camion', 'placa_camion', 'factura_guia']:
        folder_path = os.path.join(current_app.config['UPLOAD_MATERIAL_FOLDER'], 'Transporte')
    elif file_type in ['ficha_certificado']:
        folder_path = os.path.join(current_app.config['UPLOAD_MATERIAL_FOLDER'], 'Producto')
    else:
        return jsonify({"error": "Tipo de archivo no válido."}), 400

    os.makedirs(folder_path, exist_ok=True)

    # Guardar el archivo
    file = request.files.get('file')
    if file:
        original_extension = os.path.splitext(file.filename)[1]
        new_filename = f"{selected_date}_{supplier_name}_{brand_name}_{product_name}_{file_type}{original_extension}"
        file_path = os.path.join(folder_path, new_filename)

        print(f"Guardando archivo en: {file_path}")
        file.save(file_path)

        return jsonify({"message": "Archivo subido exitosamente", "filename": new_filename}), 200
    else:
        return jsonify({"error": "No se ha enviado ningún archivo."}), 400

@packaging_bp.route('/download-material-file/<folder>/<filename>', methods=['GET']) # Descargar archivo seleccionado | Material de empque
def download_material_file(folder, filename):
    # Construir la ruta completa
    folder_path = f"{Config.UPLOAD_MATERIAL_FOLDER}/{folder}"
    try:
        # Enviar el archivo desde la carpeta correspondiente
        return send_from_directory(folder_path, filename, as_attachment=True)
    except FileNotFoundError:
        # Manejo de error si el archivo no existe
        abort(404, description="Archivo no encontrado.")

@packaging_bp.route('/delete-material-file', methods=['DELETE']) # Eliminar archivo seleccionado | Material de empqeu
def delete_material_file():
    try:
        # Obtener datos del archivo y la carpeta desde la solicitud
        data = request.get_json()
        file_name = data['file']
        folder = data['folder']

        # Determinar la ruta del archivo a eliminar
        if folder not in ['Transporte', 'Producto']:
            return jsonify({'error': 'Carpeta no válida'}), 400

        file_path = os.path.join(Config.UPLOAD_MATERIAL_FOLDER, folder, file_name)

        # Verificar si el archivo existe
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({'message': 'Archivo eliminado correctamente'}), 200
        else:
            return jsonify({'error': 'Archivo no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@packaging_bp.route('/provider-material', methods=['GET']) # Listar proveedores | Material de Empaque
def get_provider_material():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT provider_name FROM providers_material ORDER BY id ASC")  # Ajusta el nombre de la tabla y columna según tu base de datos
        providers = [row['provider_name'] for row in cursor.fetchall()]
        return jsonify(providers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

@packaging_bp.route('/material', methods=['GET']) 
def get_material():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT material_name FROM packaging_material ORDER BY material_name ASC")
        products = [row['material_name'] for row in cursor.fetchall()]
        return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

#PAGINA "REGISTRO DE MATERIAL DE EMPAQUE"

@packaging_bp.route('/materials', methods=['GET']) # Listar registro de ingreso de material de empaque
def get_material_list():
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM material_entry;")
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(products)

@packaging_bp.route('/materials/<int:material_id>', methods=['PUT']) # Editar registro | Ingreso de material de empaque
def update_material_list(material_id):
    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Generar los campos dinámicamente
    update_fields = ", ".join([f"{key} = %s" for key in data.keys()])
    values = list(data.values()) + [material_id]
    
    query = f"UPDATE material_entry SET {update_fields} WHERE id = %s;"
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Producto actualizado exitosamente."})

@packaging_bp.route('/materials/<int:material_id>', methods=['DELETE']) # Eliminar registro | Ingreso de material de empaque
def delete_material_list(material_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM material_entry WHERE id = %s;", (material_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Producto eliminado exitosamente."})

@packaging_bp.route('/download-material-table', methods=['GET']) # Descargar registro | Ingreso de material de empaque
def download_material_table():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Consulta para seleccionar todas las columnas de la tabla
        cur.execute('''
            SELECT id, entry_date, supplier, driver_name, driver_id, invoice_number,
             strange_smells, pests_evidence, clean_truck, uniformed_personnel, 
             floor_walls_roof_condition, truck_box_holes,
             foreign_bodies, brand, product, lot_number, shelf_life_check, 
             allergen_statement, product_accepted, rejection_reasons, 
             received_by, manufacture_date, package_quantity, unit_quantity, total_weight,
             invoice_file_confirmation, truck_condition_image_confirmation, truck_plate_image_confirmation,
             technical_file_confirmation
            FROM material_entry
            ORDER BY entry_date DESC
        ''')
        data = cur.fetchall()

        # Crear un libro de trabajo de Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Material de Empaque"

        # Encabezados en español
        headers = [
            "ID", "Fecha de Ingreso", "Proveedor", "Nombre del Conductor", "ID del Conductor",
            "Número de Factura", "Olores Extraños", "Evidencia de Plagas",
            "Camión Limpio", "Personal Uniformado", "Estado del Piso, Paredes y Techo",
            "Huecos en la Caja del Camión", "Cuerpos Extraños", "Marca",
            "Producto", "Número de Lote", "Cantidad de Paquetes", "Cantidad de unidades", "Peso Total",
            "Fecha de Fabricación", "Verificación de Vida Útil",
            "Declaración de Alérgenos", "Producto Aceptado",
            "Razones de Rechazo", "Recibido Por", "Confirmación de Factura",
            "Confirmación de Imagen del Estado del Camión",
            "Confirmación de Imagen de la Placa del Camión", "Confirmación de Archivo Técnico"
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
            download_name="registro-material-de-empaque.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
