from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
import os
import pyperclip

# Fill in Miva store domain, Username/Password for login and import file location
STORE_DOMAIN = ""
USERNAME = ""
PASSWORD =""
IMPORT_FILE_LOCATION = ""
#IMPORT_FILE_LOCATION = "/Optimizer_Files/prod-test-import.txt"

def frame_switch(name):
  driver.switch_to.frame(driver.find_element_by_name(name))
  print("switched to frame: " + name)

def waitForAlert():
    try:
        WebDriverWait(driver, 4).until(EC.alert_is_present())
        driver.switch_to.alert.accept()
    except TimeoutException as ex:
        print("Alert wasn't present this time.. continuing..")

PATH = os.path.dirname(os.path.abspath(__file__))
driver = webdriver.Chrome(executable_path= PATH + '/chromedriver.exe')
driver.get(STORE_DOMAIN + "/Merchant5/admin.mvc")

# Not required but ensures you're on the correct web page
#assert "Miva Merchant" in driver.title

dataStr = ""
with open(PATH + IMPORT_FILE_LOCATION, "r") as myfile:
    dataStr += str(myfile.read().splitlines())
dataStr = dataStr.replace("'", "").replace("[","").replace("]","")
pyperclip.copy(dataStr)

user = driver.find_element_by_name("UserName").send_keys(USERNAME)
pw = driver.find_element_by_name("Password").send_keys(PASSWORD)
signInBtn = driver.find_element_by_id('mm9_login_button').click()

# Kicks first user in list until Miva is accesible
while not driver.find_elements_by_id("mm9_screen_header_search_box_search"):
    try:
        kickUser = driver.find_element_by_partial_link_text('Close Session').click()
        closeAlert = driver.find_element_by_partial_link_text('Yes').click()
    except NoSuchElementException:
        print("No need to kick anyone")

driver.implicitly_wait(10)
search = driver.find_element_by_id("mm9_screen_header_search_box_search").send_keys('optimizer')
driver.implicitly_wait(10)
option = driver.find_element_by_xpath('//*[@id="mm9_screen_header_search_box"]/div/div[2]/span[1]/div/div[1]/span/span').click()

waitForAlert()

driver.switch_to.default_content()
importTab = driver.find_element_by_xpath('//*[@id="mm9_screen_actionbar_tablist_content"]/span[5]').click()

frame_switch("Main")

driver.implicitly_wait(10)

while(True):
    try:
        prodsRadio = driver.find_element_by_xpath('//*[@id="mm9_content"]/div[3]/table/tbody/tr[1]/td/fieldset/table/tbody/tr[1]/td[1]/input').click()
        textArea = driver.find_element_by_xpath('//*[@id="mm9_content"]/div[3]/table/tbody/tr[1]/td/fieldset/table/tbody/tr[1]/td[2]/textarea')
        textArea.click()
        textArea.send_keys(Keys.CONTROL, 'v')
        break
    except StaleElementReferenceException as Exception:
        print (Exception)
importBtn = driver.find_element_by_xpath('//*[@id="mm9_content"]/div[3]/table/tbody/tr[2]/td/input').click()

driver.switch_to.default_content()
pagesBtn = driver.find_element_by_xpath('//*[@id="mm9_screen_actionbar_tablist_content"]/span[3]').click()

waitForAlert()

frame_switch("Main")
importBtn2 = driver.find_element_by_xpath('//*[@id="mm9_content"]/div[3]/table/tbody/tr[2]/td/input').click()

#driver.close()