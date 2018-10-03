from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def frame_switch(name):
  driver.switch_to.frame(driver.find_element_by_name(name))

def waitForAlert():
    WebDriverWait(driver, 25).until(EC.alert_is_present())
    driver.switch_to.alert.accept()

# Fill in Miva store domain, Username/Password for login and import file location
STORE_DOMAIN = ""
USERNAME = ""
PASSWORD = ""
IMPORT_FILE_LOCATION = ""

driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get(STORE_DOMAIN + "/Merchant5/admin.mvc")
assert "Miva Merchant" in driver.title

data = []
with open(IMPORT_FILE_LOCATION, "r") as myfile:
    data += myfile.readlines()

user = driver.find_element_by_name("UserName").send_keys(USERNAME)
pw = driver.find_element_by_name("Password").send_keys(PASSWORD)
signInBtn = driver.find_element_by_id('mm9_login_button').click()

search = driver.find_element_by_id("mm9_screen_header_search_box_search").send_keys('optimizer')
driver.implicitly_wait(10)
option = driver.find_element_by_xpath('//*[@id="mm9_screen_header_search_box"]/div/div[2]/span[1]/div/div[1]/span/span').click()

waitForAlert()

driver.switch_to.default_content()
importTab = driver.find_element_by_xpath('//*[@id="mm9_screen_actionbar_tablist_content"]/span[5]').click()

frame_switch("Main")
prodsRadio = driver.find_element_by_xpath('//*[@id="mm9_content"]/div[3]/table/tbody/tr[1]/td/fieldset/table/tbody/tr[1]/td[1]/input')
prodsRadio.click()
textArea = driver.find_element_by_xpath('//*[@id="mm9_content"]/div[3]/table/tbody/tr[1]/td/fieldset/table/tbody/tr[1]/td[2]/textarea')
textArea.click()
textArea.send_keys(data)
importBtn = driver.find_element_by_xpath('//*[@id="mm9_content"]/div[3]/table/tbody/tr[2]/td/input').click()

driver.switch_to.default_content()
pagesBtn = driver.find_element_by_xpath('//*[@id="mm9_screen_actionbar_tablist_content"]/span[3]').click()

waitForAlert()

frame_switch("Main")
importBtn2 = driver.find_element_by_xpath('//*[@id="mm9_content"]/div[3]/table/tbody/tr[2]/td/input').click()

#driver.close()