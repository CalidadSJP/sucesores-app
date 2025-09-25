from flask import Blueprint, request, jsonify
from core.database import get_db_connection
from openpyxl import Workbook
from io import BytesIO
from flask import request, jsonify, send_file, current_app
from psycopg2.extras import RealDictCursor
from datetime import datetime, date
import numpy as np

weight_bp = Blueprint("weight", __name__)


#PÁGINA CONTROL DE PESOS

@weight_bp.route('/get-product-info', methods=['GET']) # Obtener datos del producto producto | Control del pesos
def get_product_info():
    # Obtener el EAN13 desde los parámetros de la solicitud
    ean13 = request.args.get('ean13')

    if not ean13:
        return jsonify({"error": "EAN13 es requerido"}), 400

    try:
        # Conectar a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Consulta para obtener la información del producto, uniendo la tabla 'article' con la tabla 'brand'
        query = """
        SELECT 
            a.ean13, 
            a.weight AS peso_neto, 
            a.format AS formato, 
            a.brand_id, 
            b.brand_name AS marca
        FROM articles a
        JOIN brand b ON a.brand_id = b.id
        WHERE a.ean13 = %s
        """
        cursor.execute(query, (ean13,))
        product = cursor.fetchone()

        # Cerrar la conexión
        cursor.close()
        conn.close()

        # Verificar si el producto existe
        if product:
            return jsonify(product), 200
        else:
            return jsonify({"error": "Producto no encontrado"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@weight_bp.route('/get-balers', methods=['GET']) # Obtener los nombres de las empacadoras | Control de pesos
def get_balers():
    try:
        # Conectar a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Consulta para obtener todas las empacadoras
        query = "SELECT id, baler_name FROM balers"
        cursor.execute(query)
        balers = cursor.fetchall()

        # Cerrar conexión
        cursor.close()
        conn.close()

        return jsonify(balers), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@weight_bp.route('/save-weight-control', methods=['POST']) # Subir el nuevo registro de control de pesos
def save_weight_control():
    try:
        data = request.json

        # Extraer datos principales
        date = data.get('date', datetime.today().strftime('%Y-%m-%d'))
        baler = data.get('baler')
        net_weight = float(data.get('net_weight'))  # Peso nominal (Qnom)
        format_ = data.get('format')
        brand = data.get('brand')
        lot = data.get('lot')
        ean13 = data.get('ean13')
        manufacture_date = data.get('manufacture_date')
        expiry_date = data.get('expiry_date')

        # Extraer los pesos y asegurarse de que sean numéricos
        pesos = [float(p) for p in data.get('weights', []) if p not in [None, ""]]

        # Cálculo de tolerancia basado en la fórmula proporcionada
        if net_weight == 100:
            error_T1 = net_weight * 0.045  # 4.5% de net_weight
        elif net_weight >= 200 and net_weight < 300:
            error_T1 = 9
        elif net_weight >= 300 and net_weight < 500:
            error_T1 = net_weight * 0.03  # 3% de net_weight
        elif net_weight >= 500 and net_weight < 1000:
            error_T1 = 15
        elif net_weight >= 1000 and net_weight < 10000:
            error_T1 = net_weight * 0.015  # 1.5% de net_weight
        elif net_weight >= 10000 and net_weight < 15000:
            error_T1 = 150
        elif net_weight >= 15000 and net_weight < 50000:
            error_T1 = net_weight * 0.01  # 1% de net_weight
        else:
            error_T1 = "ERROR TOLERANCIA"  # Error en tolerancia si no cae en los rangos

        if error_T1 == "ERROR TOLERANCIA":
            return jsonify({"error": "Error en los rangos de tolerancia para el peso nominal"}), 400

        # Cálculo de ERROR T2
        error_T2 = error_T1 * 2

        # Cálculo de límites máximos operativos
        limite_maximo_operativo = round(net_weight + (net_weight * 0.02), 2)
        limite_minimo_operativo = round(net_weight - (net_weight * 0.03), 2)

        # Calcular estadísticas de peso
        if pesos:
            average = float(np.mean(pesos))  # Convertir np.float64 a float
            minimum = float(np.min(pesos))
            maximum = float(np.max(pesos))
            std_dev = float(np.std(pesos, ddof=1)) if len(pesos) > 1 else 0.0
        else:
            average, minimum, maximum, std_dev = None, None, None, None

        # Calcular errores T1 y T2
        rango_T1_min = net_weight - 2 * error_T1  # Límite inferior de T1
        rango_T1_max = net_weight - error_T1      # Límite superior de T1
        rango_T2 = net_weight - 2 * error_T1      # Límite inferior de T2

        # Contar unidades con error T1 y T2
        count_T1 = sum(rango_T1_min <= p < rango_T1_max for p in pesos)
        count_T2 = sum(p < rango_T2 for p in pesos)

        # Porcentaje de unidades con error T1
        percent_T1 = (count_T1 / len(pesos)) * 100 if pesos else 0

        # Determinar el resultado de aceptación del lote
        result = "Aceptado"
        if average < net_weight:
            result = "Rechazado - Promedio insuficiente"
        elif percent_T1 > 2.5:
            result = "Rechazado - Demasiados errores T1"
        elif count_T2 > 0:
            result = "Rechazado - Error T2 presente"

        # Conectar a la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Insertar los datos en la base de datos
        query = """
            INSERT INTO weight_control (
                date, baler, net_weight, format, brand, lot, 
                manufacture_date, expiry_date, average, minimum, maximum, standard_deviation,
                p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, 
                p16, p17, p18, p19, p20, p21, p22, p23, p24, p25, p26, p27, p28, p29, p30,
                count_T1, count_T2, percent_T1, result, limite_maximo_operativo, limite_minimo_operativo, ean13
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                      %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = [
            date, baler, net_weight, format_, brand, lot, manufacture_date, expiry_date,
            average, minimum, maximum, std_dev
        ] + pesos + [None] * (30 - len(pesos)) + [count_T1, count_T2, percent_T1, result, limite_maximo_operativo, limite_minimo_operativo, ean13]

        cur.execute(query, values)
        conn.commit()

        # Cerrar la conexión
        cur.close()
        conn.close()

        return jsonify({
            "message": "Registro guardado exitosamente",
            "average": average,
            "min": minimum,
            "max": maximum,
            "std_dev": std_dev,
            "count_T1": count_T1,
            "count_T2": count_T2,
            "percent_T1": percent_T1,
            "result": result,
            "limite_maximo_operativo": limite_maximo_operativo,
            "limite_minimo_operativo": limite_minimo_operativo,
            "ean13": ean13
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@weight_bp.route('/get-last-weight-summary', methods=['GET']) #Obtener la información de la ultimo ingreso de pesos
def get_last_weight_summary():

    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
            SELECT date, baler, net_weight, format, brand, lot, 
                   manufacture_date, expiry_date, average, minimum, maximum, standard_deviation,  
                   count_t1, count_t2, 
                   limite_maximo_operativo, limite_minimo_operativo, result, ean13
            FROM weight_control 
            ORDER BY id DESC 
            LIMIT 1
        """)
        last_record = cur.fetchone()

        cur.close()
        conn.close()

        if last_record:
            return jsonify(last_record), 200
        else:
            return jsonify({"message": "No hay registros"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@weight_bp.route('/get-weight-history', methods=['GET']) # Obtener los datos para el grafico de dispersion | Control de pesos
def get_weight_history():

    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Obtener el último registro
        cur.execute("""
            SELECT net_weight, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10,
                   p11, p12, p13, p14, p15, p16, p17, p18, p19, p20,
                   p21, p22, p23, p24, p25, p26, p27, p28, p29, p30,
                   limite_maximo_operativo, limite_minimo_operativo, average
            FROM weight_control
            ORDER BY id DESC
            LIMIT 1
        """)
        record = cur.fetchone()

        cur.close()
        conn.close()

        if record:
            # Extraer los pesos en una lista
            weights = [{"x": i+1, "y": record[f"p{i+1}"]} for i in range(30)]

            return jsonify({
                "net_weight": record["net_weight"],
                "weights": weights,
                "limite_maximo_operativo": record["limite_maximo_operativo"],
                "limite_minimo_operativo": record["limite_minimo_operativo"],
                "average": record["average"]
            }), 200
        else:
            return jsonify({"message": "No hay registros"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@weight_bp.route('/get-last-weights', methods=['GET']) # Obtener los ultimos pesos ingresados
def get_last_weights():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Obtener el último registro de pesos
        cur.execute("""
            SELECT p1, p2, p3, p4, p5, p6, p7, p8, p9, p10,
                   p11, p12, p13, p14, p15, p16, p17, p18, p19, p20,
                   p21, p22, p23, p24, p25, p26, p27, p28, p29, p30
            FROM weight_control
            ORDER BY id DESC
            LIMIT 1
        """)
        record = cur.fetchone()

        cur.close()
        conn.close()

        if record:
            # Convertir los pesos en una lista simple
            weights = [record[f"p{i+1}"] for i in range(30)]

            return jsonify({"weights": weights}), 200
        else:
            return jsonify({"message": "No hay registros"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@weight_bp.route('/weight-control', methods=['GET'])
def get_weight_control_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT id, date, baler, net_weight, format, brand, lot, manufacture_date, expiry_date, 
               average, minimum, maximum, standard_deviation, 
               p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, 
               p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, 
               p21, p22, p23, p24, p25, p26, p27, p28, p29, p30, 
               result, count_t1, count_t2, percent_t1, 
               limite_maximo_operativo, limite_minimo_operativo, ean13
        FROM weight_control
        ORDER BY date DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        # Obtener nombres de columnas
        column_names = [desc[0] for desc in cursor.description]

        # Convertir los datos a lista de diccionarios
        data = [dict(zip(column_names, row)) for row in rows]

        # Formatear las fechas a 'DD-MM-YYYY'
        for row in data:
            if row.get('date'):
                row['date'] = row['date'].strftime('%d-%m-%Y')  # Formato de la fecha
            if row.get('manufacture_date'):
                row['manufacture_date'] = row['manufacture_date'].strftime('%d-%m-%Y')
            if row.get('expiry_date'):
                row['expiry_date'] = row['expiry_date'].strftime('%d-%m-%Y')

        cursor.close()
        conn.close()

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@weight_bp.route('/weight-control/<int:id>', methods=['PUT'])  # Editar registro de control de peso
def update_weight_control(id):
    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()

    # Generar los campos dinámicamente para la actualización
    update_fields = ", ".join([f"{key} = %s" for key in data.keys()])
    values = list(data.values()) + [id]

    # Consulta de actualización
    query = f"UPDATE weight_control SET {update_fields} WHERE id = %s;"
    
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Registro de peso actualizado exitosamente."})

@weight_bp.route('/weight-control/<int:id>', methods=['DELETE'])  # Eliminar registro de control de peso
def delete_weight_control(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Ejecutar eliminación
    cursor.execute("DELETE FROM weight_control WHERE id = %s;", (id,))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"message": "Registro de peso eliminado exitosamente."})

@weight_bp.route('/download-weight-control', methods=['GET'])  # Descargar registro | Control de peso
def download_weight_control_excel():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('''
            SELECT id, date, baler, net_weight, format, brand, lot, manufacture_date, expiry_date, 
                   average, minimum, maximum, standard_deviation, 
                   p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, 
                   p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, 
                   p21, p22, p23, p24, p25, p26, p27, p28, p29, p30, 
                   result, count_t1, count_t2, percent_t1, 
                   limite_maximo_operativo, limite_minimo_operativo, ean13
            FROM weight_control
            ORDER BY date DESC
        ''')
        data = cur.fetchall()

        # Crear el archivo Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Control de Peso"

        # Encabezados
        headers = [
            "ID", "Fecha", "Empacador", "Peso Neto", "Formato", "Marca", "Lote",
            "Fecha de Fabricación", "Fecha de Vencimiento",
            "Promedio", "Mínimo", "Máximo", "Desviación Estándar",
        ]
        headers += [f"P{i}" for i in range(1, 31)]
        headers += [
            "Resultado", "Cantidad T1", "Cantidad T2", "Porcentaje T1",
            "Límite Máx. Operativo", "Límite Mín. Operativo", "EAN13"
        ]
        ws.append(headers)

        # Función para convertir fechas a string
        def safe_str(value):
            if isinstance(value, (datetime, date)):
                return value.strftime('%d-%m-%Y')
            return value

        # Agregar filas de datos
        for row in data:
            formatted_row = [safe_str(value) for value in row]
            ws.append(formatted_row)

        cur.close()
        conn.close()

        # Guardar en BytesIO
        output = BytesIO()
        wb.save(output)
        wb.close()
        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name="registro_pesos.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#PAGINA PARA LISTAR ARTICULOS

# Obtener todos los artículos
@weight_bp.route('/articles', methods=['GET'])
def get_articles():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM articles ORDER BY id;")
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    data = [dict(zip(colnames, row)) for row in rows]
    cur.close()
    conn.close()
    return jsonify(data)

# Insertar nuevo artículo
@weight_bp.route('/articles', methods=['POST'])
def add_article():
    data = request.json
    query = """
        INSERT INTO articles (cod_article, article_name, format, brand_id, ean13, ean14, weight)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data['cod_article'], data['article_name'], data['format'],
        data['brand_id'], data['ean13'], data['ean14'], data['weight']
    )
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Artículo añadido correctamente'})

# Actualizar artículo
@weight_bp.route('/articles/<int:id>', methods=['PUT'])
def update_article(id):
    data = request.json
    query = """
        UPDATE articles SET cod_article=%s, article_name=%s, format=%s,
        brand_id=%s, ean13=%s, ean14=%s, weight=%s WHERE id=%s
    """
    values = (
        data['cod_article'], data['article_name'], data['format'],
        data['brand_id'], data['ean13'], data['ean14'], data['weight'], id
    )
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Artículo actualizado correctamente'})

# Eliminar artículo
@weight_bp.route('/articles/<int:id>', methods=['DELETE'])
def delete_article(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM articles WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Artículo eliminado correctamente'})

@weight_bp.route('/brands', methods=['GET'])
def get_brands():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, brand_name FROM brand ORDER BY brand_name ASC")
    rows = cur.fetchall()
    brands = [{'id': row[0], 'name': row[1]} for row in rows]
    cur.close()
    return jsonify(brands)

