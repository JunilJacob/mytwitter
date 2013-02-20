from django.db import models
class Follow(models.Model):
    username = models.CharField(max_length=30)
    followers = models.CharField(max_length=1000)
    following = models.CharField(max_length=1000)
class Post(models.Model):
	username = models.CharField(max_length=30)
	post = models.CharField(max_length=140)
	touser = models.CharField(max_length=1000)
	created = models.DateTimeField(auto_now = True)

