import unittest
from selenium import webdriver

class NewVisitorTest(unittest.TestCase):
    '''new visitor's test'''

    def setUp(self):
        '''installing'''
        self.browser = webdriver.Firefox()

    def tearDown(self):
        '''uninstalling'''
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        '''can start list and retrieve it later'''

        # Andrew have known about a new cool web-app with To-Do Lists. He disided to check it's home page. 
        self.browser.get('http://localhost:8000')

        # He sees that a title of the home page says about To-Do Lists 
        self.assertIn('To-Do', self.browser.title)
        self.fail()

        # This app offer him to enter a list's item

        # He entering to text-field: "I have to learn TDD"

        # When he presses Enter keyboard button, the page updates and then list contains: "I have to learn TDD". 

        # The page still offering to enter a new list's item.
        # He entering: "I have to learn FastAPI".

        # Then the page updates again and list contains two items now.

        # It's interesting to him will this site save his To-Do list. Then he sees, that the site have generated an uniq URL to him and shows a message with text explanasions about it.

        # He visites this URL and his To-Do list is still there.

        # He goes to sleep.


if __name__ == '__main__':
    unittest.main(warnings='ignore')