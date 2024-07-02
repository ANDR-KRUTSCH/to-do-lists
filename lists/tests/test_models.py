from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List

# Create your tests here.
class ItemModelTest(TestCase):
    
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

    def test_list_ordering(self):
        list_1 = List.objects.create()
        item_1 = Item.objects.create(list=list_1, text='1')
        item_2 = Item.objects.create(list=list_1, text='2')
        item_3 = Item.objects.create(list=list_1, text='3')
        self.assertEqual(list(Item.objects.all()), [item_1, item_2, item_3])

class ListAndItemModelsTest(TestCase):

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item.objects.create(text='', list=list_)
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item.objects.create(list=list_, text='bla')
            item.full_clean()

    def test_CAN_save_same_item_to_different_lists(self):
        list_1 = List.objects.create()
        list_2 = List.objects.create()

        item_1 = Item.objects.create(list=list_1, text='bla')
        item_2 = Item.objects.create(list=list_2, text='bla')

        item_2.full_clean()

    def test_str_representasion(self):
        item = Item(text='Some text')
        self.assertEqual(str(item), 'Some text')