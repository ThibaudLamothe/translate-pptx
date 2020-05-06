import random
import time
import logzero
import logging
from logzero import logger
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

class seleniumDefault:

    def __init__(self, driver_path='chromedriver', loglevel='error'):
        
        self.driver_path = driver_path
        self.original_window = None
        self.display_sleep_time=False
        self.url = None

        self.create_driver()
        self.set_loglevel(loglevel)
    
    def create_driver(self):
        logger.error(self.driver_path)
        self.driver = webdriver.Chrome(self.driver_path)

    def add_url(url):
        self.url = url    

    def load_url(self, sleep=3):
        self.driver.get(self.url)
        self.original_window =  self.driver.window_handles[0]
        self.sleep(sleep, 'Load url : {}'.format(self.url))

    def scroll_to_element(self, elmt, sleep=1):
        y = elmt.location['y']
        logger.debug('scrolling to y={}'.format(y))
        y = y - 150
        self.driver.execute_script("window.scrollTo(0, {})".format(y))
        self.sleep(sleep)

    def sleep(self, sleep=1, message='Wait'):
        if self.display_sleep_time:
            logger.info('({} s.) - {}'.format(sleep, message))
        noise = random.random() - 0.5
        sleep = max(sleep + noise, 1)
        time.sleep(sleep)

    def close_driver(self):
        logger.error('Exit navigation.')
        self.driver.quit()
        

    def set_loglevel(self, level):
        level_table = {
            'debug':logging.DEBUG,
            'warn':logging.WARNING,
            'warning':logging.WARNING,
            'info':logging.INFO,
            'error':logging.ERROR
        }
        loglevel = level_table[level.lower()]
        logzero.loglevel(loglevel)
        
    # def add_user_agent(user_agent=None):
    #     self.user_agent = 'Mozilla/5.0 (Linux; Android 7.0; SM-G930VC Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36'
    #     opts = Options()
    #     opts.add_argument(USER_AGENT)
    #     # driver = webdriver.Chrome(path, options=opts)
