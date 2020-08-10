from selenium import webdriver
import PostgresConnection as config  # database connection
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
from bs4 import BeautifulSoup


def get_link(url_link):

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-error')
    options.add_argument('ignore-ssl-errors')
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = dir_path + "/chromedriver"           # chromedriver path
    browser = webdriver.Chrome(dir_path)

    error = True
    while error == True:        # if error accord due blocking it will be repeat
        try:                # check error type
            error = False
            # url of where job links you want to search
            url = url_link
            # open browser and load url
            browser.get(url)
            # wait for full loading of page
            time.sleep(5)
            # Maximize browser
            browser.maximize_window()
            print("loding more itmes")
            itmes = 0
            # load more page by scrolling down
            while itmes != len(browser.find_elements_by_tag_name('li')):  # find no of li tags in page
                # assign value to itmes variable
                itmes = len(browser.find_elements_by_tag_name('li'))
                # scroll to end of page
                browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                actions = ActionChains(browser)
                # calling END key to scroll down
                actions.send_keys(Keys.END)
                actions.perform()
                time.sleep(5)               # wait for loading of page
            # after loading of full jobs load html date into soup variable
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            # filter date of specific class
            jobsData = soup.find(class_='jobs-search__results-list')
            # extract job all link tags
            jobsList = jobsData.find_all(class_='result-card__full-card-link')
            # extract job all ID tags
            jobIdData = jobsData.find_all(
                class_='result-card job-result-card result-card--with-hover-state')
            for i in jobIdData:
                jobsLinks = 'https://de.linkedin.com/jobs/view/' + \
                    str(i['data-id'])  # extract jobs links
                job_id = i['data-id']   # extract job id
                cur = config.conn.cursor()
                try:
                    # save date into database
                    postgres_insert_query = """INSERT INTO public."jobsUrls"(
                    "Urls", "Job_ID")
                    VALUES (%s, %s)
                    ON CONFLICT ("Job_ID")
                    DO NOTHING;
                """
                    record_to_insert = (str(jobsLinks), job_id)
                    cur.execute(postgres_insert_query, record_to_insert)
                    config.conn.commit()
                    count = cur.rowcount
                    print(count, "Record inserted successfully into mobile table")
                except (Exception, config.psycopg2.Error) as error:
                    if(config.conn):
                        print("Failed to insert record into mobile table", error)
                finally:
                    # closing database connection.
                    if (config.conn):
                        cur.close()
        except (Exception, config.psycopg2.Error) as er:
            print(er)
            time.sleep(10)
            error = True
    browser.quit()


# Data Scientist link
link1 = ('https://www.linkedin.com/jobs/search/?f_PP=106967730&f_TP=1%2C2&f_TPR=r604800&geoId=103035651&keywords=data%20scientist&location=Berlin%2C%20Germany&sortBy=DD&redirect=false&position=1&pageNum=0')
get_link(link1)

time.sleep(3)

# Data Analyst link
link2 = ('https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=Berlin%2C%20Deutschland&geoId=103035651&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0&sortBy=DD&f_TP=1%2C2')
get_link(link2)

time.sleep(3)

# Data Engineer link
link3 = ('https://www.linkedin.com/jobs/search?keywords=Data%2BEngineer&location=Berlin%2C%2BGermany&geoId=103035651&trk=public_jobs_jobs-search-bar_search-submit&sortBy=DD&f_TP=1%2C2&redirect=false&position=1&pageNum=0')
get_link(link3)

config.conn.close()
