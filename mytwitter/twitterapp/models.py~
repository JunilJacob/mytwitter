from django.db import models
class Follow(models.Model):
    username = models.CharField(max_length=30)
    following = models.CharField(max_length=1000)#list of users the user is following
class Post(models.Model):
	username = models.CharField(max_length=30)
	post = models.CharField(max_length=140)
	created = models.DateTimeField(auto_now = True)

