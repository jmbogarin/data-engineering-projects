import pandas as pd

df = pd.read_parquet('green_tripdata_2025-10.parquet', columns=[
    'lpep_pickup_datetime',
    'tip_amount'
])

df['hour'] = df['lpep_pickup_datetime'].dt.floor('h')

result = df.groupby('hour')['tip_amount'].sum().reset_index()
print(result.sort_values('tip_amount', ascending=False).head(5))