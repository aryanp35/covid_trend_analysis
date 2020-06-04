from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import linecache
import sys
import os
import glob
import shutil
import datetime as DT
import time


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('window-size=2560,1440')
chrome_path = "/home/starc/Desktop/chromedriver_linux64/chromedriver"
driver = webdriver.Chrome(chrome_path, options=options)
driver.get("https://app.talkwalker.com/app/login")

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print ("EXCEPTION IN ({}, LINE {} \"{}\"): {}".format(filename, lineno, line.strip(), exc_obj))


# change credentials here for your email and password
def loginManeuver():
    try:
        driver.find_element_by_xpath("/html/body/div[2]/div/div/login-page/div/form/div[2]/div[1]/input").send_keys("wefder02@gmail.com")
        driver.find_element_by_xpath("/html/body/div[2]/div/div/login-page/div/form/div[3]/div[1]/input").send_keys("asdf1234")
        driver.find_element_by_xpath("/html/body/div[2]/div/div/login-page/div/form/div[4]/tw-progress-button").click()
    except Exception as e:
        print(e)


# change renaming convention here as you need
def renameDownload(searchText, downloadText):
    direct_path = '/home/starc/Downloads/'
    os.chdir(direct_path)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    latest_file = files[-1]
    today = DT.date.today()
    week_ago = today - DT.timedelta(days=7)
    filepath = direct_path + latest_file
    newfilepath = direct_path+searchText+"_Demographics-"+downloadText+"_"+str(today)+"to"+str(week_ago)+".csv"
    os.rename(filepath, newfilepath)

driver.implicitly_wait(40)

loginManeuver()


driver.implicitly_wait(40)



## For Saved Search and Demographics page
try :
    #moves cursor to a saved search
    ActionChains(driver).move_to_element(driver.find_element_by_xpath("/html/body/div[2]/div/div/free-search-page/div/div[1]/div/div[2]/div/div/div/div[1]/ul/li[2]/span[1]")).perform()
    
    #clicks on the saved search
    searchText = driver.find_element_by_xpath("/html/body/div[2]/div/div/free-search-page/div/div[1]/div/div[2]/div/div/div/div[1]/ul/li[2]/span[1]").text
    driver.find_element_by_xpath("/html/body/div[2]/div/div/free-search-page/div/div[1]/div/div[2]/div/div/div/div[1]/ul/li[2]/span[1]").click()
    driver.implicitly_wait(15)
    
    #moves cursor then clicks demographics tab
    ActionChains(driver).move_to_element(driver.find_element_by_xpath("/html/body/div[2]/div/div/free-search-page/div/div[1]/div[1]/div/div[4]/div/div/i")).perform()
    driver.find_element_by_xpath("/html/body/div[2]/div/div/free-search-page/div/div[1]/div[1]/div/div[4]/div/div/i").click()
    
    driver.implicitly_wait(6)
except:
    PrintException()
try:  
    # moves cursor then clicks on the 3 dots to the graph
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder[1]/div/div/tw-widget/div/tw-widget-body/div")))
    ActionChains(driver).move_to_element(driver.find_element_by_xpath("/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder[1]/div/div/tw-widget/div/tw-widget-body/div")).perform()
    driver.find_element_by_xpath("/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder[1]/div/div/tw-widget/div/div/button").click()
    
    driver.implicitly_wait(2)

    # moves to export option
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "icon2-tw-export")))
    ActionChains(driver).move_to_element(driver.find_element_by_class_name("icon2-tw-export ")).perform()
    
    driver.implicitly_wait(3)

    # clicks on csv option
    driver.find_element_by_class_name("icon-tw-csv").click()
    driver.implicitly_wait(10)
    
    #downloads the .csv file
    downloadLink=driver.find_element_by_link_text("here").get_attribute('href')
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(downloadLink)
    driver.close()
    time.sleep(2)
    
    renameDownload(searchText, "Gender")

    #switches back to the original tab
    driver.switch_to.window(driver.window_handles[0])
    print("successfully clicked")
    driver.implicitly_wait(5)
    if driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/i"):
        driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/i").click()
    
    driver.implicitly_wait(10)
    
    driver.implicitly_wait(5)

    # closes the download prompt
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/ul/li/div[2]/i")))
    ActionChains(driver).move_to_element(driver.find_element_by_xpath("/html/body/div[5]/div/ul/li/div[2]/i")).perform()
    driver.find_element_by_xpath("/html/body/div[5]/div/ul/li/div[2]/i").click()

