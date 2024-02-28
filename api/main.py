from flask import Flask, request, jsonify
import json
import sqlite3
app = Flask(__name__)

"""
Run with python main.py
"""

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("solar.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route("/solar", methods=["GET", "POST"])
def solars():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM solar")
        solars = [
            dict(id=row[0], solar_power=row[1], solar_voltage=row[2], solar_current=row[3], battery_voltage=row[4], battery_current=row[5], 
            battery_temp=row[6], load_current=row[7], load_voltage=row[8] )
            for row in cursor.fetchall()
        ]
        if solars is not None:
            return jsonify(solars)

    if request.method == "POST":
        print(request.form)
        new_solar_power = request.form["solar_power"]
        new_solar_voltage = request.form["solar_voltage"]
        new_solar_current = request.form["solar_current"]
        new_battery_voltage = request.form["battery_voltage"]
        new_battery_current = request.form["battery_current"]
        new_battery_temp = request.form["battery_temp"]
        new_load_current = request.form["load_current"]
        new_load_voltage = request.form["load_voltage"]
        
        sql = """INSERT INTO solar (solar_power, solar_voltage, solar_current, battery_current, battery_temp, battery_voltage, 
        load_current, load_voltage)
                    values (?, ?, ?, ?, ?, ?, ?, ?)"""
        cursor = conn.execute(sql, (new_solar_power, new_solar_voltage, new_solar_current, new_battery_voltage, new_battery_current,
        new_battery_temp, new_load_current, new_load_voltage ))
        conn.commit()
        return f"Book with the id: {cursor.lastrowid} created successfully", 201

@app.route("/")
def hello():
    return "Hejsann allihpppe"

@app.route("/test")
def test():
    return "This is a test!!"



@app.route("/<argument>")
def argument(argument):
    return f"The argument is {argument}, insane!"


if __name__ == "__main__":
    app.run(debug=True)