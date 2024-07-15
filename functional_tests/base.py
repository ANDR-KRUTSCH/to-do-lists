from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import os
import time

MAX_WAIT = 10

class FunctionalTest(StaticLiveServerTestCase):

    MAX_WAIT = 10

    def setUp(self):
        '''installing'''
        self.browser = webdriver.Firefox()
        self.staging_server = os.environ.get('STAGING_SERVER')
        self.password = os.environ.get('PASSWORD')
        if self.staging_server:
            self.live_server_url = 'http://' + self.staging_server
            if self.staging_server == 'localhost':
                self.hostname = 'www.staging.to-do-lists.com'
            elif self.staging_server == '127.0.0.1':
                self.hostname = 'www.live.to-do-lists.com'

    def tearDown(self):
        '''uninstalling'''
        self.browser.quit()

    def wait(fn):
        def modified_dn(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > MAX_WAIT:
                        raise e
                    time.sleep(0.5)
        return modified_dn

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > self.MAX_WAIT:
                    raise e
                time.sleep(0.5)

    @wait
    def wait_for(self, fn):
        return fn()

    def get_item_input_box(self):
        return self.browser.find_element(By.CSS_SELECTOR, 'input[name="text"]')
    
    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element(By.ID, 'id_logout')
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element(By.NAME, 'email')
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertNotIn(email, navbar.text)