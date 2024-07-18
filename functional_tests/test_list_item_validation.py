from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from .base import FunctionalTest
from .list_page import ListPage

class ItemValidationTest(FunctionalTest):

    def get_error_element(self) -> WebElement:
        return self.browser.find_element(By.CSS_SELECTOR, '.has-error')

    def test_cannot_add_empty_list_item(self) -> None:
        # Andrew opens a home page and tryes to send an empty list item. He presses Enter on an empty input-field.
        self.browser.get(self.live_server_url)
        list_page = ListPage(test=self)
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        # Browser catches the request and doesn't load list page
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid'))

        # Andrew starts inputing new item text and an error disappears
        list_page.get_item_input_box().send_keys('I have to find a well-paid job.')
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid')) 

        # And he can send it successfully
        list_page.get_item_input_box().send_keys(Keys.ENTER)
        list_page.wait_for_row_in_list_table(item_text='I have to find a well-paid job.', item_number=1)

        # He diside to send the second empty list item
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        # He gets the same warrning on a list page.
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid'))

        # And he can fix it by inputing the some text.
        list_page.get_item_input_box().send_keys('I have to learn Django')
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid'))
        list_page.get_item_input_box().send_keys(Keys.ENTER)
        list_page.wait_for_row_in_list_table(item_text='I have to find a well-paid job.', item_number=1)
        list_page.wait_for_row_in_list_table(item_text='I have to learn Django', item_number=2)

    def test_cannot_add_duplicate_items(self) -> None:
        # Andrew opens the home page and starts a new list
        self.browser.get(self.live_server_url)
        list_page = ListPage(test=self)
        list_page.add_list_item(item_text='I have to find a well-paid job.')
        list_page.wait_for_row_in_list_table(item_text='I have to find a well-paid job.', item_number=1)

        # He tryes to input a duplicate item
        list_page.get_item_input_box().send_keys('I have to find a well-paid job.')
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        # He sees useful error message
        self.wait_for(lambda: self.assertEqual(self.get_error_element().text, "You've already got this in your list"))

    def test_error_messages_are_cleared_on_input(self) -> None:
        # Andrew starts a list and calls a validation error
        self.browser.get(self.live_server_url)
        list_page = ListPage(test=self)
        list_page.add_list_item(item_text='I have to find a well-paid job.')
        list_page.wait_for_row_in_list_table(item_text='I have to find a well-paid job.', item_number=1)
        list_page.get_item_input_box().send_keys('I have to find a well-paid job.')
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(self.get_error_element().is_displayed()))

        # He starts inputing to delete error message
        list_page.get_item_input_box().send_keys('I')

        # He sees that there is no error message now
        self.wait_for(lambda: self.assertFalse(self.get_error_element().is_displayed()))