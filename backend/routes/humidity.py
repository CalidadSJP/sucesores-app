from flask import Blueprint, request, jsonify
from core.database import get_db_connection
from openpyxl import Workbook
from io import BytesIO
from flask import request, jsonify, send_file, current_app
from psycopg2.extras import RealDictCursor
from datetime import date, time


humidity_bp = Blueprint("humidity", __name__)


#CONTROL DE HUMEDADES

@humidity_bp.route('/submit-humidity-control', methods=['POST'])
def add_humidity():
    try:
        data = request.get_json()

        # Reemplazar campos vacíos con "0" o " " según corresponda
        cleaned_data = {
            'date': data.get('date') or '0',
            'time': data.get('time') or '0',
            'line': data.get('line') or '0',
            'format': data.get('format') or '0',
            'zone': data.get('zone') or '0',
            'humidity': data.get('humidity') or '0',
            'responsible': data.get('responsible') if data.get('responsible') not in [None, ''] else '',
            'observations': data.get('observations') if data.get('observations') not in [None, ''] else '',
            'balance': data.get('balance') if data.get('balance') not in [None, ''] else '0'
        }

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO humidity_control (
                date, time, line, format, zone,
                humidity, responsible, observations, balance
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            cleaned_data['date'],
            cleaned_data['time'],
            cleaned_data['line'],
            cleaned_data['format'],
            cleaned_data['zone'],
            cleaned_data['humidity'],
            cleaned_data['responsible'],
            cleaned_data['observations'],
            cleaned_data['balance']
        ))

        conn.commit()
        return jsonify({'message': 'Registro guardado correctamente'}), 201

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        return jsonify({'error': 'Error al guardar el registro', 'details': str(e)}), 500

    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

@humidity_bp.route('/humidity-control/<int:id>', methods=['PUT'])
def update_humidity_record(id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE humidity_control
        SET balance=%s, date=%s, time=%s, line=%s, format=%s, zone=%s,
            humidity=%s, responsible=%s, observations=%s
        WHERE id=%s
    """, (
        data['balance'], data['date'], data['time'], data['line'], data['format'],
        data['zone'], data['humidity'], data['responsible'], data['observations'], id
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Registro actualizado'})

@humidity_bp.route('/humidity-records', methods=['GET']) # Obtener el registro de control de humeades para la tabla
def get_humidity_records():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM humidity_control ORDER BY id DESC")
        rows = cur.fetchall()
        records = []

        for row in rows:
            record = {}
            for i, value in enumerate(row):
                column_name = cur.description[i][0]
                # Convert date and time to string
                if isinstance(value, (date, time)):
                    record[column_name] = value.isoformat()
                else:
                    record[column_name] = value
            records.append(record)

        return jsonify(records)
    except Exception as e:
        print(f"❌ Error en get_humidity_records: {e}")
        return jsonify({"error": str(e)}), 500

@humidity_bp.route('/get-lines', methods=['GET']) # Obtener los nombres de las lineas de producción | Control de Humedades
def get_lines():
    try:
        # Conectar a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Consulta para obtener todas las empacadoras
        query = "SELECT id, line_name FROM production_line"
        cursor.execute(query)
        lines = cursor.fetchall()

        # Cerrar conexión
        cursor.close()
        conn.close()

        return jsonify(lines), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@humidity_bp.route('/get-formats/<int:line_id>', methods=['GET'])# Obtener los formatos del producto por cada linea de produccións
def get_formats_by_line(line_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, format_name FROM pasta_format WHERE line_id = %s", (line_id,))
    formats = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": f[0], "format_name": f[1]} for f in formats])

@humidity_bp.route('/download-humidity', methods=['GET'])  # Endpoint para descarga de registro de humedades
def download_humidity():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Consulta de los datos de la tabla humidity_control
        cur.execute('''
            SELECT date, time, line, format, zone, humidity, responsible, observations
            FROM humidity_control
            ORDER BY date DESC, time DESC
        ''')
        data = cur.fetchall()

        # Crear el archivo Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Control de Humedades"

        # Encabezados
        headers = [
            "Fecha", "Hora", "Línea", "Formato", "Zona", "Humedad (%)", "Responsable", "Observaciones"
        ]
        ws.append(headers)

        # Insertar los datos
        for record in data:
            ws.append(list(record))

        cur.close()
        conn.close()

        # Guardar en memoria (BytesIO)
        output = BytesIO()
        wb.save(output)
        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name="registro-humedades.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

