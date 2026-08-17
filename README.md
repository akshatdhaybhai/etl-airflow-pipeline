# ETL Airflow Pipeline 🚀

An end-to-end **production-ready ETL pipeline** that extracts crypto price data from CoinGecko API, transforms it with Pandas, loads it into MySQL, and orchestrates everything with Apache Airflow — all containerized with Docker for reproducible deployments.

## 🎯 Project Overview

This project demonstrates core **data engineering** skills:
- ✅ ETL pipeline design (Extract → Transform → Load)
- ✅ Data modeling and schema design
- ✅ Apache Airflow orchestration with DAGs
- ✅ Idempotent data loading (no duplicates)
- ✅ Docker containerization for reproducibility
- ✅ Error handling and retry logic

## 📊 Architecture
CoinGecko API (External Data Source)
↓
┌──────────────────────────────────┐
│ Docker Container Network │
├──────────────────────────────────┤
│ │
│ ┌─────────────┐ │
│ │ Extract │ │
│ │ (requests) │ │
│ └──────┬──────┘ │
│ ↓ │
│ ┌─────────────┐ │
│ │ Transform │ │
│ │ (pandas) │ │
│ └──────┬──────┘ │
│ ↓ │
│ ┌─────────────┐ │
│ │ Load │ │
│ │ (MySQL) │ │
│ └──────┬──────┘ │
│ ↓ │
│ ┌──────────────────────┐ │
│ │ Apache Airflow DAG │ │
│ │ (Scheduling, Retry) │ │
│ └──────────────────────┘ │
│ │
│ Orchestrates Extract/Transform/ │
│ Load with scheduling and │
│ failure handling │
│ │
└──────────────────────────────────┘
↓
MySQL Database
(etl_pipeline.crypto_prices)

## 🏗️ Project Structure

etl-airflow-pipeline/
├── extract.py # Fetches data from CoinGecko API
├── transform.py # Cleans & transforms with Pandas
├── load.py # Loads to MySQL (idempotent)
├── run_pipeline.py # Standalone pipeline runner
├── schema.sql # MySQL table definition
├── dags/
│ └── etl_dag.py # Airflow DAG definition
├── docker-compose.yml # Docker services (Airflow, MySQL, PostgreSQL)
├── requirements.txt # Python dependencies
├── README.md # This file
└── .gitignore # Git ignore rules


## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- Git
- Python 3.10+ (for local development)

### 1. Clone the Repository
```bash
git clone https://github.com/akshathhaybhai/etl-airflow-pipeline.git
cd etl-airflow-pipeline
```

### 2. Start Everything with Docker
```bash
docker-compose up -d
```

Wait 3-5 minutes for full initialization.

### 3. Access Airflow UI
Open browser: **http://localhost:8080**

**Login credentials:**
- Username: `admin`
- Password: `admin`

### 4. Create Database & Load Schema
```bash
# Create database
docker exec -it etl-airflow-pipeline-mysql-1 mysql -u root -pyourpassword -e "CREATE DATABASE etl_pipeline;"

# Load schema
Get-Content schema.sql | docker exec -i etl-airflow-pipeline-mysql-1 mysql -u root -pyourpassword etl_pipeline
```

### 5. Trigger the DAG
1. Click on `etl_crypto_pipeline` DAG
2. Click the play button (▶️)
3. Click "Trigger DAG"
4. Watch all 3 tasks turn green ✅

### 6. Verify Data
```bash
docker exec -it etl-airflow-pipeline-mysql-1 mysql -u root -pyourpassword etl_pipeline -e "SELECT * FROM crypto_prices;"
```

## 📋 Design Decisions

### 1. **Single MySQL Table** (`crypto_prices`)
- **Why**: Simplicity for learning & interview. Real projects may use multiple normalized tables.
- **Tradeoff**: Less flexible schema, but easier to understand and maintain.

### 2. **Idempotency Strategy**
- **Method**: `INSERT ... ON DUPLICATE KEY UPDATE` with `UNIQUE KEY (coin_name)`
- **Why**: Prevents duplicate data if Airflow DAG retries or reruns
- **Benefit**: Safe to run pipeline multiple times on same day without duplicates

### 3. **Decimal Data Types**
- **Why**: `DECIMAL(15,2)` for prices (exact, not floating-point)
- **Risk with floats**: 63502.00 might become 63502.0000000001 in floating-point
- **Benefit**: Accurate financial data

### 4. **CoinGecko API** (Data Source)
- **Why**: No API key required, simple JSON, free tier unlimited
- **Alternative**: OpenWeatherMap, Exchangerate.host, NASA APOD
- **Benefit**: Focus on pipeline logic, not authentication

