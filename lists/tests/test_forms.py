from django.test import TestCase
from lists.forms import ItemForm, ExistingListItemForm, NewListForm, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR
from lists.models import List, Item
from unittest.mock import Mock, patch
import unittest

class ItemFormTest(TestCase):
    
    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm({'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': 'text'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.first())


class ExistingListItemFormTest(TestCase):
     
    def test_form_renders_item_text_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())

    def test_form_validation_for_blank_items(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='text')
        form = ExistingListItemForm(for_list=list_, data={'text': 'text'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])


class NewListFormTest(unittest.TestCase):

    @patch('lists.views.List.create_new')
    def test_save_creates_new_list_from_POST_data_if_user_not_authenticated(self, mock_List_create_new: Mock) -> None:
        user = Mock(is_authenticated=False)
        form = NewListForm(data={'text': 'New Item Text'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(first_item_text='New Item Text')

    @patch('lists.views.List.create_new')
    def test_save_creates_new_list_from_POST_data_if_user_authenticated(self, mock_List_create_new: Mock) -> None:
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'New Item Text'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(first_item_text='New Item Text', owner=user)

    @patch('lists.views.List.create_new')
    def test_save_returns_new_list_object(self, mock_List_create_new: Mock) -> None:
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'New Item Text'})
        form.is_valid()
        response = form.save(owner=user)
        self.assertEqual(response, mock_List_create_new.return_value)
