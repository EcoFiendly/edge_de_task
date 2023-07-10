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