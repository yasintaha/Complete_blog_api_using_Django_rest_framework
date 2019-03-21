from django.db import models 
from django.utils import timezone
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
# Create your models here.

def create_auth_token(sender, instance=None, created=False,**kwargs):
    if created:
        print(instance)
        Token.objects.create(user=instance)

post_save.connect(create_auth_token,sender=User)


class PostModel(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title = models.CharField(max_length=243)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title    

    def __str__(self):
        return self.text  

class CommentModel(models.Model):
    post = models.ForeignKey('api.PostModel',on_delete=models.CASCADE)
    author = models.CharField(max_length=243)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text            