# NYC Taxi Ingestion Project

## Overview

This project consists of a dockerized application that ingests New York City Green Taxi data into a PostgreSQL database for analysis and subsequent queries.

The project includes:
- **Data Ingestion**: Python script that downloads and loads datasets into PostgreSQL
- **Database**: PostgreSQL with pgAdmin web interface
- **Containers**: Docker Compose to orchestrate the infrastructure
- **Analytics**: SQL queries to answer business questions

## Key Learnings

- Understood Docker port mapping vs internal container networking
- Implemented one-shot batch ingestion using Docker Compose jobs
- Learned how Docker named volumes persist database state across restarts
- Applied SQL analytics on ingested datasets using PostgreSQL
- Clarified the difference between development orchestration (docker-compose) and production workflows


---

## Project Structure

```
nyc-taxi-ingestion/
├── ingest_data.py          # Main data ingestion script
├── queries.sql              # SQL analysis queries
├── pyproject.toml           # Dependency configuration (uv)
├── docker-compose.yaml      # Container orchestration
├── Dockerfile               # Docker service image
├── datasets.yaml            # Dataset configuration
├── .python-version          # Python version (3.13.10)
└── README.md               # This file
```

---

## Prerequisites

- **Docker**: v24.0 or higher
- **Docker Compose**: v2.0 or higher

---

## Installation and Setup

1. **Start the services**:
   ```bash
   docker compose up -d
   ```

   This brings up:
   - **PostgreSQL**: Port `5433` (host) → `5432` (container)
   - **pgAdmin**: Port `8080` for web interface

2. **Verify services are running**:
   ```bash
   docker compose ps
   ```

   Wait a few seconds for PostgreSQL to be fully initialized before running data ingestion.

---

## Usage

### Data Ingestion

The `ingest_data.py` script runs in a Docker container and downloads and loads data into PostgreSQL.

**Syntax**:
```bash
docker compose run --rm ingest --url <DATASET_URL> --table <TABLE_NAME>
```

The script automatically connects to the PostgreSQL service using the environment variables configured in `docker-compose.yaml`.

**Examples**:

1. **Download Green Taxi data (November 2025)**:
   ```bash
   docker compose run --rm ingest \
     --url https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet \
     --table green_tripdata_2025_11
   ```

2. **Download taxi zones**:
   ```bash
   docker compose run --rm ingest \
     --url https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv \
     --table taxi_zone_lookup
   ```

**Supported Formats**:
- `.parquet` - Downloaded with Pandas
- `.csv` - Downloaded with Pandas

**Environment Variables**:

The script uses the following environment variables (with defaults):
- `DB_HOST`: PostgreSQL host (default: `localhost`)
- `DB_PORT`: PostgreSQL port (default: `5433`)
- `DB_USER`: Database user (default: `postgres`)
- `DB_PASS`: Database password (default: `postgres`)
- `DB_NAME`: Database name (default: `ny_taxi`)

When running via Docker Compose, these are automatically configured.

---

## Datasets

### 1. Green Taxi Data (November 2025)
- **Table**: `green_tripdata_2025_11`
- **Source**: NYC TLC Data Release
- **Format**: Parquet
- **URL**: https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet
- **Description**: Green Taxi trip data including distance, time, fare, tips, etc.

### 2. Taxi Zone Lookup
- **Table**: `taxi_zone_lookup`
- **Source**: DataTalksClub
- **Format**: CSV
- **URL**: https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
- **Description**: Mapping of LocationID to geographic zone names

---

## Database Access

### pgAdmin (Web Interface)
- **URL**: http://localhost:8080
- **Email**: `admin@admin.com`
- **Password**: `admin`

**Steps to connect to PostgreSQL**:
1. Open pgAdmin
2. Click "Add New Server"
3. General tab - Name: any name (e.g., "NY Taxi")
4. Connection tab:
   - Host: `pgdatabase` (container name)
   - Port: `5432`
   - Username: `postgres`
   - Password: `postgres`
5. Save and connect

### Direct Connection (SQL Client)
```
Host: localhost
Port: 5433
User: postgres
Password: postgres
Database: ny_taxi
```