except:
    PrintException()

## Age export
try:
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/ul/li/div[2]/i")))
        ActionChains(driver).move_to_element(driver.find_element_by_xpath("/html/body/div[5]/div/ul/li/div[2]/i")).perform()
        driver.find_element_by_xpath("/html/body/div[5]/div/ul/li/div[2]/i").click()
    except:
        PrintException()
    driver.implicitly_wait(3)

    # moves cursor then clicks on the 3 dots to the graph
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder[2]/div/div/tw-widget/div/tw-widget-body/div/div/div[2]/div/span/canvas")))
    ActionChains(driver).move_to_element(driver.find_element_by_xpath("/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder[2]/div/div/tw-widget/div/tw-widget-body/div/div/div[2]/div/span/canvas")).perform()
    driver.find_element_by_xpath("/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder[2]/div/div/tw-widget/div/div/button/i").click()
    driver.implicitly_wait(3)

    # moves to export option
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "icon2-tw-export")))
    ActionChains(driver).move_to_element(driver.find_element_by_class_name("icon2-tw-export ")).perform()
    
    driver.implicitly_wait(3)

    # clicks on csv option
    driver.find_element_by_class_name("icon-tw-csv").click()
    driver.implicitly_wait(10)
    
    #downloads the .csv file
    downloadLink=driver.find_element_by_link_text("here").get_attribute('href')
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(downloadLink)
    driver.close()
    
    time.sleep(2)


    renameDownload(searchText, "Age")

    #switches back to the original tab
    driver.switch_to.window(driver.window_handles[0])
    print("successfully clicked")
    driver.implicitly_wait(5)
    
    driver.implicitly_wait(10)
    
    
    driver.implicitly_wait(3)

    #close the download prompt
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/ul/li/div[2]/i")))
    ActionChains(driver).move_to_element(driver.find_element_by_xpath("/html/body/div[5]/div/ul/li/div[2]/i")).perform()
    driver.find_element_by_xpath("/html/body/div[5]/div/ul/li/div[2]/i").click()
except:
    PrintException()


## Top Languages
try:
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/ul/li/div[2]/i")))
        ActionChains(driver).move_to_element(driver.find_element_by_xpath("/html/body/div[5]/div/ul/li/div[2]/i")).perform()
        driver.find_element_by_xpath("/html/body/div[5]/div/ul/li/div[2]/i").click()
    except:
        PrintException()
    driver.implicitly_wait(3)

    # moves cursor then clicks on the 3 dots to the graph
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder[3]/div/div/tw-widget/div/tw-widget-body/div/div/div[2]/div")))
    ActionChains(driver).move_to_element(driver.find_element_by_xpath("/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder[3]/div/div/tw-widget/div/tw-widget-body/div/div/div[2]/div")).perform()
    driver.find_element_by_xpath("/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder[3]/div/div/tw-widget/div/div/button").click()
    driver.implicitly_wait(3)

    # moves to export option
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "icon2-tw-export")))
    ActionChains(driver).move_to_element(driver.find_element_by_class_name("icon2-tw-export ")).perform()
    
    driver.implicitly_wait(3)

    # clicks on csv option
    driver.find_element_by_class_name("icon-tw-csv").click()
    driver.implicitly_wait(10)
    
    #downloads the .csv file
    downloadLink=driver.find_element_by_link_text("here").get_attribute('href')
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(downloadLink)
    driver.close()

    time.sleep(2)

    renameDownload(searchText, "TopLanguages")

    #switches back to the original tab
    driver.switch_to.window(driver.window_handles[0])
    print("successfully clicked")
    driver.implicitly_wait(5)
    
    driver.implicitly_wait(10)
    

    driver.implicitly_wait(3)

    #close the download prompt
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/ul/li/div[2]/i")))
    ActionChains(driver).move_to_element(driver.find_element_by_xpath("/html/body/div[5]/div/ul/li/div[2]/i")).perform()
    driver.find_element_by_xpath("/html/body/div[5]/div/ul/li/div[2]/i").click()
