# Una vez terminada la carga, consultamos DuckDB
import duckdb

conn = duckdb.connect("taxi.duckdb")

# Consultas para el examen
print("\n" + "="*30)
print("   RESULTADOS DEL WORKSHOP")
print("="*30)

# Q1: Fechas (ajustado a los nombres de tus columnas del log)
fechas = conn.sql("SELECT min(trip_pickup_date_time), max(trip_pickup_date_time) FROM taxi_data.trips").fetchone()
print(f"Pregunta 1: {fechas[0]} hasta {fechas[1]}")

# Q2: Proporción de tarjetas
tarjetas = conn.sql("""
    SELECT (COUNT(CASE WHEN payment_type = 'Credit' THEN 1 END) * 100.0 / COUNT(*)) 
    FROM taxi_data.trips
""").fetchone()
print(f"Pregunta 2 (Credit Card %): {round(tarjetas[0], 2)}%")

# Q3: Propinas
propinas = conn.sql("SELECT SUM(tip_amt) FROM taxi_data.trips").fetchone()
print(f"Pregunta 3 (Total Tips): ${round(propinas[0], 2)}")
print("="*30)