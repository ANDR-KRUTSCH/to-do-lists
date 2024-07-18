from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class MyListsPage(object):

    def __init__(self, test: FunctionalTest) -> None:
        self.test = test

    def go_to_my_lists_page(self) -> Self:
        self.test.browser.get(self.test.live_server_url)
        self.test.browser.find_element(By.LINK_TEXT, 'My Lists').click()
        self.test.assertEqual(self.test.browser.find_element(By.TAG_NAME, 'h1').text, 'My Lists')
        return self