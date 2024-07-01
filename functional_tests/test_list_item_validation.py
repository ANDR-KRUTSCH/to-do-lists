from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_item(self):
        # Andrew opens a home page and tryes to send an empty list item. He presses Enter on an empty input-field.
        self.browser.get(self.live_server_url)
        input = self.browser.find_element(By.CSS_SELECTOR, 'input[name="text"]')
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
        input = self.browser.find_element(By.CSS_SELECTOR, 'input[name="text"]')
        input.send_keys(Keys.ENTER)

        # He gets the same warrning on a list page.
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid'))

        # And he can fix it by inputing the some text.
        input.send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid')) 
        input.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')
        self.fail()