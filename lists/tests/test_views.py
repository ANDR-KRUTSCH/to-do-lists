import unittest
from unittest import skip
from unittest.mock import Mock, patch

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.http.request import HttpRequest
from django.utils.html import escape

from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR
# from lists.views import new_list

User = get_user_model()

# Create your tests here.
class HomePageViewTest(TestCase):

    def test_user_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(f'/lists/{list_.id}/', data={'text': ''})

    def test_uses_list_template(self):
        '''Test: uses list template'''
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        '''test: passes correct list to template'''
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    @skip
    def test_displays_only_items_for_that_list(self):
        '''Test: all list items displaying'''
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        another_list = List.objects.create()
        Item.objects.create(text='another itemey 1', list=another_list)
        Item.objects.create(text='another itemey 2', list=another_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'another itemey 1')
        self.assertNotContains(response, 'another itemey 2')

    def test_can_save_a_POST_request_to_an_existing_list(self):
        '''test: can save a POST-request to an existing list'''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/', data={'text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirect_to_list_view(self):
        '''test: redirecting to list view'''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/', data={'text': 'A new item for existing list'})

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_for_invalid_input_nothing_save_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list_1 = List.objects.create()
        item_1 = Item.objects.create(list=list_1, text='text')
        response = self.client.post(f'/lists/{list_1.id}/', data={'text': 'text'})

        self.assertContains(response, escape(DUPLICATE_ITEM_ERROR))
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.count(), 1) 


class NewListViewIntegratedTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_invalid_list_items_arrent_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_list_owner_is_saved_if_user_is_authenticated(self):
        user = User.objects.create(email='andr.krutsch@gmail.com')
        self.client.force_login(user)

        self.client.post('/lists/new', data={'text': 'new item'})

        list_ = List.objects.first()
        self.assertEqual(list_.owner, user)


class MyListsViewTest(TestCase):
    def test_my_lists_url_renders_my_lists_template(self):
        user = User.objects.create(email='andr.krutsch@gmail.com')
        response = self.client.get(f'/lists/users/{user.email}/')
        self.assertTemplateUsed(response, 'my_lists.html')

    def test_passes_correct_owner_to_template(self):
        User.objects.create(email='temp@gmail.com')
        correct_user = User.objects.create(email='andr.krutsch@gmail.com')
        response = self.client.get(f'/lists/users/{correct_user.email}/')
        self.assertEqual(response.context['owner'], correct_user)


# @patch('lists.views.NewListForm')
# class NewListViewUnitTest(unittest.TestCase):
#     def setUp(self) -> None:
#         # self.client = Client()
#         self.request = HttpRequest()
#         self.request.POST['text'] = 'New List Item'
#         self.request.user = Mock()

#     @patch('lists.views.redirect')
#     def test_passes_POST_data_to_NewListForm(self, mock_redirect: Mock, mock_NewListForm: Mock) -> None:
#         new_list(request=self.request)
#         mock_NewListForm.assert_called_once_with(data=self.request.POST)

#     @patch('lists.views.redirect')
#     def test_saves_form_with_owner_if_form_valid(self, mock_redirect: Mock, mock_NewListForm: Mock) -> None:
#         mock_form = mock_NewListForm.return_value
#         mock_form.is_valid.return_value = True
#         new_list(request=self.request)
#         mock_form.save.assert_called_once_with(owner=self.request.user)

#     @patch('lists.views.redirect')
#     def test_redirects_to_form_returned_object_if_form_valid(self, mock_redirect: Mock, mock_NewListForm: Mock) -> None:
#         mock_form = mock_NewListForm.return_value
#         mock_form.is_valid.return_value = True

#         response = new_list(request=self.request)
        
#         self.assertEqual(response, mock_redirect.return_value)
#         mock_redirect.assert_called_once_with(to=mock_form.save.return_value)

#     @patch('lists.views.render')
#     def test_renders_home_template_with_form_if_form_invalid(self, mock_render: Mock, mock_NewListForm: Mock) -> None:
#         mock_form = mock_NewListForm.return_value
#         mock_form.is_valid.return_value = False

#         response = new_list(request=self.request)

#         self.assertEqual(response, mock_render.return_value)
#         mock_render.assert_called_once_with(request=self.request, template_name='home.html', context={'form': mock_form})

#     @patch('lists.views.render')
#     def test_does_not_save_if_form_invalid(self, mock_render: Mock, mock_NewListForm: Mock) -> None:
#         mock_form = mock_NewListForm.return_value
#         mock_form.is_valid.return_value = False

#         new_list(request=self.request)
#         self.assertFalse(mock_form.save.called)


class ShareListViewTest(TestCase):

    def test_POST_redirects_to_list_page(self) -> None:
        user = User.objects.create(email='andr.krutsch@gmail.com')
        list_ = List.objects.create(owner=user)
        self.client.force_login(user=user)
        response = self.client.post(path=f'/lists/{list_.pk}/share', data={'sharee': user.email})
        self.assertRedirects(response, list_.get_absolute_url())

    def test_can_share_list_with_user(self):
        user = User.objects.create(email='andr.krutsch@gmail.com')
        list_ = List.objects.create(owner=user)
        self.client.force_login(user=user)
        self.client.post(path=f'/lists/{list_.pk}/share', data={'sharee': user.email})
        self.assertIn(user, list_.shared_with.all())

    def test_incorrect_list_id_raises_404(self):
        user = User.objects.create(email='andr.krutsch@gmail.com')
        self.client.force_login(user=user)
        response = self.client.post(path=f'/lists/0/share', data={'sharee': user.email})
        self.assertEqual(response.status_code, 404)

    def test_returns_400_if_sharing_with_non_existing_user(self):
        user = User.objects.create(email='andr.krutsch@gmail.com')
        list_ = List.objects.create(owner=user)
        self.client.force_login(user=user)
        response = self.client.post(path=f'/lists/{list_.pk}/share')
        self.assertEqual(response.status_code, 400)

    # def test_only_authenticated_users_can_share_lists(self):
    #     user = User.objects.create(email='andr.krutsch@gmail.com')
    #     list_ = List.objects.create(owner=user)
    #     response = self.client.post(path=f'/lists/{list_.pk}/share', data={'sharee': user.email})
    #     self.assertEqual(response.headers.get('Location'), '/accounts/login/?next=/lists/1/share')

    def test_only_authenticated_users_can_share_lists(self):
        user = User.objects.create(email='andr.krutsch@gmail.com')
        list_ = List.objects.create(owner=user)
        response = self.client.post(path=f'/lists/{list_.pk}/share', data={'sharee': user.email})
        self.assertEqual(response.status_code, 400)