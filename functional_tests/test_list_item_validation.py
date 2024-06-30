from unittest import skip
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_item(self):
        # Andrew opens a home page and tryes to send an empty list item. He presses Enter on an empty input-field.

        # A home page updates and there is a message about error because list items can not be empty.

        # He tryes again, but not with a text and it works.

        # He diside to send the second empty list item

        # He gets the same warrning on a list page.

        # And he can fix it by inputing the some text.
        self.fail()