# %%
# import library's
import time
# from selenium import webdriver
import csv
import urllib.request as req
import random
from datetime import datetime
import pathlib
from selenium.webdriver.common.by import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import csv
import pandas as pd
import os
import json
from urllib.parse import urlparse
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pathlib import Path
import sys
from googleapiclient.discovery import build
from google.cloud import storage
from PIL import Image
from seleniumwire import webdriver 
import threading
import queue
project_init=False
if not os.path.isfile('config.csv'):
    CONFIG_DF=pd.DataFrame(columns=["SUMRUSH_EMAIL","PROXY","GOOGLE_CUSTOM_SEARCH_ENGINE_ID","GOOGLE_CUSTOM_SEARCH_API_KEY","GCS_S3_BUCKET_NAME","GCS_CREDENTIALS_PATH"])    
    CONFIG_DF.to_csv('config.csv',index=False)
    project_init=True
else:
    CONFIG_DF=pd.read_csv('config.csv')

if project_init:   
    sys.exit('Config And Proxy Just Intilized')
 
with open('config/global_config.json', 'r') as file:
    CONFIG_DATA = json.load(file)




def build_selenium_browser(cookie_file,cookie):
    rt={'status':False, 'browser':None,'info':None}
    pxy=False

    temp_driver_df_config=CONFIG_DF[CONFIG_DF['SUMRUSH_EMAIL']=='nawed.wahedi01@gmail.com']
    if temp_driver_df_config.empty:
        rt['info']='Account Configuration not set.'
        return rt
    else:
        account_config= temp_driver_df_config.iloc[0]
        if account_config['PROXY']:
            pxy=True
    options = webdriver.ChromeOptions() 
    options.add_argument("pageLoadStrategy=none")
    options.add_argument("--disable-network-throttling")
    options.add_argument("--disable-cpu-throttling")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--window-size="+str(CONFIG_DATA['Resolution-W'])+"x"+str(CONFIG_DATA['Resolution-H']))
    options.add_argument("--hide-scrollbars")
    if CONFIG_DATA['SHOW_Window'].lower()!='yes' and False:
        options.add_argument('headless')
    if pxy==True:
        while True:
            proxy_options = {
                'proxy': {
                    'http': 'socks5://'+account_config['PROXY'],
                    'https': 'socks5://'+account_config['PROXY'],
                    'no_proxy': 'localhost,127.0.0.1'
                }
            }
            driver = webdriver.Chrome(seleniumwire_options=proxy_options,options=options)
            driver.set_page_load_timeout(60)
            # configure proxy driver
            try:
                driver.get('https://ifconfig.me/ip')
                print('Account '+cookie+' , Proxy Ip:',driver.find_element(By.CSS_SELECTOR,'body').text)
                break
            except Exception as e:
                print(cookie,'Proxy Not Working ! ',e)
                inp=input('As Proxy Not working You want to Reconfigure or skip this account?  (Y Reconfigure /N Skip): ')
                if inp.lower()=='y':
                    inp=input('Press Enter if you reconfigured the Proxy')
                    return  build_selenium_browser(cookie_file,cookie)
                else:
                    rt['info']='Account Skiped due proxy not working '+cookie
                return rt


    else:
        driver = webdriver.Chrome(options=options)  # Optional argument, if not specified will search path.
        driver.set_page_load_timeout(60)
        # configure driver
        try:
            driver.get('https://ifconfig.me/ip')
            print('Account '+cookie+' , Proxy Ip:',driver.find_element(By.CSS_SELECTOR,'body').text())
        except:
            print(cookie,'Proxy Not Working ! ')
            rt['info']='Proxy not working '+cookie
            return rt
    
    try:
        driver.get('https://www.semrush.com/')
    except TimeoutException:
        driver.execute_script("window.stop();")
    # load semrush

    try:
        with open(cookie_file, 'r') as file:
            # Read the entire contents of the file
            cookies__ = json.load(file)
            for cookie__ in cookies__:
                driver.add_cookie(cookie__)
            driver.refresh()
        c_=0
        while True:
            if c_>0:
                driver.execute_script("window.stop();")
            c_+=1
            
            if c_>5:
                rt['info']='Bad Credential. Try Again ! '+cookie
                return rt
                break
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[data-test="header-menu__user"]'))
                )
                rt['status']=True
                rt['browser']=driver            
                print(cookie,' Logged in successfully.')
                rt['browser']={'driver':driver,'config':account_config}
                return rt
                break
                pass
            except TimeoutException as e:
                continue
            except Exception as e:
                print(cookie,'Bad Credential. Try Again ! ',e)
                rt['info']='Bad Credential. Try Again ! '+cookie
                return rt
            
                
    except FileNotFoundError:
        print(f"The file  was not found. Try again !")
        rt['info']='Bad Credential. Try Again ! '+cookie
        return rt
    except Exception as e:
        print(f"An error occurred: {e}")
        rt['info']='An error occurred: {e}" ! '+cookie
        return rt
    return rt

d=[['smush_cookies/nawedwa.hedi01@gmail.com_cookies.json','nawedwa.hedi01'],['smush_cookies/nawedw.ahedi01@gmail.com_cookies.json','nawedwa.hedi02']]




threads = []
results = queue.Queue()

# Create and start multiple threads
num_threads = 5

for i in d:
    thread = threading.Thread(target=lambda i=i: results.put(build_selenium_browser(i[0],i[1])))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Retrieve results from the queue
while not results.empty():
    result = results.get()
    print(result)

print("Account Threads Initlized!")