import re
from django.core import mail
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

TEST_EMAIL = 'andr.krutsch@gmail.com'
SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):
    def test_can_get_email_link_to_log_in(self):
        # Andrew opens the site and notices Log-in in nav-bar. It waits for an email from him and he inputes it
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.NAME, 'email').send_keys(TEST_EMAIL)
        self.browser.find_element(By.NAME, 'email').send_keys(Keys.ENTER)

        # There is a message that tells to him that there was sent a message to his email
        self.wait_for(lambda: self.assertIn('Check your email', self.browser.find_element(By.TAG_NAME, 'body').text))

        # Andrew checks his email and findes a message
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # It contains a link
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail()
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Andrew presses on the link
        self.browser.get(url)

        # He logged in
        self.wait_for(lambda: self.browser.find_element(By.ID, 'id_logout'))
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)
        self.wait_for(lambda: self.browser.find_element(By.ID, 'id_logout'))
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)

        # He try to log out
        self.browser.find_element(By.ID, 'id_logout').click()

        # He logged out
        self.wait_for(lambda: self.browser.find_element(By.NAME, 'email'))
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertNotIn(TEST_EMAIL, navbar.text)