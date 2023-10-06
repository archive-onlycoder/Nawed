# %%
# import library's
import time
from selenium import webdriver
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
import io
from PIL import Image
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pathlib import Path
from seleniumwire import webdriver

with open('config/config.json', 'r') as file:
    CONFIG_DATA = json.load(file)

GOOGLE_CUSTOM_SEARCH_API_KEY=CONFIG_DATA['GOOGLE_CUSTOM_SEARCH_API_KEY']
GOOGLE_CUSTOM_SEARCH_ENGINE_ID=CONFIG_DATA['GOOGLE_CUSTOM_SEARCH_ENGINE_ID']

from googleapiclient.discovery import build


from google.cloud import storage
GCS_S3_BUCKET_NAME=CONFIG_DATA['GCS_S3_BUCKET_NAME']
GCS_CREDENTIALS_PATH=Path.cwd()+'/'+CONFIG_DATA['GCS_CREDENTIALS_PATH']
from PIL import Image
import io

def _get_gcs_public_url(bucket_name: str, object_name: str, secure: bool=True):
    scheme = "https" if secure else "http"
    return f"{scheme}://storage.googleapis.com/{bucket_name}/{object_name}"



def _upload_to_gcs(bucket_name: str, file_name: str, buffer: bytes):

    client = storage.Client.from_service_account_json(GCS_CREDENTIALS_PATH)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(buffer)

    return _get_gcs_public_url(bucket_name, file_name)


def rtn_url(image_path,website):
    image = Image.open(image_path)

    with io.BytesIO() as buffer:
        image.save(buffer, format="PNG")
        
        return _upload_to_gcs(GCS_S3_BUCKET_NAME, website+str(time.time()).split('.')[0]+'.png', buffer.getvalue())


# Create custom search service
custom_search_service = build(
    "customsearch", "v1", developerKey=GOOGLE_CUSTOM_SEARCH_API_KEY
)


# Get estimated indexed page numbers using the google custom search api
def _get_estimated_indexed_pages(service, api_key, cx, domain):
    query = f"site:{domain}"
    response = service.cse().list(q=query, cx=cx, key=api_key).execute()
    if 'error' in response:
        if response['error']['code'] == 403 and response['error']['errors'][0]['reason'] == 'dailyLimitExceeded':
            raise Exception("Your daily quota has been exhausted.")
        else:
            raise Exception(f"An error occurred: {response['error']['message']}")

    return response['searchInformation']['totalResults']


def get_estimated_pages(domain_with_scheme: str) -> int:
    return _get_estimated_indexed_pages(
        custom_search_service,
        GOOGLE_CUSTOM_SEARCH_API_KEY,
        GOOGLE_CUSTOM_SEARCH_ENGINE_ID,
        domain_with_scheme
    )



# Create custom search service
custom_search_service = build(
    "customsearch", "v1", developerKey=GOOGLE_CUSTOM_SEARCH_API_KEY
)


# Get estimated indexed page numbers using the google custom search api
def _get_estimated_indexed_pages(service, api_key, cx, domain):
    query = f"site:{domain}"
    response = service.cse().list(q=query, cx=cx, key=api_key).execute()
    
    if 'error' in response:
        if response['error']['code'] == 403 and response['error']['errors'][0]['reason'] == 'dailyLimitExceeded':
            raise Exception("Your daily quota has been exhausted.")
        else:
            raise Exception(f"An error occurred: {response['error']['message']}")

    return response['searchInformation']['totalResults']


def get_estimated_pages(domain_with_scheme: str) -> int:
    return _get_estimated_indexed_pages(
        custom_search_service,
        GOOGLE_CUSTOM_SEARCH_API_KEY,
        GOOGLE_CUSTOM_SEARCH_ENGINE_ID,
        domain_with_scheme
    )

# import library's