---

## SQL Analysis Queries

The `queries.sql` file contains queries to answer business questions:

### Question 3: Short Trips in November
Count of trips with distance ≤ 1 mile in November 2025.

### Question 4: Day with Longest Trip
Identifies the day with the longest trip distance in November 2025.

### Question 5: Revenue by Zone (November 18)
Sum of total revenue by pickup zone on November 18, 2025.

### Question 6: Maximum Tips from East Harlem North
Maximum tip amount by dropoff zone from "East Harlem North" in November.

---

## Infrastructure Configuration

### Docker Compose

**Services**:
- **pgdatabase**: Postgres 17 Alpine
- **pgadmin**: pgAdmin 4 for visual management

**Persistent Volumes**:
- `pgdata`: Stores PostgreSQL data
- `pgadmin_data`: Stores pgAdmin configuration

**Ports**:
- PostgreSQL: `5433:5432`
- pgAdmin: `8080:80`

### Dockerfile

Uses:
- **Base**: `python:3.13.10-slim`
- **Package Manager**: `uv` (included)
- **Dependencies**: Installed from `pyproject.toml` with `uv sync --locked`

---

## Dependencies

Specified in `pyproject.toml`:

| Library | Version | Purpose |
|---------|---------|---------|
| pandas | ≥2.3.3 | Data manipulation |
| psycopg2-binary | ≥2.9.11 | PostgreSQL adapter |
| pyarrow | ≥23.0.0 | Parquet support |
| sqlalchemy | ≥2.0.45 | Database ORM |

---

## Typical Workflow

1. **Start services**:
   ```bash
   docker compose up -d
   ```

2. **Wait for PostgreSQL to initialize** (10-15 seconds):
   ```bash
   docker compose logs pgdatabase
   ```

3. **Ingest Green Taxi data**:
   ```bash
   docker compose run --rm nyc-taxi-ingestion python ingest_data.py \
     --url https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet \
     --table green_tripdata_2025_11
   ```

4. **Ingest taxi zones**:
   ```bash
   docker compose run --rm nyc-taxi-ingestion python ingest_data.py \
     --url https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv \
     --table taxi_zone_lookup
   ```

5. **Run queries**:
   - Open pgAdmin at http://localhost:8080
   - Copy queries from `queries.sql`
   - Execute in the query editor

6. **Stop services**:
   ```bash
   docker compose down
   ```

---

## Troubleshooting

### Error: "Connection refused"
- Verify PostgreSQL is running: `docker compose ps`
- Wait 15-20 seconds after `docker compose up -d`
- Check logs: `docker compose logs pgdatabase`

### Error: "Permission denied" with Docker
- Add user to docker group:
  ```bash
  sudo usermod -aG docker $USER
  newgrp docker
  ```

### Error: Port 5433 already in use
- Change port in `docker-compose.yaml`: `"5434:5432"`
- Or stop the other service on that port

### pgAdmin not loading
- Clear browser cache (Ctrl+Shift+Delete)
- Restart the container: `docker compose restart pgadmin`

---

## Useful Commands

```bash
# View service status
docker compose ps

# View logs for a specific service
docker compose logs pgdatabase
docker compose logs pgadmin

# Execute commands in container
docker compose exec pgdatabase psql -U postgres -d ny_taxi

# Stop without removing data
docker compose stop

# Stop and remove data
docker compose down -v

# Rebuild images
docker compose build --no-cache
```

---

## Important Notes

- **Docker-based Ingestion**: The `ingest_data.py` script runs exclusively in Docker containers using `docker compose run`. This ensures consistency and avoids local environment issues.
- **Environment Variables**: Database credentials are configured via environment variables in `docker-compose.yaml`. In production, use secrets management tools.
- **Persistence**: PostgreSQL data persists in the `pgdata` volume even after stopping containers.
- **Python**: The project uses Python 3.13.10 as specified in `.python-version`.
- **uv**: Modern and fast Python package manager, alternative to pip/poetry.

---

## References

- [NYC TLC Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.html)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [pgAdmin Documentation](https://www.pgadmin.org/docs/)

