import unittest
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class NewVisitorTest(LiveServerTestCase):
    '''new visitor's test'''

    def setUp(self):
        '''installing'''
        self.browser = webdriver.Firefox()

    def tearDown(self):
        '''uninstalling'''
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        '''can start list and retrieve it later'''

        # Andrew have known about a new cool web-app with To-Do Lists. He disided to check it's home page. 
        self.browser.get(self.live_server_url)

        # He sees that a title of the home page says about To-Do Lists 
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1')
        self.assertIn('To-Do', header_text.text)

        # This app offer him to enter a list's item
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # He entering to text-field: "I have to learn TDD"
        inputbox.send_keys('I have to learn TDD')

        # When he presses Enter keyboard button, the page updates and then list contains: "I have to learn TDD".
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table(row_text='1: I have to learn TDD')

        # The page still offering to enter a new list's item.
        # He entering: "I have to learn FastAPI".
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        inputbox.send_keys('I have to learn FastAPI')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Then the page updates again and list contains two items now.
        self.check_for_row_in_list_table(row_text='1: I have to learn TDD')
        self.check_for_row_in_list_table(row_text='2: I have to learn FastAPI')

        self.fail('Finish test!')

        # It's interesting to him will this site save his To-Do list. Then he sees, that the site have generated an uniq URL to him and shows a message with text explanasions about it.

        # He visites this URL and his To-Do list is still there.

        # He goes to sleep.