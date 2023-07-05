from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import time 
import pickle
import requests

course_watchlist = ["le-eecs-3221"]
trigger_manual_2fa = True

driver = webdriver.Safari()

def write_cookie():
    with open("cookies.pickle", "wb") as file:
        pickle.dump(driver.get_cookies(), file)

def load_cookie():
    with open("cookies.pickle", 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        # if cookies:
        #     print("in if cookies")
        #     trigger_manual_2fa = False

        for cookie in cookies:
            driver.add_cookie(cookie)


# load_cookie()



time.sleep(2)
driver.get("https://schedulebuilder.yorku.ca/vsb/")
time.sleep(2)


#fill username
username = driver.find_element(By.XPATH, "//*[@id='mli']")
username.send_keys('mickeyb')
time.sleep(2)

#fill password
password = driver.find_element(By.XPATH, "//*[@id='password']")
password.send_keys('82tx94c2?')

time.sleep(2)
driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[1]/form/div[2]/div[2]/p[2]/input").click()
time.sleep(2)

WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@id='duo_iframe']")))
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login-form"]/div[2]/div/label/input'))).click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Send Me a Push']"))).click()
cookies = driver.get_cookies()
# print(cookies)
# write_cookie()


driver.quit()
# //*[@id="auth_methods"]/fieldset[1]/div[1]/button
# xpath for RemME: //*[@id="login-form"]/div[2]/div/label/input
