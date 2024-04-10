import sqlite3

conn = sqlite3.connect("solar.sqlite")

cursor = conn.cursor()
sql_query = """CREATE TABLE solar (
    id integer PRIMARY KEY,
    solar_power DOUBLE,
    solar_voltage DOUBLE,
    solar_current DOUBLE,
    battery_voltage DOUBLE,
    battery_current DOUBLE,
    battery_temp DOUBLE,
    load_current DOUBLE,
    load_voltage DOUBLE

    ) """

sql_query2 = """CREATE TABLE solar_position (
    id integer PRIMARY KEY,
    yaw DOUBLE,
    pitch DOUBLE

    )"""

q = """ALTER TABLE solar_position ADD COLUMN created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP"""
x = """ALTER TABLE solar ADD COLUMN created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP"""
test = """INSERT INTO solar_position (yaw, pitch) VALUES (300.5, 500.5)"""
fetch = """SELECT yaw, pitch FROM solar_position ORDER BY created_time DESC LIMIT 1"""
try:
    # cursor.execute(test)
    cursor.execute(fetch)
    # conn.commit()
    data = cursor.fetchall()
    yaw, pitch = data[0]

    print(yaw, pitch)
    conn.close()

except Exception as e:
    print(f"Error message: {e}")
