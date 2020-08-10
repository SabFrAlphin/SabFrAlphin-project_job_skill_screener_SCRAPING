
# Linkedin job ad webscraping

## Objective:
Create a dynamic web scraper, that will get job advertising data for the Berlin tech job market, stores them in a postgres SQL database.
- Data Scientist
- Data Analyst
- Data Engineer

This data collection in Part I of II. The collected data will be the foundation to run machine learning on in Part II


## Structure:
The PostgreSQL database can either be run locally or e.g. via Amazon RDS.
![data structure](/98_presentation/data_structure.jpeg)

## Technical Requirements:

- copy the repo to your computer
- Postgres SQL: set up a new database ('linkedin')
- insert your postgres credential into 'PostgresConnection.py'
- create tables with SQL scripts 'create_table_jobsUrls' and 'create_table_Specifications'
- download latest chromedriver for your system [here] (https://chromedriver.chromium.org/)
- run python scripts consecutively
1. 'JobsUrls.py' for getting the job Urls
2. 'MainWithoutLogin.py' to scrape all metadata from linkedin
