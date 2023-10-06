from seleniumwire import webdriver

# selenium-wire proxy settings
# note: setting https:// for the 'http' key as well is not a mistake,
# but a workaround to avoid `ValueError: 
# Different settings for http and https proxy servers not supported`
seleniumwire_options = {
        'proxy': {
            'https': 'https://myusername:password@myproxyserver.com:123456', 
            'https': 'https://myusername:password@myproxyserver.com:123456',
            'no_proxy': 'localhost,127.0.0.1' # excludes
        }  
    }

# other Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--ignore-certificate-errors-spki-list')
chrome_options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome( 
                            options=chrome_options,
                            seleniumwire_options=seleniumwire_options)