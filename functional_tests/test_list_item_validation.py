from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_item(self):
        # Andrew opens a home page and tryes to send an empty list item. He presses Enter on an empty input-field.
        self.browser.get(self.live_server_url)
        input = self.get_item_input_box()
        input.send_keys(Keys.ENTER)

        # Browser catches the request and doesn't load list page
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid'))

        # Andrew starts inputing new item text and an error disappears
        input.send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid')) 

        # And he can send it successfully
        input.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # He diside to send the second empty list item
        input = self.get_item_input_box()
        input.send_keys(Keys.ENTER)

        # He gets the same warrning on a list page.
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid'))

        # And he can fix it by inputing the some text.
        input.send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid')) 
        input.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        # Andrew opens the home page and starts a new list
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy laptop')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy laptop')

        # He tryes to input a duplicate item
        self.get_item_input_box().send_keys('Buy laptop')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # He sees useful error message
        self.wait_for(lambda: self.assertEqual(self.browser.find_element(By.CSS_SELECTOR, '.has-error').text, "You've already got this in your list"))