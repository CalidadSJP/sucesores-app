from flask import Blueprint, request, jsonify
from core.database import get_db_connection


weightB1_bp = Blueprint("weightB1", __name__)

@weightB1_bp.route('/save-weight-control-B1', methods=['POST'])
def save_weight_control():
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1️⃣ Insertar cabecera
        cursor.execute("""
            INSERT INTO weight_controls_B1 (
                control_date,
                net_weight,
                brand,
                lot,
                packaging_responsible,
                manufacture_date,
                expiry_date
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            data['date'],
            data['net_weight'],
            data['brand'],
            data['lot'],
            data['packaging_responsible'],
            data['manufacture_date'],
            data['expiry_date']
        ))

        weight_control_id = cursor.fetchone()[0]

        # 2️⃣ Insertar pesos primarios
        for index, weight in enumerate(data['primary_weights'], start=1):
            if weight is not None:
                cursor.execute("""
                    INSERT INTO weight_control_weights (
                        weight_control_id,
                        weight_value,
                        weight_group,
                        position
                    )
                    VALUES (%s, %s, %s, %s)
                """, (
                    weight_control_id,
                    weight,
                    'PRINCIPAL',
                    index
                ))

        # 3️⃣ Insertar pesos secundarios (si existen)
        for index, weight in enumerate(data.get('secondary_weights', []), start=1):
            if weight is not None:
                cursor.execute("""
                    INSERT INTO weight_control_weights (
                        weight_control_id,
                        weight_value,
                        weight_group,
                        position
                    )
                    VALUES (%s, %s, %s, %s)
                """, (
                    weight_control_id,
                    weight,
                    'SECUNDARIO',
                    index
                ))

        conn.commit()

        return jsonify({
            'message': 'Registro guardado correctamente',
            'id': weight_control_id
        }), 201

    except Exception as e:
        conn.rollback()
        print(e)
        return jsonify({'error': 'Error al guardar el control de peso'}), 500

    finally:
        cursor.close()
        conn.close()
