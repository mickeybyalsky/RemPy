from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
import pickle, time, os
import functions

load_dotenv()

send_sms_message = False
send_email_message = False

def erase_cookie():
    open('cookies.pickle', 'w').close()

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

def add_course(cat):
    #add button
    driver.find_element(By.NAME, '5.1.27.1.23').click()
    time.sleep(3)
    course_box = driver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/span[2]/input[1]')

    course_box.send_keys(cat)
    time.sleep(2)
    driver.find_element(By.NAME, '5.1.27.7.9').click()
    time.sleep(2)
    
    #IF CAT CODE IS <6 CHARS
    try:
        result = driver.find_element(By.CLASS_NAME, 'alert')
        print(result.text)
        driver.find_element(By.XPATH,'/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table[3]/tbody/tr/td/span/a').click()
    except NoSuchElementException:

        #add button
        driver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table[2]/tbody/tr[7]/td[2]/input[1]').click()
        
        result = driver.find_elements(By.XPATH, "//span[@class='bodytext']/font/b")
    
        res = []
        for text in result:
            res.append(text.text)
        string = ' '.join(res)

        #IF COURSE WAS ADDDED
        if "The course has been successfully added." in string:
            curr_course = driver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table[2]/tbody/tr[4]/td[2]/span').text
            cur_course = curr_course[3:12] + " "+ curr_course[21:22]
            #print(f"The course {cur_course} has been successfully added.\nTHIS ACTION HAS FINANCIAL IMPACT TO YOUR FINANCIAL ACCOUNT\nVISIT https://sfs.yorku.ca FOR UPDATED TUTION INFORMATION.")
            body=f"\nThe course {cur_course} has been successfully added.\nTHIS ACTION HAS FINANCIAL IMPACT TO YOUR STUDENT FINANCIAL ACCOUNT.VISIT HTTPS://SFS.YORKU.CA FOR UPDATED TUTION INFORMATION."
            
            if send_sms_message: functions.send_sms(body)
            if send_email_message: functions.send_email(body)

            time.sleep(3)
            driver.find_element(By.NAME, '5.1.27.23.9').click()

        #IF COURSE WAS NOT ADDED BECAUSE IT IS FULL
        elif "The course you are trying to add is full." in string:
            time.sleep(3)
            curr_course = driver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table[2]/tbody/tr[5]/td[2]/span').text
            cur_course = curr_course[3:12] + " "+ curr_course[21:22]
            print(f"The course {cur_course} has not been added. The course you are trying to add is full.")
            time.sleep(3)
            driver.find_element(By.NAME, '5.1.27.27.11').click()

        #IF COURSE WAS NOT ADDED BECAUSE IT IS RESERVED
        elif "The spaces in this course are reserved." in string:
            curr_course = driver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table[2]/tbody/tr[5]/td[2]/span').text
            cur_course = curr_course[3:12] + " "+ curr_course[21:22]
            print(f"The course {cur_course} has not been added. The spaces in this course are reserved.")
            time.sleep(3)
            driver.find_element(By.NAME, '5.1.27.27.11').click()

        else:
            print(string)

