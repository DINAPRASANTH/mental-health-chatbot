from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f'{self.user.username}: {self.message}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lang = models.CharField(max_length=20,null=True,blank=True)
    color = models.CharField(max_length=20, null=True, blank=True)
    season = models.CharField(max_length=20, null=True, blank=True)
    pet = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    age_group = models.CharField(max_length=10, null=True, blank=True)
    def _str_(self):
        return f'{self.user.username}: {self.lang}, {self.color}, {self.season}, {self.pet},{self.color},{self.gender},{self.age_group}'