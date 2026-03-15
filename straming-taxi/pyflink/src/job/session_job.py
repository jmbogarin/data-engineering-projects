from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.watermark_strategy import WatermarkStrategy, TimestampAssigner
from pyflink.common.time import Duration
from pyflink.datastream.window import EventTimeSessionWindows
import json
import psycopg2
from datetime import datetime

def parse_message(msg):
    try:
        data = json.loads(msg)
        dt = datetime.strptime(data['lpep_pickup_datetime'], '%Y-%m-%d %H:%M:%S')
        ts = int(dt.timestamp() * 1000)
        return (data['PULocationID'], ts)
    except:
        return None

class PickupTimestampAssigner(TimestampAssigner):
    def extract_timestamp(self, value, record_timestamp):
        return value[1]

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    env.enable_checkpointing(10000)

    source = KafkaSource.builder() \
        .set_bootstrap_servers('redpanda-1:29092') \
        .set_topics('green-trips') \
        .set_starting_offsets(KafkaOffsetsInitializer.earliest()) \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .build()

    watermark_strategy = WatermarkStrategy \
        .for_bounded_out_of_orderness(Duration.of_seconds(5)) \
        .with_timestamp_assigner(PickupTimestampAssigner())

    stream = env.from_source(source, watermark_strategy, 'green-trips-source') \
        .map(parse_message) \
        .filter(lambda x: x is not None) \
        .key_by(lambda x: x[0]) \
        .window(EventTimeSessionWindows.with_gap(Duration.of_minutes(5))) \
        .apply(lambda key, window, inputs, out: out.collect((
            key,
            window.start,
            window.end,
            len(list(inputs))
        )))

    def write_to_postgres(record):
        conn = psycopg2.connect(
            host='postgres', port=5432,
            database='postgres', user='postgres', password='postgres'
        )
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO trips_sessions (PULocationID, window_start, window_end, num_trips)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (window_start, PULocationID) DO UPDATE SET num_trips = EXCLUDED.num_trips
        """, (
            record[0],
            datetime.fromtimestamp(record[1]/1000),
            datetime.fromtimestamp(record[2]/1000),
            record[3]
        ))
        conn.commit()
        cur.close()
        conn.close()

    stream.map(write_to_postgres)
    env.execute('session_job')

if __name__ == '__main__':
    main()