def transfer_course(cat):
    #transfer button
    driver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table[4]/tbody/tr[1]/td[3]/div/input').click()
    time.sleep(3)
    
    course_box = driver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/input[1]')
    course_box.send_keys(cat)
    time.sleep(2)
    driver.find_element(By.NAME, '5.1.27.7.9').click() # "Transfer Course" button
    time.sleep(2)
    
        # The catalogue number for the course you wish to transfer does not match the existing course. Please try again. 
    try:
        result = driver.find_element(By.CLASS_NAME, 'alert')
        print(result.text)
        time.sleep(3)
        driver.find_element(By.XPATH,'/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table[4]/tbody/tr/td/span/a').click()
        
    except NoSuchElementException:
        time.sleep(3)
        driver.find_element(By.NAME, '5.1.27.11.11').click() #Please confirm that you want to: Transfer to: YES
        
        result = driver.find_elements(By.XPATH, "//span[@class='bodytext']/font/b")

        res = []
        for text in result:
            res.append(text.text)
        string = ' '.join(res)

        # The course has been successfully transferred.
        if "The course has been successfully transferred." in string: 
            curr_course = driver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table[2]/tbody/tr[4]/td[2]/span').text       
            cur_course = curr_course[3:12] + " "+ curr_course[21:22]
            
            body=f"\nYou have successfully been transferred into {cur_course}.\nTHIS ACTION HAS FINANCIAL IMPACT TO YOUR STUDENT FINANCIAL ACCOUNT. VISIT HTTPS://SFS.YORKU.CA FOR UPDATED TUTION INFORMATION.",
            
            if send_sms_message: functions.send_sms(body)
            if send_email_message: functions.send_email(body)

            time.sleep(3)
            driver.find_element(By.NAME, '5.1.27.19.9').click() #continue button

        #The course has not been transfered. The spaces in this course are reserved.
        elif "The spaces in this course are reserved." in string:
            curr_course = driver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table[2]/tbody/tr[5]/td[2]/span').text       
            cur_course = curr_course[3:12] + " "+ curr_course[21:22]
            print(f"The course {cur_course} has not been transfered to.\nThe spaces in this course are reserved.")
            time.sleep(3)
            driver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table[2]/tbody/tr[8]/td[2]/input').click() #continue button 
        
        # The course has not been transfered.
        # The course you are trying to add is full.
        elif "The course you are trying to add is full." in string: 
            curr_course = driver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table[2]/tbody/tr[5]/td[2]/span').text       
            cur_course = curr_course[3:12] + " "+ curr_course[21:22]
            print(f"The course {cur_course} has not been transfered to - The course is full.")
            time.sleep(3)
            driver.find_element(By.NAME, '5.1.27.23.11').click()
        else:
            print(string)
        #print result

driver = webdriver.Firefox(executable_path="/Users/mickeybyalsky/Downloads/geckodriver")
watchlist = [["G84J01", 'A'], ["X44V01",'A'], ["F46T02",'A'], ["V21Y01",'A'], ["S81Q02", 'T'], ["H06X02", 'T'], ["C27P04", 'T'] ]
''' 
    X44V01 - EECS 3221 A - What I actually want
    G84J01 - MATH 1014 A - An example of a successful add.
    F46T02 - EECS 3101 A - An example of a full course.
    V21Y01 - EECS 2911 M - An example of a reserved course.

    TRANSFER SECTIONS Successfully
        C27P02 -> C27P03 or C27P04 - EECS 1022
    TRANSFER TO FULL SECTION
        1015 A (N59W02) to 1015 B (H06X02)
    TRANSFER TO RESERVED SECTION
        3101 M (X87W02) TO 3101 Z (S81Q02)
'''

#load_cookie()
driver.set_window_size(1200, 1000)

driver.get("https://wrem.sis.yorku.ca/Apps/WebObjects/REM.woa/wa/DirectAction/rem")

#fill username
username = driver.find_element(By.XPATH, "//*[@id='mli']")
username.send_keys(os.getenv("PPY_USERNAME"))
time.sleep(3)

#fill password
password = driver.find_element(By.XPATH, "//*[@id='password']")
password.send_keys(os.getenv("PPY_PASSWORD"))
time.sleep(3)

#click on submit button
driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[1]/form/div[2]/div[2]/p[2]/input").click()
time.sleep(3)

#duo 2fa
WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@id='duo_iframe']")))
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login-form"]/div[2]/div/label/input'))).click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Send Me a Push']"))).click()
time.sleep(10)

#write_cookie()

driver.get("https://wrem.sis.yorku.ca/Apps/WebObjects/REM.woa/wa/DirectAction/rem")

select_element = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.NAME, "5.5.1.27.1.11.0")))

# Create a Select object
select = Select(select_element)
select.select_by_value("3")

time.sleep(3)

driver.find_element(By.XPATH, '/html/body/form/div[1]/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td[2]/input').click()
time.sleep(3)
for entry in watchlist:
    cat, action = entry
    if action == 'A': add_course(cat)
    elif action == 'T': transfer_course(cat)

    time.sleep(4)
driver.quit()