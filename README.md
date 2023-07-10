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

### Output and what I suggest could be done with it
The output is the data stored in fact and dimension tables in the SQLite db
I selected records with postcode starting with SW17 because that's where I live
It would be interesting to find out what is prescribed in the area
This can contribute to formulating a care plan for SW17 which can alleviate pressures on the local practices
Eg benefits program to improve the health of residents so they require less visits and prescription drugs

### Next steps
Automation: eg using CRON to schedule the data pull monthly
I focused on getting a working pipeline over automating a non working pipeline
Logging: Essential in production, for detecting anomalies during pipeline runs
Validation: Have a PK for dupe checking when pulling new data
Scalability: Have tools in place to handle large datasets in parallel if pipeline grows
Appending new data: As I'm following a data warehouse and ETL process, new dat will have to be normalised before being appended to tables in db. Tables will have to be deduped after
Research alternative methods for appending new data
Backup: Logging should be the first line of defense against bad data being pulled, but important to have duplicate databases as backup in case the data in db gets corrupted.


### Project vs my experience working with NHS data
My experience working with NHS data focuses more on dealing with Personal Identifiable Information (PID) and data conformation.
Sometimes BIs would upload Personal Identifiable Information (PID).
What I have done is to ensure PID gets discovered early, reported and deleted. And then request for a new upload of data from the clients.
Next would be conformation. Table names, field names and datatypes (datetimes in particular).
Due to the public data I used being from NHSBSA's data warehouse, there is no PID, and the dtypes are all right. Data is also aggregated.