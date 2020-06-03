from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.actions.interaction import KEY
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import date, timedelta
import os, glob, time

driver = None

to = date.today()
frm = to - timedelta(days = 6)

### Grabs the latest file from your Downloads directory to rename
def last_file():
    time.sleep(5)
    list_of_files = glob.glob('Path to your Downloads folder/*')  # '/*' needs to be appended to search for all files 
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

### Clicks on the link to download the file
def file_download():
    anchor = EC.presence_of_element_located((By.LINK_TEXT, 'here'))
    WebDriverWait(driver, 120).until(anchor)
    href = driver.find_element_by_link_text('here')
    driver.get(href.get_attribute('href'))

### Closes the pop-up after successful download
def close_pop_up():
    close = WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.CLASS_NAME, 'success')))
    WebDriverWait(close, 120).until(EC.element_to_be_clickable((By.CLASS_NAME, 'icon-tw-cross'))).click()

### Clicks on the XLS button
def xls_click():
    xls = WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.CLASS_NAME, 'icon-tw-xls')))
    ActionChains(driver).move_to_element(xls).perform()
    WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.CLASS_NAME, 'icon-tw-xls'))).click() 

### Hovers on the export sub-menu option
def hover_on_export():
    export = WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="export-share-menu"]/ul/li/menuitem')))
    driver.execute_script("arguments[0].scrollIntoView();", export)
    ActionChains(driver).move_to_element(export).perform()

### Changes the file name after download
def change_file_name(file_name, new_name):
    src = last_file()
    dst = 'Path to your Downloads folder'+file_name+'_'+frm.strftime('%d-%m-%Y')+'_'+'to'+'_'+to.strftime('%d-%m-%Y')+'_'+new_name+'.xls' 
    os.rename(src,dst)

### Runs the above functions from hovering on export to closing the pop-up
def run_all():
    hover_on_export()
    xls_click()
    file_download()
    close_pop_up()


try:
    # Opens website app.talkwalker.com
    driver = webdriver.Chrome(r"../chromedriver.exe")
    driver.maximize_window()
    driver.get("https://app.talkwalker.com/app/login")
    
    # Waits for the page to load
    element_present = EC.presence_of_element_located((By.NAME, 'email_sign_in'))
    WebDriverWait(driver, 120).until(element_present)
    
    # Login using your email and password
    e = driver.find_element_by_name('email_sign_in')
    e.send_keys('wefder02@gmail.com')
    e = driver.find_element_by_name('password_sign_in')
    e.send_keys('asdf1234')
    e = driver.find_element_by_tag_name('button')
    e.click()
    
    # Waits for the page to load
    element_present = EC.presence_of_element_located((By.ID, 'search_bar'))
    WebDriverWait(driver, 120).until(element_present)
    
    saved_items = driver.find_elements_by_class_name('saved-search-item')
    item = saved_items[0]
    
    name = WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="quicksearch-saved"]/ul/li[2]/span[1]')))
    file_name = name.text
    
    ### Clicks on first saved search item
    WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.CLASS_NAME, 'saved-search-item')))
    item.click()
    
    element_present = EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder[2]/div/div/tw-widget/div/div/button'))
    WebDriverWait(driver, 120).until(element_present)  

    ### Zooming out for screenshot of first page
    time.sleep(5)
    driver.execute_script("document.body.style.zoom='60%'")
    driver.save_screenshot('screen.png')
    driver.execute_script("document.body.style.zoom='100%'")
    
    
    ### MENTIONS OVER TIME
    heading = driver.find_element_by_xpath('/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder[2]/div/div/tw-widget/div/tw-widget-body/div/div/div[1]/div/widget-header/div/div[1]/h5')
    hover = ActionChains(driver).move_to_element(heading)
    hover.perform()

    icon = driver.find_element_by_xpath('/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder[2]/div/div/tw-widget/div/div/button')
    icon.click()
    
    run_all()
   
    change_file_name(file_name, 'mentions_over_time')

    
    ### TOP THEMES
    driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
    cloud = driver.find_element_by_class_name('icon2-tw-themecloud')
    cloud.click()
    element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="page_content"]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder/div/div/tw-widget/div/tw-widget-body/div/div/div[1]/div/tw-widget-menus-top/div/widget-topic-menu-select/div/div/div/div[2]/span'))
    WebDriverWait(driver, 120).until(element_present)        
    heading = driver.find_element_by_xpath('//*[@id="page_content"]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder/div/div/tw-widget/div/tw-widget-body/div/div/div[1]/div/tw-widget-menus-top/div/widget-topic-menu-select/div/div/div/div[2]/span')
    hover = ActionChains(driver).move_to_element(heading)
    hover.perform()
    
    # icon = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder/div/div/tw-widget/div/div/button')))
    # ActionChains(driver).move_to_element(icon).click().perform()
    driver.find_element_by_xpath('/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder/div/div/tw-widget/div/div/button').click()
    # time.sleep(3)
    # export = driver.find_element_by_xpath('//*[@id="export-share-menu"]/ul/li/menuitem/span')
    run_all()

    change_file_name(file_name, 'top_themes')
    
    
    ### TOP HASHTAGS
    driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
    # theme = WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder/div/div/tw-widget/div/tw-widget-body/div/div/div[1]/div/tw-widget-menus-top/div/widget-topic-menu-select/div/div/div/div[1]')))
    hashtag = driver.find_element_by_xpath('//*[@id="page_content"]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder/div/div/tw-widget/div/tw-widget-body/div/div/div[1]/div/tw-widget-menus-top/div/widget-topic-menu-select/div/div/div/div[2]/span')
    # driver.execute_script("arguments[0].scrollIntoView();", theme)
    hashtag.click()        

    ActionChains(driver).move_to_element(hashtag).perform()
    time.sleep(5)
    # driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
    WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder/div/div/tw-widget/div/div/button'))).click()

    run_all()
       
    change_file_name(file_name, 'top_hashtags')        
    
    
    ### INFLUENCERS
    driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
    people = driver.find_element_by_class_name('icon2-tw-qs-people')
    people.click()        
    
    posts = WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="page_content"]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder[1]/div/div/tw-widget/div/tw-widget-body/div/div/div[2]/div/div/table/thead/tr/th[4]/div')))
    ActionChains(driver).move_to_element(posts).perform()        
    
    WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder[1]/div/div/tw-widget/div/div/button'))).click()
    
    run_all()
 
    change_file_name(file_name, 'influencers')

    
    ### RESULTS
    driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
    results = driver.find_element_by_class_name('icon2-tw-results-list')
    results.click()      
    
    WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="page_content"]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder/div/div/tw-widget/div/tw-widget-body/div/div/div[2]/div/div/div/div/div[1]/div[1]/article/div[1]/div[2]/h5/a/span')))
    
    count = 0
    # last_height = driver.execute_script("return document.body.scrollHeight")
    while count<=10:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        count += 1
    
    driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
    ActionChains(driver).move_to_element(driver.find_element_by_xpath('//*[@id="page_content"]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder/div/div/tw-widget/div/tw-widget-body/div/div/div[1]/div/widget-header/div/div[1]/h5')).perform()

    WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/free-search-page/div/div[1]/div[2]/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder/div/div/tw-widget/div/div/button'))).click()
    
    run_all()

    change_file_name(file_name, 'top_results')
                
except TimeoutException:
    print("Timed out waiting for the page to load")
finally:
    print('Successful')
    if driver is not None:
        driver.close()
    
