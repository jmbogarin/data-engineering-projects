import dlt
import requests
import duckdb

# 1. Probamos la API manualmente primero
print("Probando conexión a la API...")
response = requests.get("https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api?limit=10")
data = response.json()
print(f"API responde correctamente con {len(data)} registros.")

# 2. Definimos una función simple que entrega los datos
@dlt.resource(name="trips", write_disposition="replace")
def fetch_taxi_data():
    url = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"
    page = 1
    while True:
        print(f"Fetching page {page}...")
        params = {"page": page, "limit": 1000}
        r = requests.get(url, params=params)
        page_data = r.json()
        if not page_data: # Si la página está vacía, paramos
            break
        yield page_data
        page += 1
        

# 3. Corremos el pipeline
if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="taxi",
        destination="duckdb",
        dataset_name="taxi_data"
    )
    
    print("Cargando datos en DuckDB...")
    info = pipeline.run(fetch_taxi_data())
    print(info)

    # 4. Verificación final
    conn = duckdb.connect("taxi.duckdb")
    print("\nConteo de filas en la tabla:")
    print(conn.sql("SELECT count(*) FROM taxi_data.trips").show())