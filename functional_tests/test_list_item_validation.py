from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_item(self):
        # Andrew opens a home page and tryes to send an empty list item. He presses Enter on an empty input-field.
        self.browser.get(self.live_server_url)
        input = self.browser.find_element(By.ID, 'id_new_item')
        input.send_keys(Keys.ENTER)

        # A home page updates and there is a message about error because list items can not be empty.
        self.wait_for(lambda: self.assertEqual(self.browser.find_element(By.CSS_SELECTOR, '.has-error').text, 'You can\'t have an empty list item'))

        # He tryes again, but with a text and it works now.
        input = self.browser.find_element(By.ID, 'id_new_item')
        input.send_keys('Buy milk')
        input.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # He diside to send the second empty list item
        input = self.browser.find_element(By.ID, 'id_new_item')
        input.send_keys(Keys.ENTER)

        # He gets the same warrning on a list page.
        self.wait_for(lambda: self.assertEqual(self.browser.find_element(By.CSS_SELECTOR, '.has-error').text, 'You can\'t have an empty list item'))

        # And he can fix it by inputing the some text.
        input = self.browser.find_element(By.ID, 'id_new_item')
        input.send_keys('Make tea')
        input.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')
        self.fail()