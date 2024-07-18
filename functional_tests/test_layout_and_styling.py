from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest
from .list_page import ListPage

class TestLayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self) -> None:
        # Andrew opens the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # He notices that input field was centred
        list_page = ListPage(test=self)
        inputbox = list_page.get_item_input_box()
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)

        # He starts the new list and sees that input field is also centered there
        inputbox.send_keys('I have to find a well-paid job.')
        inputbox.send_keys(Keys.ENTER)
        list_page.wait_for_row_in_list_table(item_text='I have to find a well-paid job.', item_number=1)
        inputbox = list_page.get_item_input_box()
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)