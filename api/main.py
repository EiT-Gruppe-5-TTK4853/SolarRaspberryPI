from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)


"""
Run with python main.py
"""

# Function to get a database connection.
def get_db_connection():
    try:
        conn = sqlite3.connect('solar.sqlite')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(e)
        return None

@app.route('/solar', methods=['GET'])
def get_solar_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM solar')
    solar_entries = cursor.fetchall()
    
    # Convert query results to a list of dicts
    solar_data = [dict(row) for row in solar_entries]
    
    conn.close()
    return jsonify(solar_data)

@app.route('/solar', methods=['POST'])
def post_solar_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        data = request.json
        print(data)
        cursor.execute("""
                INSERT INTO solar (solar_power, solar_voltage, solar_current, battery_voltage, battery_current, battery_temp, load_current, load_voltage)
                VALUES (:solar_power, :solar_voltage, :solar_current, :battery_voltage, :battery_current, :battery_temp, :load_current, :load_voltage)
                """, data)
        conn.commit()
        conn.close()
        return {"message": "Data inserted"}, 201
    except Exception as e:
        return {"message": str(e)}, 500

@app.route('/solar/<int:id>', methods=['DELETE'])
def delete_solar_data(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if the entry exists
    cursor.execute('SELECT * FROM solar WHERE id = ?', (id,))
    entry = cursor.fetchone()
    if entry is None:
        conn.close()
        return jsonify({"message": "Data not found"}), 404
    
    # Delete the entry
    cursor.execute('DELETE FROM solar WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Data deleted successfully"}), 200

# @app.route("/solar", methods=["GET", "POST"])
# def solars():
#     conn = db_connection()
#     cursor = conn.cursor()

#     if request.method == "GET":
#         cursor = conn.execute("SELECT * FROM solar")
#         solars = [
#             dict(id=row[0], solar_power=row[1], solar_voltage=row[2], solar_current=row[3], battery_voltage=row[4], battery_current=row[5], 
#             battery_temp=row[6], load_current=row[7], load_voltage=row[8] )
#             for row in cursor.fetchall()
#         ]
#         if solars is not None:
#             return jsonify(solars)

#     if request.method == "POST":
#         print(request.form)
#         new_solar_power = request.form["solar_power"]
#         new_solar_voltage = request.form["solar_voltage"]
#         new_solar_current = request.form["solar_current"]
#         new_battery_voltage = request.form["battery_voltage"]
#         new_battery_current = request.form["battery_current"]
#         new_battery_temp = request.form["battery_temp"]
#         new_load_current = request.form["load_current"]
#         new_load_voltage = request.form["load_voltage"]
        
#         sql = """INSERT INTO solar (solar_power, solar_voltage, solar_current, battery_current, battery_temp, battery_voltage, 
#         load_current, load_voltage)
#                     values (?, ?, ?, ?, ?, ?, ?, ?)"""
#         cursor = conn.execute(sql, (new_solar_power, new_solar_voltage, new_solar_current, new_battery_voltage, new_battery_current,
#         new_battery_temp, new_load_current, new_load_voltage ))
#         conn.commit()
#         return f"Book with the id: {cursor.lastrowid} created successfully", 201

# @app.route("/")
# def hello():
#     return "Hejsann allihpppe"

# @app.route("/test")
# def test():
#     return "This is a test!!"



# @app.route("/<argument>")
# def argument(argument):
#     return f"The argument is {argument}, insane!"


if __name__ == "__main__":
    app.run(debug=True)