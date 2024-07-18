from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListsPage

def quite_if_possible(browser: WebDriver) -> None:
    try: browser.quit()
    except: pass

class SharingTest(FunctionalTest):
    
    def test_can_share_a_list_with_another_user(self) -> None:
        # Andrew is an authenticated user
        self.create_pre_authenticated_session(email='andr.krutsch@gmail.com')
        andrews_browser = self.browser
        self.addCleanup(lambda: quite_if_possible(andrews_browser))

        # Maria opens the site too
        marias_browser = webdriver.Firefox()
        self.addCleanup(lambda: quite_if_possible(marias_browser))
        self.browser = marias_browser
        self.create_pre_authenticated_session('maria@gmail.com')

        # Andrew opens the home page and starts the new list
        self.browser = andrews_browser
        self.browser.get(self.live_server_url)
        list_page = ListPage(test=self).add_list_item(item_text='I have to find a well-paid job.')

        # He sees an option "Share with"
        share_box = list_page.get_share_box()
        self.assertEqual(share_box.get_attribute('placeholder'), 'your-friend@example.com')

        # He shared his list. The page updates and says that they both use this page now.
        list_page.share_list_with('maria@gmail.com')

        # Maria opens the "My Lists" page
        self.browser = marias_browser
        MyListsPage(test=self).go_to_my_lists_page()

        # She sees Andrew's list
        self.browser.find_element(By.LINK_TEXT, 'I have to find a well-paid job.').click()

        # The opened page says that it's the Andrew's list
        self.wait_for(lambda: self.assertEqual(list_page.get_list_owner(), 'andr.krutsch@gmail.com'))

        # She addes an element to the list
        list_page.add_list_item(item_text='Hello, Andrew!')

        # When Andrew updates the list page he sees the Maria's element
        self.browser = andrews_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table(item_text='Hello, Andrew!', item_number=2)