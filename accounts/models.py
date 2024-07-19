import uuid

from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(primary_key=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    
    @property
    def is_anonymous(self):
        return False
    
    @property
    def is_authenticated(self):
        return True


class Token(models.Model):
    email = models.EmailField()
    uid = models.CharField(max_length=40, default=uuid.uuid4)