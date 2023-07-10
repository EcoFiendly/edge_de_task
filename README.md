# Edge-task

## Requirements
Develop a maintainable data pipeline in 3 hours that will:
- pick up new data file when it's published
- clean and process the data
- produce an output

## Project
Data engineering project on the English Prescribing Dataset (EPD)

## Architecture
Usage of docker for reproducibility
Containers can easily be hosted and on the cloud

Dataset is published in monthly versions.
Due to the size of the full monthly data set (23.7GB), I've decided to narrow it down by selecting records with postcode starting with SW17
Overall outline below + diagram:
1. Extract: scrape data from NHS Open Data Portal Business Services Authority through their public API
2. Transform: Apply data modelling
3. Load: Transformed data pushed to transformed db
4. Ready to hand over to viz/analysts

### Datastore
The dbs persist between runs via the volumn, new data will be transformed and appended to the existing
SQLite used because it is small, quick and easy for prototyping a task
In production, I would probably use PostgreSQL instead:
    PostgreSQL supports more data types. SQLite Nly supports basics, eg no datetime, uses functions instead
    PostgresQL handles small and medium queries much better than SQLite
    PostgrSQL handles concurrency better than SQLite

### Extract
Sends a `SELECT *` query to the API
Exits if response isn't success

### Transform
Since the data came from NHSBSA's data warehouse, it was already aggregated and conformed
I tried to apply data modelling to the data best I could, it is challenging without the input of end users

### Load
Creates schema on SQLite db
Loads data to output db