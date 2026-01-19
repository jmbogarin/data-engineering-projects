--Question 3
SELECT
    COUNT(*) AS short_trips
FROM green_tripdata_2025_11
WHERE lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime <  '2025-12-01'
  AND trip_distance <= 1;

  
--Question 4
WITH daily_max AS (
    SELECT
        DATE(lpep_pickup_datetime) AS pickup_day,
        MAX(trip_distance) AS max_trip_distance
    FROM green_tripdata_2025_11
    WHERE trip_distance < 100
    GROUP BY DATE(lpep_pickup_datetime)
)
SELECT pickup_day
FROM daily_max
ORDER BY max_trip_distance DESC
LIMIT 1;


--Question 5
SELECT
    z.zone AS pickup_zone,
    SUM(t.total_amount) AS total_revenue
FROM green_tripdata_2025_11 t
JOIN taxi_zone_lookup z
  ON t.pulocationid = z.locationid
WHERE t.lpep_pickup_datetime >= '2025-11-18'
  AND t.lpep_pickup_datetime <  '2025-11-19'
GROUP BY z.zone
ORDER BY total_revenue DESC
LIMIT 1;

--Question 6
SELECT
    z_do.zone AS dropoff_zone,
    MAX(t.tip_amount) AS max_tip
FROM green_tripdata_2025_11 t
JOIN taxi_zone_lookup z_pu
  ON t.pulocationid = z_pu.locationid
JOIN taxi_zone_lookup z_do
  ON t.dolocationid = z_do.locationid
WHERE z_pu.zone = 'East Harlem North'
  AND t.lpep_pickup_datetime >= '2025-11-01'
  AND t.lpep_pickup_datetime <  '2025-12-01'
GROUP BY z_do.zone
ORDER BY max_tip DESC
LIMIT 1;
