from selenium import webdriver
from selenium.webdriver.common.by import By

from .base import FunctionalTest
from .list_page import ListPage

class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self) -> None:
        # Andrew have known about a new cool web-app with To-Do Lists. He disided to check it's home page. 
        self.browser.get(self.live_server_url)
        list_page = ListPage(test=self)

        # He sees that a title of the home page says about To-Do Lists 
        self.assertIn('To-Do', self.browser.title)
        self.assertIn('To-Do', self.browser.find_element(By.TAG_NAME, 'h1').text)

        # This app offer him to enter a list's item
        self.assertEqual(list_page.get_item_input_box().get_attribute('placeholder'), 'Enter a to-do item')

        # He entering to text-field: "I have to learn TDD"
        list_page.add_list_item('I have to find a well-paid job.')

        # When he presses Enter keyboard button, the page updates and then list contains: "I have to learn TDD".
        list_page.wait_for_row_in_list_table(item_text='I have to find a well-paid job.', item_number=1)

        # The page still offering to enter a new list's item.
        # He entering: "I have to learn FastAPI".
        self.assertEqual(list_page.get_item_input_box().get_attribute('placeholder'), 'Enter a to-do item')
        list_page.add_list_item('I have to learn Django.')

        # Then the page updates again and list contains two items now.
        list_page.wait_for_row_in_list_table(item_text='I have to find a well-paid job.', item_number=1)
        list_page.wait_for_row_in_list_table(item_text='I have to learn Django.', item_number=2)

    def test_multiple_users_can_start_lists_at_different_urls(self) -> None:
        # Andrew starts the new list
        self.browser.get(self.live_server_url)
        list_page = ListPage(test=self)
        list_page.add_list_item(item_text='I have to find a well-paid job.')
        list_page.wait_for_row_in_list_table(item_text='I have to find a well-paid job.', item_number=1)

        # He sees that his list has a uniq URL
        andrew_list_url = self.browser.current_url
        self.assertRegex(andrew_list_url, '/lists/.+')

        # The new user, Leon, visits the web-site now

        ## We use the new browser session to delete all info from Andrew (cookie, etc.)
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Leon visits the home page. There are no any Andrew'a list signs
        self.browser.get(self.live_server_url)
        self.assertNotIn('I have to find a well-paid job.', self.browser.find_element(By.TAG_NAME, 'body').text)

        # Leon starts the new list by inputing a new item. It's less interesting then Andrew's list
        list_page.add_list_item(item_text='I have to learn Django.')
        list_page.wait_for_row_in_list_table(item_text='I have to learn Django.', item_number=1)

        # Leon gets the uniq URL
        leon_list_url = self.browser.current_url
        self.assertRegex(leon_list_url, '/lists/.+')
        self.assertNotEqual(leon_list_url, andrew_list_url)

        # One more time: there are no any Andrew's list signs
        self.assertNotIn('I have to find a well-paid job.', self.browser.find_element(By.TAG_NAME, 'body').text)