### 5. **Airflow SequentialExecutor**
- **Current**: Single-threaded execution (development)
- **Production**: Use CeleryExecutor or KubernetesExecutor for parallel tasks
- **Note**: Scheduler warning about SequentialExecutor is expected for local dev

### 6. **Docker Compose for Orchestration**
- **Why**: Single `docker-compose up` runs entire stack
- **Includes**: Airflow webserver, scheduler, PostgreSQL, MySQL
- **Benefit**: Reproducibility (works on any machine with Docker)

## 🔍 How It Works

### Pipeline Flow
1. **Extract** (`extract_task`): 
   - Calls CoinGecko API
   - Fetches Bitcoin, Ethereum, Cardano, Solana prices
   - Saves raw JSON to `raw/` folder (data lake pattern)

2. **Transform** (`transform_task`):
   - Loads raw JSON
   - Removes null values
   - Converts to proper data types (floats, timestamps)
   - Deduplicates
   - Returns clean DataFrame

3. **Load** (`load_task`):
   - Connects to MySQL
   - Upserts data using `INSERT ... ON DUPLICATE KEY UPDATE`
   - Ensures no duplicates on rerun

### Airflow DAG Orchestration
- **Schedule**: `@daily` (runs every day at 00:00 UTC)
- **Retries**: 2 retries with 5-minute delay on failure
- **Dependencies**: extract → transform → load (automatic sequencing)
- **XCom**: Tasks pass data via Airflow's cross-communication feature

## 📊 Example Output

### MySQL Data
id	coin_name	price_usd	market_cap_usd	volume_24h_usd	fetched_at
1	bitcoin	63502.00	1274527244533.56	14245435199.50	2026-08-17 10:44:15
2	ethereum	1902.66	229591491737.28	5264461975.02	2026-08-17 10:44:15
3	cardano	0.17	6494742203.71	1964922231.08	2026-08-17 10:44:15
4	solana	75.61	4407077599.49	1051924389.42	2026-08-17 10:44:15

## 🛠️ Technologies Used

| Component | Technology | Version |
|-----------|-----------|---------|
| **Orchestration** | Apache Airflow | 2.7.0 |
| **ETL** | Python, Pandas | 3.11 |
| **Database** | MySQL | 8.0 |
| **Metadata DB** | PostgreSQL | 13 |
| **Containerization** | Docker | Latest |
| **API** | CoinGecko (free) | v3 |

## 💡 Interview Preparation

### Questions You'll Be Asked
1. **"Walk me through what happens when your DAG runs"**
   - Extract → Transform → Load, with Airflow orchestrating tasks and handling retries

2. **"What would happen if the API was down when your pipeline ran?"**
   - Airflow would retry twice (configured in DAG), then mark task as failed with alert capability

3. **"How do you avoid duplicate data if the pipeline runs twice?"**
   - Using `INSERT ... ON DUPLICATE KEY UPDATE` with UNIQUE constraint on coin_name and date

4. **"Why did you choose this schema design?"**
   - Simple single table for MVP; normalized schema would scale better; DECIMAL for financial data accuracy

5. **"How would you scale this if data was 100x bigger?"**
   - Partitioning by date; Spark for distributed processing; Kafka for streaming; batch processing

### What You Can Say
- "Built end-to-end ETL pipeline extracting crypto data, transforming with Pandas, loading into MySQL"
- "Orchestrated scheduling & monitoring with Apache Airflow DAG with retry logic"
- "Implemented idempotent loads using INSERT ... ON DUPLICATE KEY UPDATE to prevent duplicates"
- "Containerized entire pipeline with Docker for reproducible deployment"
- "Designed MySQL schema with attention to data types (DECIMAL), constraints, and duplicate handling"

## 🐛 Troubleshooting

### Airflow UI not loading
```bash
docker-compose restart airflow-webserver
# Wait 2 minutes and refresh
```

### DAG not appearing
```bash
docker-compose restart airflow-scheduler
# Wait 1 minute and refresh
```

### Database connection error
```bash
# Recreate MySQL container
docker-compose down
docker volume rm etl-airflow-pipeline_mysql_data
docker-compose up -d
```

### Check logs
```bash
docker-compose logs airflow-scheduler
docker-compose logs mysql
```

## 📈 Future Enhancements

- [ ] Add email alerts on DAG failure
- [ ] Implement CeleryExecutor for parallel task execution
- [ ] Add data quality checks (Great Expectations)
- [ ] Create Power BI dashboard for crypto prices
- [ ] Add more data sources (stocks, forex, commodities)
- [ ] Implement incremental loads (only fetch updated prices)
- [ ] Add monitoring & alerting (Prometheus, Grafana)

## 📝 License

Open source - free to use for learning and projects

## 👤 Author

Akshat Dhaybhai
