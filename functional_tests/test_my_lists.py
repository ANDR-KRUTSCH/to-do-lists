from .base import FunctionalTest
from selenium.webdriver.common.by import By
from django.conf import settings
from django.contrib.auth import get_user_model
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session

User = get_user_model()

class MyListsTest(FunctionalTest):
    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email=email)
        self.browser.get(self.live_server_url + '/404_no_such_url/')
        self.browser.add_cookie(
            dict(
                name=settings.SESSION_COOKIE_NAME,
                value=session_key,
                path='/',
            )
        )

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Andrew is an authenticated user
        self.create_pre_authenticated_session(email='andr.krutsch@gmail.com')

        # He opens the home page and starts the new list
        self.browser.get(self.live_server_url)
        self.add_list_item('I have to learn Django, TDD, FastAPI...')
        self.add_list_item('I have to find a well-paid job.')
        first_list_url = self.browser.current_url

        # He sees the link "My Lists" for the first time
        self.browser.find_element(By.LINK_TEXT, 'My Lists').click()

        # He sees that his list in there and it has the name like the first item's text
        self.wait_for(lambda: self.browser.find_element(By.LINK_TEXT, 'I have to learn Django, TDD, FastAPI...'))
        self.browser.find_element(By.LINK_TEXT, 'I have to learn Django, TDD, FastAPI...').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, first_list_url))

        # He decides to start a one more list just to make sure
        self.browser.get(self.live_server_url)
        self.add_list_item('I have to learn Docker, GIT, PostgreSQL...')
        second_list_url = self.browser.current_url

        # There is a one more list under the title "My Lists" now
        self.browser.find_element(By.LINK_TEXT, 'My Lists').click()
        self.wait_for(lambda: self.browser.find_element(By.LINK_TEXT, 'I have to learn Docker, GIT, PostgreSQL...'))
        self.browser.find_element(By.LINK_TEXT, 'I have to learn Docker, GIT, PostgreSQL...').click()
        self.assertEqual(self.browser.current_url, second_list_url)

        # He logs out and there is no the link "My Lists" now
        self.browser.find_element(By.ID, 'id_logout').click()
        self.wait_for(lambda: self.assertEqual(self.browser.find_elements(By.LINK_TEXT, 'My lists'), []))