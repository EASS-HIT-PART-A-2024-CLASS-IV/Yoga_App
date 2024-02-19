from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import argparse
import json

class_details_list = []
data_filename = "/app/yoga_data.json"
print(f"File {data_filename} created successfully!")

url="https://www-nylovesyoga-com.filesusr.com/html/e57bb2_3226c108f719e47cbc6dfdbad3222264.html"
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.binary_location = "/usr/bin/chromium"
webdriver_path = "/usr/bin/chromedriver"

options.add_argument(f"executable_path={webdriver_path}")
driver = webdriver.Chrome(options=options)
driver.get(url)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "bw-session")))

html_content = driver.page_source

soup = BeautifulSoup(html_content, 'html.parser')

day_elements = soup.find_all(class_="bw-widget__day")
for day_element in day_elements:
    day = day_element.find(class_="bw-widget__date").text.strip()

    class_elements = day_element.find_all(class_="bw-session")
    for class_element in class_elements:
        class_name = class_element.find(
            class_="bw-session__name").text.strip()
        start_time = class_element.find(class_="hc_starttime").text.strip()
        end_time = class_element.find(class_="hc_endtime").text.strip()

        class_details_list.append({
            "classname": class_name,
            "day": day,
            "start_time": start_time,
            "end_time": end_time
        })
        print(class_details_list)
        with open(data_filename, "w") as json_file:
            json.dump(class_details_list, json_file)
driver.quit()

