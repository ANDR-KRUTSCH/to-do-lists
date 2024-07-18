import os
import time

from typing import Callable, Any

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings

from .server_tools import reset_database
from .server_tools import create_session_on_server

from .management.commands.create_session import create_pre_authenticated_session

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webelement import WebElement

MAX_WAIT = 10

def wait(fn: Callable) -> Callable:
    def modified_fn(*args, **kwargs) -> Any:
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server is not None:
            self.password = os.environ.get('PASSWORD')
            self.assertNotEqual(self.password, None)
            self.live_server_url = 'http://' + self.staging_server
            reset_database(self.staging_server)
            self.hostname = 'www.staging.to-do-lists.com'

    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text: str) -> None:
        start_time = time.time()
        while True:
            try:
                rows = self.browser.find_elements(By.CSS_SELECTOR, '#id_list_table tr')
                self.assertIn(row_text, [row.text for row in rows])
                return None
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    @wait
    def wait_for(self, fn: Callable) -> Any:
        return fn()

    def get_item_input_box(self) -> WebElement:
        return self.browser.find_element(By.CSS_SELECTOR, 'input[name="text"]')
    
    @wait
    def wait_to_be_logged_in(self, email: str) -> None:
        # self.browser.find_element(By.ID, 'id_logout')
        self.assertIn(email, self.browser.find_element(By.CSS_SELECTOR, '.navbar').text)

    @wait
    def wait_to_be_logged_out(self, email: str) -> None:
        # self.browser.find_element(By.NAME, 'email')
        self.assertNotIn(email, self.browser.find_element(By.CSS_SELECTOR, '.navbar').text)

    def add_list_item(self, item_text: str) -> None:
        num_rows = len(self.browser.find_elements(By.CSS_SELECTOR, '#id_list_table tr'))
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        num_rows += 1
        self.wait_for_row_in_list_table(row_text=f'{num_rows}: {item_text}')

    def create_pre_authenticated_session(self, email: str) -> None:
        if self.staging_server:
            session_key = create_session_on_server(host=self.staging_server, email=email)
        else:
            session_key = create_pre_authenticated_session(email=email)
        self.browser.get(self.live_server_url + '/404_no_such_url/')
        self.browser.add_cookie(
            dict(
                name=settings.SESSION_COOKIE_NAME,
                value=session_key,
                path='/',
            )
        )