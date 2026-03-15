import json
import pandas as pd
from kafka import KafkaProducer
from time import time

# Serializador: convierte dict a bytes JSON
def json_serializer(data):
    return json.dumps(data).encode('utf-8')

# Conectarse a Redpanda (que habla protocolo Kafka)
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=json_serializer
)

# Verificar conexión
print(producer.bootstrap_connected())

# Leer solo las columnas que pide el homework
columns = [
    'lpep_pickup_datetime',
    'lpep_dropoff_datetime',
    'PULocationID',
    'DOLocationID',
    'passenger_count',
    'trip_distance',
    'tip_amount',
    'total_amount'
]

df = pd.read_parquet('green_tripdata_2025-10.parquet', columns=columns)

# Medir el tiempo de envío
t0 = time()

for _, row in df.iterrows():
    message = row.where(pd.notnull(row), None).to_dict()
    
    # Convertir datetimes a string (JSON no soporta Timestamp)
    message['lpep_pickup_datetime'] = str(message['lpep_pickup_datetime'])
    message['lpep_dropoff_datetime'] = str(message['lpep_dropoff_datetime'])
    
    producer.send('green-trips', value=message)

producer.flush()

t1 = time()
print(f'took {(t1 - t0):.2f} seconds')