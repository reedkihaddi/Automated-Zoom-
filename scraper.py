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
import time
import re

userProfile = "C:\\Users\\BB\\AppData\\Local\\Google\\Chrome\\User Data\\Default"

options = webdriver.ChromeOptions()
options.add_argument(r"user-data-dir=" + userProfile)
prefs = {"protocol_handler.excluded_schemes.zoommtg": False}
options.add_experimental_option("prefs", prefs)
# options.add_experimental_option("prefs", {
#     "protocol_handler": {"excluded_schemes": {"zoommtg": "false"}}
# })
driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe', options=options)
print("Starting Chrome.")
driver.get("https://web.whatsapp.com/")


def search_message():
    while True:
        for name in driver.find_elements_by_xpath("//div[@class='_210SC']"):
            group_name = name.find_element_by_xpath(
                ".//span[contains(@class, '_3ko75 _5h6Y_ _3Whw5')]")

            if group_name.text == "Group":
                print("Success, found the chat.")
                time.sleep(2)
                name.find_element_by_xpath(
                    ".//div[contains(@class,'_2kHpK')]").click()
                return


def read_message():
    urls = []
    urls_ = []
    call_info = {}
    time.sleep(1)
    # for _ in range(5):
    #     driver.execute_script(
    #         "document.getElementsByClassName('copyable-area')[0].lastChild.scrollBy(0,-500)")

    chat = driver.find_elements(By.XPATH,
                                '//*[contains(concat( " ", @class, " " ), concat( " ", "copyable-text", " " ))]')

    chat.reverse()

    print("Searching for Zoom link.")
    for chat_message in chat:
        urls.append(chat_message.text)

    for i in range(0, len(urls)):
        # print(urlparse(i))
        urls_.append(urlparse(urls[i]))

        meeting_id = re.search("(?<=id:).*", urls[i], flags=re.IGNORECASE)
        password = re.search("(?<=password:).*", urls[i], flags=re.IGNORECASE)
        if meeting_id:
            call_info["password"] = password.group().strip()
            call_info["meeting_id"] = meeting_id.group().strip()
            link = urlparse(urls[i])
            if link.scheme == "https" and "zoom" in link.netloc:
                # print("CURRENT LINK: \n"+link.geturl()+"CURRENT TEXT: \n"+i)
                print("Found the link.")
                call_info["url"] = link.geturl()
                break

        else:
            link = urlparse(urls[i])
            if link.scheme == "https" and "zoom" in link.netloc:
                print("Found the link.")
                call_info["url"] = link.geturl()
                try:
                    meeting_id = re.search("(?<=id:).*", urls[i + 1], flags=re.IGNORECASE)
                    password = re.search("(?<=password:).*", urls[i + 1], flags=re.IGNORECASE)

                    if meeting_id:
                        if call_info["url"] in urls[i + 1]:
                            call_info["password"] = password.group().strip()
                            call_info["meeting_id"] = meeting_id.group().strip()
                except NameError:
                    pass
                break

    for j in urls_:
        if j.scheme == "https" and "zoom" in j.netloc:
            call_info["url"] = j.geturl()
            break

    return call_info


def main():
    search_message()
    return read_message()


