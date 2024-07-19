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
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.service import Service

MAX_WAIT = 10

def wait(func: Callable) -> Callable:
    def inner(*args, **kwargs) -> Any:
        start_time = time.time()
        while True:
            try:
                return func(*args, **kwargs)
            except (AssertionError, WebDriverException) as error:
                if time.time() - start_time > MAX_WAIT:
                    raise error
                time.sleep(0.5)
    return inner

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self) -> None:
        service = Service(executable_path='/usr/local/bin/geckodriver')
        self.browser = webdriver.Firefox(service=service)

        self.staging_server = os.environ.get('STAGING_SERVER')
        
        if self.staging_server is not None:
            self.password = os.environ.get('PASSWORD')
            self.assertNotEqual(self.password, None)
            self.live_server_url = 'http://' + self.staging_server
            reset_database(self.staging_server)
            self.hostname = 'www.staging.to-do-lists.com'

    def tearDown(self) -> None:
        self.browser.quit()

    @wait
    def wait_for(self, fn: Callable) -> Any:
        return fn()
    
    @wait
    def wait_to_be_logged_in(self, email: str) -> None:
        self.assertIn(email, self.browser.find_element(By.CSS_SELECTOR, '.navbar').text)

    @wait
    def wait_to_be_logged_out(self, email: str) -> None:
        self.assertNotIn(email, self.browser.find_element(By.CSS_SELECTOR, '.navbar').text)

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