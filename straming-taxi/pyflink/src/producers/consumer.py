import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'green-trips',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

count = 0

for message in consumer:
    trip = message.value
    if trip['trip_distance'] > 5.0:
        count += 1
    print(f'Count so far: {count}', end='\r')