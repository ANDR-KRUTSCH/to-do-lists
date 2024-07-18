import re
import paramiko

from django.core import mail

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

TEST_EMAIL = 'andr.krutsch@gmail.com'
SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self) -> None:
        # Andrew opens the site and notices Log-in in nav-bar. It waits for an email from him and he inputes it
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.NAME, 'email').send_keys(TEST_EMAIL)
        self.browser.find_element(By.NAME, 'email').send_keys(Keys.ENTER)

        # There is a message that tells to him that there was sent a message to his email
        self.wait_for(lambda: self.assertIn('Check your email', self.browser.find_element(By.TAG_NAME, 'body').text))

        # Andrew checks his email and findes a message
        if self.staging_server is None:
            email = mail.outbox[0]
            self.assertIn(TEST_EMAIL, email.to)
            self.assertEqual(email.subject, SUBJECT)
            self.assertIn('Use this link to log in', email.body)
            url_search = re.search(r'http://.+/.+$', email.body)
        else:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.staging_server, port=22, username='krutsch', password=self.password)
            sftp = ssh.open_sftp()
            ls = sftp.listdir(path=f'/home/krutsch/sites/{self.hostname}/')
            for file_name in ls:
                if '.log' in file_name and 'access' not in file_name and 'error' not in file_name:
                    file = sftp.open(filename=f'/home/krutsch/sites/{self.hostname}/{file_name}', mode='r')
                    email = file.read().decode()
                    sftp.remove(f'/home/krutsch/sites/{self.hostname}/{file_name}')
                    file.close()
                    sftp.close()
                    ssh.close()
                    self.assertIn('Use this link to log in', email)
                    url_search = re.search(r'http://.+/.+', email)

        # It contains a link
        if not url_search:
            self.fail()
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Andrew presses on the link
        self.browser.get(url)

        # He logged in
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # He try to log out
        self.browser.find_element(By.ID, 'id_logout').click()

        # He logged out
        self.wait_to_be_logged_out(email=TEST_EMAIL)