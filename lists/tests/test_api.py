import json

from django.test import TestCase

from lists.models import List, Item

class ListAPITest(TestCase):
    # base_url = '/api/lists/{}/'
    def test_get_returns_json_200(self) -> None:
        list_ = List.create_new(first_item_text='I have to find a well-paid job.')
        
        # response = self.client.get(path=ListAPITest.base_url.format(list_.pk))
        response = self.client.get(path='/api/lists/{}/get_items'.format(list_.pk))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('content-type'), 'application/json')

    def test_get_returns_items_for_correct_list(self) -> None:
        other_list = List.objects.create()
        Item.objects.create(list=other_list, text='Item 1')
        our_list = List.objects.create()
        item_1 = Item.objects.create(list=our_list, text='Item 1')
        item_2 = Item.objects.create(list=our_list, text='Item 2')
        
        # response = self.client.get(path=ListAPITest.base_url.format(our_list.pk))
        response = self.client.get(path='/api/lists/{}/get_items'.format(our_list.pk))

        self.assertEqual(
            json.loads(s=response.content.decode()), 
            # {
            #     '1': {"id": item_1.pk, "text": item_1.text},
            #     '2': {"id": item_2.pk, "text": item_2.text},
            # }
            [{'text': 'Item 1'}, {'text': 'Item 2'}])

    def test_POSTing_a_new_item(self) -> None:
        list_ = List.objects.create()

        response = self.client.post(path='/api/lists/{}/post_item'.format(list_.pk), data={'text': 'New Item'})

        self.assertEqual(response.status_code, 201)
        
        new_item = list_.item_set.first()

        self.assertEqual(new_item.text, 'New Item')