except:
    PrintException()

## Top Interests
try:
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/ul/li/div[2]/i")))
        ActionChains(driver).move_to_element(driver.find_element_by_xpath("/html/body/div[5]/div/ul/li/div[2]/i")).perform()
        driver.find_element_by_xpath("/html/body/div[5]/div/ul/li/div[2]/i").click()
    except:
        PrintException()
    driver.implicitly_wait(3)

    # moves cursor then clicks on the 3 dots to the graph
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder[4]/div/div/tw-widget/div/tw-widget-body/div/div/div[2]/div")))
    ActionChains(driver).move_to_element(driver.find_element_by_xpath("/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder[4]/div/div/tw-widget/div/tw-widget-body/div/div/div[2]/div")).perform()
    driver.find_element_by_xpath("/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder[4]/div/div/tw-widget/div/div/button").click()
    driver.implicitly_wait(3)

    # moves to export option
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "icon2-tw-export")))
    ActionChains(driver).move_to_element(driver.find_element_by_class_name("icon2-tw-export ")).perform()
    
    driver.implicitly_wait(3)

    # clicks on csv option
    driver.find_element_by_class_name("icon-tw-csv").click()
    driver.implicitly_wait(10)
    
    #downloads the .csv file
    downloadLink=driver.find_element_by_link_text("here").get_attribute('href')
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(downloadLink)
    driver.close()
    
    time.sleep(2)
    

    renameDownload(searchText, "TopInterests")

    #switches back to the original tab
    driver.switch_to.window(driver.window_handles[0])
    print("successfully clicked")
    driver.implicitly_wait(5)
    
    # driver.find_element_by_xpath("/html/body/div[5]/div/ul/li/div[2]/i").click()
    driver.implicitly_wait(10)
    

    driver.implicitly_wait(3)

    #close the download prompt
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/ul/li/div[2]/i")))
    ActionChains(driver).move_to_element(driver.find_element_by_xpath("/html/body/div[5]/div/ul/li/div[2]/i")).perform()
    driver.find_element_by_xpath("/html/body/div[5]/div/ul/li/div[2]/i").click()
except:
    PrintException()


## Top Occupations
try:
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/ul/li/div[2]/i")))
        ActionChains(driver).move_to_element(driver.find_element_by_xpath("/html/body/div[5]/div/ul/li/div[2]/i")).perform()
        driver.find_element_by_xpath("/html/body/div[5]/div/ul/li/div[2]/i").click()
    except:
        PrintException()
    driver.implicitly_wait(3)
    # moves cursor then clicks on the 3 dots to the graph
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder[5]/div/div/tw-widget/div/tw-widget-body/div/div/div[2]/div")))
    ActionChains(driver).move_to_element(driver.find_element_by_xpath("/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder[5]/div/div/tw-widget/div/tw-widget-body/div/div/div[2]/div")).perform()
    driver.find_element_by_xpath("/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder[5]/div/div/tw-widget/div/div/button").click()
    driver.implicitly_wait(3)
    # moves to export option
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "icon2-tw-export")))
    ActionChains(driver).move_to_element(driver.find_element_by_class_name("icon2-tw-export ")).perform()
    
    driver.implicitly_wait(3)

    # clicks on csv option
    driver.find_element_by_class_name("icon-tw-csv").click()
    driver.implicitly_wait(10)
    
    #downloads the .csv file
    downloadLink=driver.find_element_by_link_text("here").get_attribute('href')
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(downloadLink)
    driver.close()
    
    time.sleep(2)

    
    renameDownload(searchText, "TopOccupations")

    #switches back to the original tab
    driver.switch_to.window(driver.window_handles[0])
    print("successfully clicked")
    driver.implicitly_wait(5)
    
    driver.implicitly_wait(10)
    
    
    driver.implicitly_wait(3)

    #close the download prompt
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/ul/li/div[2]/i")))
    ActionChains(driver).move_to_element(driver.find_element_by_xpath("/html/body/div[5]/div/ul/li/div[2]/i")).perform()
    driver.find_element_by_xpath("/html/body/div[5]/div/ul/li/div[2]/i").click()
except:
    PrintException()
