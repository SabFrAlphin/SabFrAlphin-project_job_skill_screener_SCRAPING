
# Linkedin job ad webscraping

## Objective:
Create a dynamic web scraper, that will get job advertising data for the Berlin tech job market, stores them in a postgres SQL database.
- Data Scientist
- Data Analyst
- Data Engineer

This data collection in Part I of II. The collected data will be the foundation to run machine learning on in [Part II](https://github.com/SabFrAlphin/project_job_skill_screener_DATA_ML)


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
- scrapes list of Urls and adds labes 'FALSE' to database column 'Is_Scraped'
- once Url metadata is scraped, label will be switched to 'TRUE'
![structurejobs](/98_presentation/structure_jobsUrls.jpeg)


2. 'MainWithoutLogin.py' to scrape all metadata from linkedin
- stores all metadata found on one specific linkedin job add per row
- calculates the time job was added based on information 'job_ad_duration' and adds result to column 'date_added'
![structurespecifications](/98_presentation/structure_specifications.jpeg)
