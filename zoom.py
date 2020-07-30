import scraper
from requests import get
from bs4 import BeautifulSoup as bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re

info = scraper.main()
url = 'https://zoom.us/join'
scraper.driver.get(info["url"])
time.sleep(5)

try:
    WebDriverWait(scraper.driver, 3).until(EC.alert_is_present(),
                                    'Timed out waiting for PA creation ' +
                                    'confirmation popup to appear.')
    scraper.driver.switch_to.alert().accept()
except NoAlertPresentException as e:
    print("no alert")

