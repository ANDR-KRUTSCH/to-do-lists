from django import forms
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

EMPTY_ITEM_ERROR = "You can't have an empty list item"

DUPLICATE_ITEM_ERROR = "You've already got this in your list"

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg',
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR},
        }
    

class ExistingListItemForm(ItemForm):
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self) -> None:
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            self.add_error('text', DUPLICATE_ITEM_ERROR)
    

class NewListForm(ItemForm):
    def save(self, owner: AbstractUser = None) -> None:
        if owner.is_authenticated:
            return List.create_new(first_item_text=self.cleaned_data['text'], owner=owner)
        else:
            return List.create_new(first_item_text=self.cleaned_data['text'])