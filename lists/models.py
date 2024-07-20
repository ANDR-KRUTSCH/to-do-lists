from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

# Create your models here.
class List(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    _shared_with = models.ManyToManyField(User, related_name='lists_with_users')

    @staticmethod
    def create_new(first_item_text: str, owner: AbstractUser = None):
        list_ = List.objects.create(owner=owner)
        Item.objects.create(text=first_item_text, list=list_)
        return list_

    def get_absolute_url(self) -> str:
        return reverse(viewname='view_list', args=[str(self.pk)])
    
    @property
    def name(self) -> str:
        return self.item_set.first().text
    
    @property
    def shared_with(self):
        return ListSharedWithManager(list=self)
    

class ListSharedWithManager:
    def __init__(self, list: List) -> None:
        self.list = list
    
    def all(self):
        return self.list._shared_with.all()
    
    def add(self, email: str):
        user = User.objects.get(email=email)
        self.list._shared_with.add(user)


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, on_delete=models.CASCADE, default='')

    class Meta:
        ordering = ('id',)
        unique_together = ('text', 'list')

    def __str__(self) -> str:
        return self.text