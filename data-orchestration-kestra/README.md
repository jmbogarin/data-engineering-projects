# Data Orchestration Demo with Kestra, PostgreSQL, and GCP

## Overview

This repository demonstrates a **modern data orchestration setup using Kestra** as an alternative to traditional schedulers like Airflow.  
The goal is to showcase how to design, run, and schedule a production-style data pipeline using declarative YAML flows, containerized services, and cloud data warehouses.

The project focuses on:
- Running **Kestra locally with Docker Compose**
- Using **PostgreSQL** both as an application database and as a data destination
- Orchestrating a **scheduled end-to-end pipeline** that ingests NYC Taxi CSV data and loads it into **Google BigQuery**

This setup is intentionally minimal but realistic, aiming to mirror how a Data Engineer would prototype or validate orchestration logic before moving to a fully managed environment.

---

## Architecture

### Services (Docker Compose)

The `docker-compose.yaml` file spins up the following services:

- **PostgreSQL (`pgdatabase`)**
  - Acts as the analytical database for taxi data
  - Used by Kestra JDBC tasks for table creation, staging, and merges

- **Kestra**
  - The workflow orchestrator
  - Executes flows, manages task dependencies, artifacts, retries, and scheduling
  - Uses its own internal PostgreSQL database for metadata, execution state, and logs

- **Kestra PostgreSQL (`kestra_postgres`)**
  - Dedicated database for Kestra internals
  - Stores executions, task states, artifacts metadata, and flow definitions

All services run on the same Docker network and communicate via service names, without exposing unnecessary ports to the host.

---

## Orchestrated Pipeline: `gcp_taxi_scheduled`

The main flow demonstrates a **scheduled batch ingestion pipeline** for NYC Taxi data.

### High-level flow logic

1. **Trigger (Schedule)**
   - Runs monthly using cron expressions
   - Supports backfills for historical periods

2. **Extract**
   - Downloads compressed CSV files from a public data source
   - Decompresses them into execution-scoped artifacts

3. **Load to PostgreSQL**
   - Creates target and staging tables if they don’t exist
   - Loads CSV data into a staging table
   - Generates deterministic row identifiers
   - Merges new data into the final table (idempotent load)

4. **Load to BigQuery**
   - Uploads raw files to GCS
   - Creates external and native BigQuery tables
   - Merges data into partitioned tables

5. **Cleanup**
   - Removes execution artifacts to avoid unnecessary storage growth

### Supported features

- Conditional logic for **Yellow vs Green taxi schemas**
- Parameterized execution (taxi type, date)
- Safe re-execution and backfills
- Separation of infrastructure, orchestration, and data logic

---

## Why Kestra?

This demo intentionally avoids Airflow to explore a different orchestration model:

- Declarative YAML flows instead of Python DAGs
- Strong first-class support for:
  - Artifacts
  - Containers
  - JDBC operations
  - Conditional logic
- Clear separation between **execution context** and **infrastructure**
- Easier local development experience with Docker

The objective is not to replace Airflow, but to understand how alternative orchestrators approach the same problems with different abstractions.

---

## Learnings

- Orchestration is **more about state, idempotency, and scheduling** than raw data processing
- Declarative workflows reduce boilerplate for common ETL patterns
- Artifacts are a powerful abstraction for passing data between tasks without tight coupling
- Backfills and scheduled runs must be designed explicitly, not as an afterthought
- Infrastructure (databases, buckets, datasets) should ideally be provisioned separately from orchestration logic
- Running an orchestrator locally helps deeply understand execution semantics before scaling

---

## Final Notes

This project is intended as a **learning and experimentation environment**, not a production deployment.  
However, the patterns used here closely resemble real-world data engineering workflows and can be extended to more complex pipelines with minimal changes.
