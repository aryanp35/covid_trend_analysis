#!/usr/bin/env python
# coding: utf-8

# In[14]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import urllib.request
import os
import shutil
import time


# In[53]:


def excel_extract(i):
    action = ActionChains(browser)
    element=browser.find_elements_by_class_name("widget-head")
    action.move_to_element(element[i]).perform()
    time.sleep(2)
    element=browser.find_elements_by_id("widget-button-target")
    element[i].click()
    time.sleep(2)
    wait = WebDriverWait(browser, 10)
    browser.execute_script("window.scrollTo(0, 400)") 
    time.sleep(2)
    element=browser.find_element_by_class_name("icon2-tw-export")
    element.click()
    element=browser.find_element_by_class_name("icon-tw-xls")
    element.click()
    time.sleep(2)
    element=browser.find_element_by_link_text("here").get_attribute('href')
    browser.get(element)

def refresh_page():
    browser.execute_script("window.scrollTo(0, 0)") 
    browser.refresh()
    time.sleep(5)
    element=browser.find_element_by_class_name("saved-search-item")
    element.click()

def sub_topic(i):
    action = ActionChains(browser)
    element=browser.find_elements_by_class_name("identity-icon-component")
    action.move_to_element(element[i]).perform()
    element[i].click()
    
def scrolling_down():
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, 0)") 

def tiny_file_rename(newname, folder_of_download,folder_of_deposit):
    filename = max([f for f in os.listdir(folder_of_download)], key=lambda xa :   os.path.getctime(os.path.join(folder_of_download,xa)))
    if '.part' in filename:
        time.sleep(1)
        os.rename(os.path.join(folder_of_download, filename), os.path.join(folder_of_deposit, newname))
    else:
        os.rename(os.path.join(folder_of_download, filename),os.path.join(folder_of_deposit,newname))

def log_in(passwordStr,usernameStr):
    # Step 1) Open chrome 
    browser = webdriver.Chrome()
    # Step 2) Navigate to Talkwalker
    browser.get("https://app.talkwalker.com/app/login")
    # Step 3) Search & Enter the Email or Phone field & Enter Password
    browser.set_window_size(100000, 100000)
    browser.implicitly_wait(15)
    element = browser.find_element_by_xpath("//input[@name='email_sign_in']")
    element.send_keys(usernameStr)
    element = browser.find_element_by_name('password_sign_in')
    element.send_keys(passwordStr)
    # Step 4) Click Login
    element.send_keys(Keys.RETURN)
    time.sleep(2)


# In[52]:


# Step 1) Open chrome 
browser = webdriver.Chrome()
# Step 2) Navigate to Talkwalker
browser.get("https://app.talkwalker.com/app/login")
# Step 3) Search & Enter the Email or Phone field & Enter Password
browser.set_window_size(100000, 100000)
browser.implicitly_wait(15)
element = browser.find_element_by_xpath("//input[@name='email_sign_in']")
element.send_keys(usernameStr)
element = browser.find_element_by_name('password_sign_in')
element.send_keys(passwordStr)
# Step 4) Click Login
element.send_keys(Keys.RETURN)
time.sleep(2)

#selecting saved item
element=browser.find_element_by_class_name("saved-search-item")
element.click()
time.sleep(2)


excel_extract(1)
name=browser.find_element_by_xpath("//*[@id='page_content']/div[2]/div/div/div/div[2]/div[1]/div/div[1]").text
namelat=name+ ' mention_over_time' + ' hello'+'.xls'
time.sleep(2)
tiny_file_rename(namelat,'D:\Downloads','D:\Covid_talkwalker')
refresh_page()

#themes
sub_topic(1)
excel_extract(0)
namelat=name+ ' theme' + ' hello'+'.xls'
time.sleep(2)
tiny_file_rename(namelat,'D:\Downloads','D:\Covid_talkwalker')
browser.execute_script("window.scrollTo(0, 0)") 
time.sleep(5)

#hash_tags
element=browser.find_element_by_xpath("//*[@id='page_content']/div[4]/div/div/div/tw-grid/div/div[2]/tw-widget-placeholder/div/div/tw-widget/div/tw-widget-body/div/div/div[1]/div/tw-widget-menus-top/div/widget-topic-menu-select/div/div/div/div[2]")
element.click()
excel_extract(0)
namelat=name+ ' hash_tag' + ' hello'+'.xls'
time.sleep(2)
tiny_file_rename(namelat,'D:\Downloads','D:\Covid_talkwalker')
refresh_page()

#influencer
sub_topic(2)
excel_extract(0)
namelat=name+ ' influencer' + ' hello'+'.xls'
time.sleep(2)
tiny_file_rename(namelat,'D:\Downloads','D:\Covid_talkwalker')
refresh_page()

#World Map
sub_topic(4)
excel_extract(0)
namelat=name+ ' world_map' + ' hello'+'.xls'
time.sleep(2)
tiny_file_rename(namelat,'D:\Downloads','D:\Covid_talkwalker')
refresh_page()

#all results
sub_topic(5)
scrolling_down()
excel_extract(0)
namelat=name+ ' all_results' + ' hello'+'.xls'
time.sleep(2)
tiny_file_rename(namelat,'D:\Downloads','D:\Covid_talkwalker')
refresh_page()