# %%
# login system
inp=input('Do you want to Start Login System(Y/N)? ')
if inp.lower()=='y':
    options = webdriver.ChromeOptions() 
    if CONFIG_DATA['SHOW_Window_on_login'].lower()!='yes':
        options.add_argument('headless')

    driver = webdriver.Chrome(options=options)  # Optional argument, if not specified will search path.
    driver.implicitly_wait(10)
    print('Starting.....')

    # %%
    file_path = 'config/smush_account.txt'  # Replace 'your_file.txt' with the actual file path
    try:
        with open(file_path, 'r') as file:
            # Read the entire contents of the file
            file_contents = file.read()
            file_contents=file_contents.split('\n')
            for i in file_contents:
                driver.get('https://www.semrush.com/')
                try:
                    driver.find_element(By.CSS_SELECTOR, "#srf-search-bar")
                    print(email, 'Just Logged In a while ago')
                    continue
                except:
                    pass
                    
                try:
                    driver.find_element(By.CSS_SELECTOR, ".ch2-dialog-actions  .ch2-allow-all-btn").click()
                except:
                    pass
                email=i.split(':')[0]
                password=i.split(':')[1]


                if os.path.exists('smush_cookies/'+email+'_cookies.json'):
                    with open('smush_cookies/ijguk787duis@icznn.com_cookies.json', 'r') as file:
                        cookies = json.load(file)
                        for cookie in cookies:
                            driver.add_cookie(cookie)
                        driver.refresh()
                    try:
                        driver.find_element(By.CSS_SELECTOR, "#srf-search-bar")
                        print(email, 'logged in from before')
                        continue
                    except:
                        pass
                    

                driver.find_element(By.CSS_SELECTOR, "#loginForm #email").send_keys(email)
                driver.find_element(By.CSS_SELECTOR, "#loginForm #password").send_keys(password)
                # driver.find_element(By.CSS_SELECTOR, "#loginForm button[type=submit]").click()
                driver.execute_script("arguments[0].click()", driver.find_element(By.CSS_SELECTOR, "#loginForm button[type=submit]"))
                time.sleep(10)
                try:
                    driver.find_element(By.CSS_SELECTOR, 'button[data-test="header-menu__user"]')
                    f=True
                    pass
                except Exception as e:
                    f=False
                    print(email, 'Is Bad Credentials',e)
                    pass
                if f==True:
                    cookies = driver.get_cookies()
                    with open('smush_cookies/'+email+'_cookies.json', 'w') as file:
                        json.dump(cookies, file)
                    print(email, 'Is logged in succesfully')
                    driver.delete_all_cookies()
                
        driver.quit()
    except FileNotFoundError:
        print(f"The file  was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
# login system

# %%
# check if file is csv or excel
def is_csv(filename):
    # Get the file extension from the filename
    file_extension = os.path.splitext(filename)[1].lower()

    # Check if the file extension is CSV or Excel
    if file_extension in ['.csv']:
        return True
    else:
        return False
# check if file is csv or excel

# %%


print('\n\nIntializing Smush.....')
options = webdriver.ChromeOptions() 
options.add_argument("pageLoadStrategy=none")
options.add_argument("--disable-network-throttling")
options.add_argument("--disable-cpu-throttling")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--disable-features=NetworkService")
options.add_argument("--window-size="+str(CONFIG_DATA['Resolution-W'])+"x"+str(CONFIG_DATA['Resolution-H']))

options.add_argument("--hide-scrollbars")



if CONFIG_DATA['SHOW_Window'].lower()!='yes':
    options.add_argument('headless')


driver = webdriver.Chrome(options=options)  # Optional argument, if not specified will search path.
driver.implicitly_wait(20)
driver.set_page_load_timeout(20)
# %%
def smush_cookies():
    try:
        driver.get('https://www.semrush.com/')
    except TimeoutException:
        driver.execute_script("window.stop();")
    folder_path = 'smush_cookies'  # Replace with the actual path to your folder

    # Use os.listdir to get a list of all files and directories in the folder
    files_and_directories = os.listdir(folder_path)

    # Filter out only the files from the list
    files = [f for f in files_and_directories if os.path.isfile(os.path.join(folder_path, f))]

    # Print the list of files
    print('Logged in smush accounts:\n')
    i=1
    for file in files:
        print(str(i)+'.',file.replace('_cookies.json',''))
    try:
        s_file=int(input('Which One you want to access (write the number only): '))
    except:
        print('Wrong Type of number. Try Again ! ')
        return smush_cookies()
    
    s_file=s_file-1
    try:
        with open('smush_cookies/'+files[s_file], 'r') as file:
            # Read the entire contents of the file
            cookies = json.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.refresh()
        try:
            driver.find_element(By.CSS_SELECTOR, 'button[data-test="header-menu__user"]')
            print('Got into account, Starting Data Collecting....')
            pass
        except:
            print('Bad Credential. Try Again ! ')
            return smush_cookies()
            
                
    except FileNotFoundError:
        print(f"The file  was not found. Try again !")
        return smush_cookies()
    except Exception as e:
        print(f"An error occurred: {e}")
        return True


# %%
def confirm_after_init():

    smush_cookies()
    for index, row in df.iterrows():
        website=False
        
        try:
            website=row['Website'] 
        except:
            print("Issue: Row Number {index} skiped , can't found website")
            continue
        
        try:
            website = urlparse(website).netloc
        except Exception as e:
            print("Issue: Unknown Website in Number {index} skiped, website:",website,e)
        
        if row['Organic Search Traffic']==True and row['Authority Score']==True:
            print('Already Generated ! Skipping This one',index,website)
            continue
        loaded=True
        try:
            driver.get("https://www.semrush.com/analytics/overview/?q="+website+"&searchType=domain")
        except TimeoutException:
            driver.execute_script("window.stop();")
        except TypeError:
            loaded=False

        if loaded==True:
            try:
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-at="do-keywords-trend"]')))
            except:
                time.sleep(5)
            
            driver.execute_script('''
        document.querySelectorAll('.srf-layout_sidebar,.srf-layoutheader,.srf-layoutnotification.srf-layoutskip-to-content, .srf-layoutsearch-panel [data-ui-name="ProductHead.Row"], [data-at="report-tabs"][data-ui-name], footer, .help-menu_button, header , [data-at="do-keywords-trend"], [data-at="do-serp-features"], #srf-search-bar, [data-at="top-line"], .srf-layout__sidebar, .help-menu__button').forEach(nod=>{
        nod.remove();
        })

        document.querySelectorAll('[data-at="organic"],[data-at="adwords"],[data-at="backlinks"]').forEach(nod=>{
        nod.parentNode.remove();
        })
        ''')
            screen_shot='screenshots/'+website+".png"
            time.sleep(CONFIG_DATA['Screenshot-Delay'])
            driver.save_screenshot(screen_shot)
            try:
                authority=driver.find_element(By.CSS_SELECTOR,'[data-ui-name="Flex"][data-at="do-summary-as"] [data-at="primary-data"] a span').text
            except:
                authority=0
            
            try:
                authority_=int(float(authority))
                authority=authority_
            except:
                pass
        
            try:
                organic=driver.find_element(By.CSS_SELECTOR,'[data-ui-name="Flex"][data-at="do-summary-ot"] [data-at="primary-data"] a span').text
            except:
                organic=0
        else:
            authority=0
            organic=0


        df.loc[index, 'Authority Score'] = authority
        df.loc[index, 'Organic Search Traffic'] = organic
        if loaded:
            screen_shot=rtn_url(screen_shot,website)
        else:
            screen_shot=None

        df.loc[index, 'ImageURL'] = screen_shot

        if loaded:
            pg=get_estimated_pages('https://'+str(website))
            try:
                pg=int(float(pg))
            except:
                pass
            df.loc[index, 'Page View'] = pg
        else:
             df.loc[index, 'Page View']=0
        
        if CONFIG_DATA['RealTime_Data_Update'].lower()=='yes':
            file_path='data_files/bak_'+filename
            if is_csv(file_path):
                df.to_csv(file_path, index=False)
            else:
                df.to_excel(file_path, index=False)
            os.rename('data_files/'+filename, 'data_files/org_'+filename)
            os.rename('data_files/bak_'+filename,'data_files/'+filename)
            os.remove('data_files/org_'+filename)


        if CONFIG_DATA['RealTime_Data_Update'].lower()!='yes' or CONFIG_DATA['Save_Data_After']!=0:
            p_data=int(CONFIG_DATA['Save_Data_After'])
            if p_data % index == 0:
                file_path='data_files/bak_'+filename
                if is_csv(file_path):
                    df.to_csv(file_path, index=False)
                else:
                    df.to_excel(file_path, index=False)
                os.rename('data_files/'+filename, 'data_files/org_'+filename)
                os.rename('data_files/bak_'+filename,'data_files/'+filename)
                os.remove('data_files/org_'+filename)

        if index % 2990 == 0 and not index==0:
            print('Reach To The End, Please Switch To Another Account')
            driver.delete_all_cookies()
            smush_cookies()
                
        print(index+1,'Rows Done',website,datetime.now().strftime("%I:%M:%S %p"))
    
    print('All Done')



confirm_after_init()

