# Financial Data Pipeline

## Overview

This project is an end-to-end data engineering pipeline that extracts financial company data from an external REST API, transforms and validates the data, and loads it into PostgreSQL.

The project is designed to practice and demonstrate core data engineering concepts such as ETL pipelines, data validation, workflow orchestration, containerization, automated testing, and database management.

## Architecture

```text
Financial Modeling Prep API
            |
            v
        Extraction
            |
            v
      Raw CSV Storage
            |
            v
      Transformation
            |
            v
    Staging CSV Storage
            |
            v
       Validation
            |
            v
          Load
        /      \
       v        v
Processed CSV  PostgreSQL
               Warehouse
```

The pipeline is orchestrated with Apache Airflow and runs inside Docker containers.

## ETL Workflow

### 1. Extract

Financial company data is retrieved from the Financial Modeling Prep API for a predefined list of stock symbols.

The extracted data includes:

- Symbol
- Company name
- Price
- Market capitalization
- Sector
- Industry
- Country
- Exchange

The raw data is stored in:

```text
data/raw/company_data.csv
```

### 2. Transform

The transformation stage:

- Removes duplicate rows
- Filters invalid prices
- Filters invalid market capitalizations
- Creates a `marketCap_billions` column

The transformed dataset is temporarily stored in:

```text
data/staging/company_data_transformed.csv
```

### 3. Validate

Before loading the data, several data quality checks are performed:

- Dataset must not be empty
- Required columns must be present
- Company symbols must be unique
- Prices must be positive
- Market capitalizations must be positive

If a validation fails, the pipeline stops before loading the data.

### 4. Load

Validated data is loaded into two destinations:

```text
data/processed/company_data_clean.csv
```

and a PostgreSQL data warehouse:

```text
financial_data
└── companies
```

## Orchestration

Apache Airflow orchestrates the pipeline using the TaskFlow API.

```text
extract
   ↓
transform
   ↓
validate
   ↓
load
```

The extraction task includes retries to handle temporary API or network failures.

The DAG currently uses:

```python
schedule=None
```

so pipeline executions are triggered manually during development.

## Technologies

- Python
- Pandas
- REST API
- PostgreSQL
- SQLAlchemy
- psycopg2
- Apache Airflow
- Docker
- Docker Compose
- Pytest
- Git
- GitHub

## Project Structure

```text
financial-data-pipeline/
│
├── dags/
│   └── financial_pipeline.py
│
├── src/
│   ├── config/
│   ├── extract.py
│   ├── transform.py
│   ├── validate.py
│   ├── load.py
│   └── main.py
│
├── test/
│
├── data/
│   ├── raw/
│   ├── staging/
│   └── processed/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Testing

Unit tests are implemented with Pytest.

Run the test suite with:

```bash
pytest test/ -v
```

or from the project virtual environment:

```bash
python -m pytest test/ -v
```

## Current Progress

- [x] REST API data extraction
- [x] Data transformation
- [x] Data quality validation
- [x] Unit testing
- [x] Docker containerization
- [x] Apache Airflow orchestration
- [x] PostgreSQL data warehouse
- [x] CSV and PostgreSQL loading
- [X] PostgreSQL UPSERT strategy
- [X] Historical financial data storage
- [ ] Automated pipeline scheduling
- [ ] CI/CD with GitHub Actions
- [ ] SQL analytics
- [ ] Data visualization dashboard

## Future Improvements

Planned improvements include:

- Replace full table replacement with PostgreSQL UPSERT logic
- Store historical price and market capitalization snapshots
- Add scheduled Airflow executions
- Add GitHub Actions for automated testing
- Improve database schema and constraints
- Add SQL analytics
- Build a data visualization dashboard