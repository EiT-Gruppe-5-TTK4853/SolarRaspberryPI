from flask import Flask, request, jsonify
from functions import fetch_position, move_model
import sqlite3
import logging

app = Flask(__name__)


"""
Run with python main.py
"""

logger = logging.getLogger(__name__)


# Function to get a database connection.
def get_db_connection():
    try:
        conn = sqlite3.connect("solar.sqlite")
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
        print(e)
        return None


@app.route("/solar", methods=["GET"])
def get_solar_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM solar ORDER BY id DESC LIMIT 1")
    solar_entrie = cursor.fetchall()

    # Convert query results to a list of dicts
    solar_data = dict(solar_entrie[0])

    conn.close()
    return jsonify(solar_data)


@app.route("/solar/all", methods=["GET"])
def get_all_solar_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM solar")
    solar_entries = cursor.fetchall()

    # Convert query results to a list of dicts
    solar_data = [dict(row) for row in solar_entries]

    conn.close()
    return jsonify(solar_data)


@app.route("/solar/position", methods=["GET"])
def get_solar_position():
    response = fetch_position()
    print(jsonify(response))
    return jsonify(response)


@app.route("/solar", methods=["POST"])
def post_solar_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        data = request.json
        print(data)
        cursor.execute(
            """
                INSERT INTO solar (solar_power, solar_voltage, solar_current, battery_voltage, battery_current, battery_temp, load_current, load_voltage)
                VALUES (:solar_power, :solar_voltage, :solar_current, :battery_voltage, :battery_current, :battery_temp, :load_current, :load_voltage)
                """,
            data,
        )
        conn.commit()
        conn.close()
        return {"message": "Data inserted"}, 201
    except Exception as e:
        return {"message": str(e)}, 500


@app.route("/solar/<int:id>", methods=["DELETE"])
def delete_solar_data(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the entry exists
    cursor.execute("SELECT * FROM solar WHERE id = ?", (id,))
    entry = cursor.fetchone()
    if entry is None:
        conn.close()
        return jsonify({"message": "Data not found"}), 404

    # Delete the entry
    cursor.execute("DELETE FROM solar WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Data deleted successfully"}), 200


@app.route("/solar/move", methods=["PUT"])
def control_solar_panel():

    data = None

    try:
        data = request.json
    except Exception as e:
        logger.info("Parse to JSON failed")
        return jsonify({"error": f"Request must be JSON. {str(e)}"}), 400

    if not data:
        logger.info(f"No data. Received {data}")
        return jsonify({"error": "Request must be JSON"}), 400

    if "pitch" not in data or not isinstance(data["pitch"], float):
        logger.info(f"No pitch or not wrong type. Received: {data}")
        return (
            jsonify(
                {"error": f"Missing pitch key or value in request. Received {data}"}
            ),
            400,
        )

    if "yaw" not in data or not isinstance(data["yaw"], float):
        logger.info(f"No yaw or not wrong type. Received: {data}")
        return (
            jsonify({"error": f"Missing yaw key or value in request. Received {data}"}),
            400,
        )

    # Update the angle setting
    yaw, pitch = 0, 0
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch latest position
        cursor.execute(
            "SELECT yaw, pitch FROM solar_position ORDER BY created_time DESC LIMIT 1"
        )
        position_raw = cursor.fetchall()
        yaw, pitch = position_raw[0]

        conn.close()
        logger.info(f"Data yaw: {yaw}, pitch: {pitch} queried from db")
    except Exception as e:
        print("It dont work fetching")
        return jsonify({"error": str(e)}), 500

    # Move model
    response = move_model(data["pitch"], data["yaw"], pitch, yaw)
    z_steps = response["z_steps"]
    y_steps = response["y_steps"]

    print("z_steps", z_steps, "y_steps", y_steps)

    if response["z_steps"] == 0 and response["y_steps"] == 0:
        return (
            jsonify("Model not moved, no steps required to reach target position"),
            204,
        )

    data["pitch"] = pitch if y_steps == 0 else data["pitch"]
    data["yaw"] = yaw if z_steps == 0 else data["yaw"]

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO solar_position (yaw, pitch) VALUES (:yaw, :pitch)""",
            data,
        )
        conn.commit()
        conn.close()
        logger.info(f"Data {data} inserted")
    except Exception as e:
        print("It dont work inserting")
        return jsonify({"error": str(e)}), 500

    # Return the updated setting
    return jsonify(response["message"]), 200


logging.basicConfig(
    filename="main.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)

if __name__ == "__main__":
    logging.info("Api starting...")
    app.run(debug=True, host="0.0.0.0")  # Run api
