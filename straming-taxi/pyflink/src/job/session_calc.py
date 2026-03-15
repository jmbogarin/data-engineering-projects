import pandas as pd

df = pd.read_parquet('green_tripdata_2025-10.parquet', columns=[
    'lpep_pickup_datetime',
    'PULocationID'
])

df = df.sort_values(['PULocationID', 'lpep_pickup_datetime'])

GAP = pd.Timedelta(minutes=5)

# Detectar inicio de nueva sesión
df['prev_time'] = df.groupby('PULocationID')['lpep_pickup_datetime'].shift(1)
df['new_session'] = (
    df['prev_time'].isna() | 
    (df['lpep_pickup_datetime'] - df['prev_time'] > GAP)
)

# Asignar ID de sesión
df['session_id'] = df.groupby('PULocationID')['new_session'].cumsum()

# Contar trips por sesión
result = df.groupby(['PULocationID', 'session_id']).size().reset_index(name='num_trips')

# La sesión más larga
top = result.sort_values('num_trips', ascending=False).head(5)
print(top)