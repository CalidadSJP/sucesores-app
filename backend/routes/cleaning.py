from flask import Blueprint, request, jsonify
from core.database import get_db_connection
from openpyxl import Workbook
from io import BytesIO
from flask import request, jsonify, send_file, current_app
from psycopg2.extras import RealDictCursor
from datetime import date, datetime

cleaning_bp = Blueprint("cleaning", __name__)


#PAGINA PARA CONTROL DE IMPLEMENTOS DE LIMPIEZA 

@cleaning_bp.route('/register-movement', methods=['POST'])
def register_movement():
    data = request.json
    product_id = data['product_id']
    movement_date = data['date']
    area = data['area']
    income = float(data.get('income', 0))  # Por defecto es 0 si no se proporciona
    outcome = float(data.get('outcome', 0))  # Por defecto es 0 si no se proporciona
    responsible = data['responsible']
    observations = data.get('observations', '')

    # Verificamos que no se pueda tener tanto ingreso como egreso al mismo tiempo
    if income > 0 and outcome > 0:
        return jsonify({'error': 'No se puede tener ingreso y egreso al mismo tiempo'}), 400

    # Obtenemos la cantidad actual del producto
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # 1. Obtener el stock actual del producto
        cur.execute("SELECT quantity FROM cleaning_products WHERE id = %s", (product_id,))
        result = cur.fetchone()

        if not result:
            return jsonify({'error': 'Producto no encontrado'}), 404

        current_quantity = float(result[0])

        # 2. Calculamos el saldo basado en el tipo de movimiento
        if income > 0:
            new_balance = current_quantity + income
        elif outcome > 0:
            if outcome > current_quantity:
                return jsonify({'error': 'No hay suficiente stock disponible para este egreso'}), 400
            new_balance = current_quantity - outcome
        else:
            return jsonify({'error': 'Debe haber un ingreso o egreso mayor a 0'}), 400

        # 3. Insertamos el movimiento con el nuevo saldo
        cur.execute("""
            INSERT INTO cleaning_movements (
                product_id, date, area, income, outcome, balance, responsible, observations
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (product_id, movement_date, area, income, outcome, new_balance, responsible, observations))

        # 4. Actualizamos el stock del producto
        cur.execute("""
            UPDATE cleaning_products
            SET quantity = %s
            WHERE id = %s
        """, (new_balance, product_id))

        conn.commit()
        return jsonify({'message': 'Movimiento registrado correctamente', 'new_balance': new_balance})

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cur.close()
        conn.close()

@cleaning_bp.route('/cleaning-products', methods=['GET'])
def get_cleaning_products():
    try:
        product_type = request.args.get('type')

        conn = get_db_connection()
        cur = conn.cursor()

        if product_type:
            cur.execute('SELECT id, name FROM cleaning_products WHERE type = %s AND is_active = TRUE ORDER BY name ASC', (product_type,))
        else:
            cur.execute('SELECT id, name FROM cleaning_products WHERE is_active = TRUE ORDER BY name ASC')

        products = cur.fetchall()
        cur.close()
        conn.close()

        product_list = [{"id": product[0], "name": product[1]} for product in products]
        return jsonify(product_list), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener productos", "message": str(e)}), 500

@cleaning_bp.route('/product-balance/<int:product_id>', methods=['GET'])
def get_product_balance(product_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT name, quantity FROM cleaning_products WHERE id = %s', (product_id,))
        product = cur.fetchone()
        cur.close()
        conn.close()

        if product:
            return jsonify({"id": product_id, "name": product[0], "quantity": product[1]}), 200
        else:
            return jsonify({"error": "Producto no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": "Error al obtener saldo", "message": str(e)}), 500

@cleaning_bp.route('/cleaning-products-list', methods=['GET'])
def get_cleaning_products_list():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, name, quantity, type, minimum FROM cleaning_products WHERE is_active = TRUE ORDER BY name ASC')
        products = cur.fetchall()
        cur.close()
        conn.close()

        product_list = [{"id": p[0], "name": p[1], "quantity": p[2], "type": p[3], "minimum": p[4]} for p in products]
        return jsonify(product_list), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener productos", "message": str(e)}), 500

@cleaning_bp.route('/add-cleaning-product', methods=['POST'])
def create_product():
    data = request.get_json()
    name = data.get('name')
    quantity = data.get('quantity', 0)
    type = data.get('type')
    minimum = data.get('minimum', 0)


    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO cleaning_products (name, quantity, type, minimum) VALUES (%s, %s, %s, %s)", (name, quantity, type, minimum))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Producto creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": "Error al crear producto", "message": str(e)}), 500

@cleaning_bp.route('/edit-cleaning-product/<int:product_id>', methods=['PUT'])
def update_cleaning_product(product_id):
    data = request.get_json()
    name = data.get('name')
    quantity = data.get('quantity')
    type = data.get('type')
    minimum = data.get('minimum')


    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE cleaning_products SET name = %s, quantity = %s, type = %s, minimum = %s WHERE id = %s", (name, quantity, type, minimum, product_id))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Producto actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": "Error al actualizar producto", "message": str(e)}), 500

@cleaning_bp.route('/delete-cleaning-product/<int:product_id>', methods=['PATCH'])
def delete_cleaning_product(product_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE cleaning_products SET is_active = FALSE WHERE id = %s', (product_id,))
        
        if cur.rowcount == 0:
            return jsonify({'error': 'Producto no encontrado'}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Producto desactivado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cleaning_bp.route('/download-cleaning-movements', methods=['GET'])
def download_cleaning_movements_excel():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('''
            SELECT cm.id, cp.name AS product_name, cm.date, cm.area,
                   cm.income, cm.outcome, cm.balance, cm.observations, cm.responsible
            FROM cleaning_movements cm
            JOIN cleaning_products cp ON cm.product_id = cp.id
            ORDER BY cm.date DESC
        ''')
        data = cur.fetchall()

        # Crear libro Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Movimientos Limpieza"

        # Encabezados
        headers = [
            "ID", "Producto", "Fecha", "Área", 
            "Ingreso", "Egreso", "Saldo", "Observaciones", "Responsable"
        ]
        ws.append(headers)

        # Función para formatear fechas
        def safe_str(value):
            if isinstance(value, (datetime, date)):
                return value.strftime('%d-%m-%Y')
            return value

        # Agregar filas
        for row in data:
            formatted_row = [safe_str(cell) for cell in row]
            ws.append(formatted_row)

        cur.close()
        conn.close()

        output = BytesIO()
        wb.save(output)
        wb.close()
        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name="movimientos_limpieza.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- Movimientos de limpieza (JSON) -----------------------------------------
@cleaning_bp.route('/cleaning-movements', methods=['GET'])
def get_cleaning_movements():
    """
    Devuelve la lista completa de movimientos de limpieza
    en formato JSON, ordenada por fecha descendente.
    """
    try:
        conn = get_db_connection()
        cur  = conn.cursor()

        cur.execute("""
            SELECT  cm.id,
                    cp.name                AS product_name,
                    cm.date,
                    cm.area,
                    cm.income,
                    cm.outcome,
                    cm.balance,
                    cm.observations,
                    cm.responsible
            FROM    cleaning_movements cm
            JOIN    cleaning_products  cp ON cm.product_id = cp.id
            ORDER BY cm.date DESC;
        """)

        rows = cur.fetchall()
        cur.close()
        conn.close()

        # Convertimos a una lista de diccionarios y formateamos la fecha
        movimientos = [
            {
                "id"          : r[0],
                "product_name": r[1],
                "date"        : r[2].strftime('%Y-%m-%d') if r[2] else None,
                "area"        : r[3],
                "income"      : r[4],
                "outcome"     : r[5],
                "balance"     : r[6],
                "observations": r[7],
                "responsible" : r[8]
            }
            for r in rows
        ]

        return jsonify(movimientos), 200

    except Exception as e:
        # Devuelve el mensaje de error al frontend si algo falla
        return jsonify({"error": str(e)}), 500

