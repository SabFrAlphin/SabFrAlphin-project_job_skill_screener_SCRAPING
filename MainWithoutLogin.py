import time
import PostgresConnection as config
from bs4 import BeautifulSoup
from selenium import webdriver
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-error')
options.add_argument('ignore-ssl-errors')
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = dir_path + "/chromedriver"
browser = webdriver.Chrome(dir_path)
cur = config.conn.cursor()
selectUrls = """SELECT "Urls","Job_ID" FROM public."jobsUrls" WHERE "Is_Scraped" = false """
cur.execute(selectUrls)
jobUrls: list = cur.fetchall()
NoOfUrls = cur.rowcount
cur.close()

# function that convert posted time to timestamp


def timestamp_converstion(job_ad_duration):
    # it will convert like this into list "Vor 2 Stunden"
    text = job_ad_duration.split(' ')
    # it will become ['Vor','2','Stunden']
    timeText = text[2]  # select 3rd value = 'Stunden'
    timeAgo = int(text[1])  # select 2nd value and convert into int
    # match the value
    # time = datetime.now()
    if timeText == 'Sekunden' or timeText == 'Sekunde':
        time = datetime.now() - relativedelta(seconds=timeAgo)
    elif timeText == 'Minuten' or timeText == 'Minute':
        time = datetime.now() - relativedelta(minutes=timeAgo)
    elif timeText == 'Stunde' or timeText == 'Stunden':
        time = datetime.now() - relativedelta(hours=timeAgo)
    elif timeText == 'Tag' or timeText == 'Tagen':
        time = datetime.now() - relativedelta(days=timeAgo)
    elif timeText == 'Woche' or timeText == 'Wochen':
        time = datetime.now() - relativedelta(weeks=timeAgo)
    elif timeText == 'Monat' or timeText == 'Monate':
        time = datetime.now() - relativedelta(months=timeAgo)
    elif timeText == 'Jahr' or timeText == 'Jahre':
        time = datetime.now() - relativedelta(years=timeAgo)
    return time


for i in range(NoOfUrls):
    url = jobUrls[i][0]  # select urls from list // i is loop no and [0] is the column No
    Job_id = str(jobUrls[i][1])  # select urls from list // i is loop no and [0] is the column No
    print(Job_id)
    print(url)
    error = True
    tryCount = 0
    while error == True:        # if error accord due blocking it will be repeat
        error = False
        try:
            browser.get(url)        # load selected urls data
            time.sleep(1)  # Wait for avoid blocking
            soup = BeautifulSoup(browser.page_source, 'html.parser')     # load html data into soup

            job_title = soup.find(class_='topcard__title').get_text().strip()       # job title

            try:
                companyName = soup.find(
                    attrs={"data-tracking-control-name": "public_jobs_topcard_org_name"}).get_text().strip()
            except:  # if company have'nt website
                companyName = soup.find(class_='topcard__flavor').get_text().strip()

            job_location = soup.find(
                'span', class_="topcard__flavor topcard__flavor--bullet").get_text().strip()

            try:
                job_ad_duration = soup.find(
                    class_='topcard__flavor--metadata posted-time-ago__text posted-time-ago__text--new').get_text().strip()
            except:
                job_ad_duration = soup.find(
                    class_='topcard__flavor--metadata posted-time-ago__text').get_text().strip()

            try:
                job_applications = soup.find(
                    class_='topcard__flavor--metadata topcard__flavor--bullet num-applicants__figure').get_text().strip()
            except:
                job_applications = soup.find(class_='num-applicants__caption').get_text().strip()

            job_applications = [int(i) for i in job_applications.split()
                                if i.isdigit()][0]         # extract digite form text

            job_criteria = soup.find(class_='job-criteria__list')
            job_criteria = job_criteria.find_all(class_='job-criteria__item')
            try:
                seniority_level = ', '.join([criteria.get_text() for criteria in job_criteria[0].find_all(
                    class_='job-criteria__text job-criteria__text--criteria')])
            except:
                seniority_level = 'N/A'
            try:
                employment_type = ', '.join([criteria.get_text() for criteria in job_criteria[1].find_all(
                    class_='job-criteria__text job-criteria__text--criteria')])
            except:
                employment_type = 'N/A'
            try:
                job_functions = ', '.join([criteria.get_text() for criteria in job_criteria[2].find_all(
                    class_='job-criteria__text job-criteria__text--criteria')])
            except:
                job_functions = 'N/A'
            try:
                industry = ', '.join([criteria.get_text() for criteria in job_criteria[3].find_all(
                    class_='job-criteria__text job-criteria__text--criteria')])
            except:
                industry = 'N/A'

            date_added = timestamp_converstion(job_ad_duration)
            job_text = soup.find(class_='description').get_text().strip()
            cur = config.conn.cursor()      # create cursor of database
            try:
                # save query in variable
                postgres_insert_query = """INSERT INTO "Specifications"(url, language, job_title, job_location, company_name, "Job_Id", job_ad_duration, job_applications, seniority_level, industry, employment_type, job_functions, job_text, date_added, date_scraped)\
                VALUES (%s, '', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now()::timestamp);
            """
                # save data in variable as in INSERT query
                record_to_insert = (str(url), str(job_title), str(job_location), str(companyName), str(Job_id), str(job_ad_duration), str(
                    job_applications), str(seniority_level), str(industry), str(employment_type), str(job_functions), str(job_text), str(date_added))
                # execute query
                cur.execute(postgres_insert_query, record_to_insert)
                # commit data to database
                config.conn.commit()
                # close cursor
                cur.close()
                # check no of record inserted
                count = cur.rowcount
                print(count, "Record inserted successfully into table")
            # if query is not save show error
            except (Exception, config.psycopg2.Error) as er:
                if(config.conn):
                    print("Failed to insert ", er)
            finally:
                # update jobsUrls table status to True that data of selected
                if (config.conn):
                    # create cursor
                    cur = config.conn.cursor()
                    update_urls_status = """UPDATE public."jobsUrls"
                                        SET "Is_Scraped"=True
                                        WHERE "Job_ID"= %s;"""
                    cur.execute(update_urls_status, (Job_id,))
                    # save data into database
                    config.conn.commit()
                    # close cursor
                    cur.close()
                    print("PostgreSQL connection is closed")
        except (Exception, config.psycopg2.Error) as er:
            print(er)
            if tryCount > 2:
                error = False
            else:
                time.sleep(10)
                error = True
                tryCount += 1
config.conn.close()
browser.quit()
