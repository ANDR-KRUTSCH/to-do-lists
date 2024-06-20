from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

class NewVisitorTest(LiveServerTestCase):
    '''new visitor's test'''

    MAX_WAIT = 10

    def setUp(self):
        '''installing'''        
        self.browser = webdriver.Firefox()

    def tearDown(self):
        '''uninstalling'''
        self.browser.quit()

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

    def test_can_start_a_list_for_one_user(self):
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
        self.wait_for_row_in_list_table(row_text='1: I have to learn TDD')

        # The page still offering to enter a new list's item.
        # He entering: "I have to learn FastAPI".
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        inputbox.send_keys('I have to learn FastAPI')
        inputbox.send_keys(Keys.ENTER)

        # Then the page updates again and list contains two items now.
        self.wait_for_row_in_list_table(row_text='1: I have to learn TDD')
        self.wait_for_row_in_list_table(row_text='2: I have to learn FastAPI')

        # He goes to sleep.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        '''Test: multiple users can start lists at different urls'''
        
        # Andrew starts the new list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('I have to learn TDD')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: I have to learn TDD')

        # He sees that his list has a uniq URL
        andrew_list_url = self.browser.current_url
        self.assertRegex(andrew_list_url, '/lists/.+')

        # The new user, Leon, visits the web-site now

        ## We use the new browser session to delete all info from Andrew (cookie, etc.)
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Leon visits the home page. There are no any Andrew'a list signs
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('I have to learn TDD', page_text)
        self.assertNotIn('I have to learn FastAPI', page_text)

        # Leon starts the new list by inputing a new item. It's less interesting then Andrew's list
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('I have to find a well paid job')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: I have to find a well paid job')

        # Leon gets the uniq URL
        leon_list_url = self.browser.current_url
        self.assertRegex(leon_list_url, '/lists/.+')
        self.assertNotEqual(leon_list_url, andrew_list_url)

        # One more time: there are no any Andrew's list signs
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('I have to learn TDD', page_text)
        self.assertIn('I have to find a well paid job', page_text)

        # They both go to sleep

    def test_layout_and_styling(self):
        '''test: layout and styling'''
        # Andrew opens the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # He notices that input field was centred
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)

        # He starts the new list and sees that input field is also centered there
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)