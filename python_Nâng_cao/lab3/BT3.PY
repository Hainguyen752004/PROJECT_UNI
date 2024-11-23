from flask import Flask, render_template, request, jsonify
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Config Database
DATABASE_CONFIG = {
    'dbname': 'db_cacu',
    'user': 'postgres',
    'password': 'hainguyen752004',
    'host': 'localhost',
    'port': '5432'
}

# Connect to Database
def get_db_connection():
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# Routes
@app.route('/')
def index():
    columns = ["hoten", "tuoi", "gioitinh", "quequan", "CCCD", "ngaysinh"]
    return render_template('index.html', columns=columns)

@app.route('/api/data', methods=['GET'])
def get_data():
    columns = request.args.getlist('columns[]')
    if not columns:
        return jsonify({"error": "Vui lòng chọn ít nhất một cột"}), 400

    query = sql.SQL("SELECT {} FROM public.\"Thong_tin\"").format(
        sql.SQL(', ').join(map(sql.Identifier, columns))
    )

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()

        return jsonify({"data": rows, "columns": columns})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/data', methods=['POST'])
def add_data():
    data = request.json
    try:
        query = sql.SQL("""
            INSERT INTO public."Thong_tin" (hoten, tuoi, gioitinh, quequan, "CCCD", ngaysinh)
            VALUES (%s, %s, %s, %s, %s, %s)
        """)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, (
            data['hoten'],
            data['tuoi'],
            data['gioitinh'],
            data['quequan'],
            data['CCCD'],
            data['ngaysinh']
        ))
        conn.commit()
        conn.close()

        return jsonify({"message": "Dữ liệu đã được thêm"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/data', methods=['PUT'])
def update_data():
    data = request.json
    try:
        query = sql.SQL("""
            UPDATE public."Thong_tin"
            SET hoten = %s, tuoi = %s, gioitinh = %s, quequan = %s, ngaysinh = %s
            WHERE "CCCD" = %s
        """)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, (
            data['hoten'],
            data['tuoi'],
            data['gioitinh'],
            data['quequan'],
            data['ngaysinh'],
            data['CCCD']
        ))
        conn.commit()
        conn.close()

        return jsonify({"message": "Dữ liệu đã được cập nhật"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/data', methods=['DELETE'])
def delete_data():
    cccd = request.json.get('CCCD')
    if not cccd:
        return jsonify({"error": "Không có dữ liệu CCCD để xóa"}), 400

    try:
        query = sql.SQL("DELETE FROM public.\"Thong_tin\" WHERE \"CCCD\" = %s")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, (cccd,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Dữ liệu đã được xóa"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
