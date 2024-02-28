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

try:
    cursor.execute(sql_query)
    
except Exception as e:
    print(f"Error message: {e}")
