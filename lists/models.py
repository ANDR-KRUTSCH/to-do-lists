from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class List(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    @staticmethod
    def create_new(first_item_text: str, owner: AbstractUser = None):
        list_ = List.objects.create(owner=owner)
        Item.objects.create(text=first_item_text, list=list_)
        return list_

    def get_absolute_url(self):
        return reverse('view_list', args=[str(self.pk)])
    
    @property
    def name(self):
        return self.item_set.first().text

class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, on_delete=models.CASCADE, default='')

    class Meta:
        ordering = ('id',)
        unique_together = ('text', 'list')

    def __str__(self):
        return self.text