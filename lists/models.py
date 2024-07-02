from django.db import models
from django.urls import reverse

# Create your models here.
class List(models.Model):

    def get_absolute_url(self):
        return reverse('view_list', args=[str(self.pk)])

class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, on_delete=models.CASCADE, default='')

    class Meta:
        ordering = ('id',)
        unique_together = ('text', 'list')

    def __str__(self):
        return self.text