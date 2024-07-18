from selenium import webdriver
from selenium.webdriver.common.by import By

from .base import FunctionalTest

def quite_if_possible(browser) -> None:
    try: browser.quit()
    except: pass

class SharingTest(FunctionalTest):
    
    def test_can_share_a_list_with_another_user(self):
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
        self.add_list_item(item_text='I have to find a well-paid job.')

        # He sees an option "Share this list"
        share_bow = self.browser.find_element(By.CSS_SELECTOR, 'input[name="share"]')
        self.assertEqual(share_bow.get_attribute('placeholder'), 'your-friend@example.com')