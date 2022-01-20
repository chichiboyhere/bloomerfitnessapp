from django.db import models
from tinymce.models import HTMLField
#from django.utils.html import escape
# https://dontrepeatyourself.org/post/django-blog-tutorial-part-4-posts-and-comments/

class Category(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = HTMLField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Category', related_name='posts')
    image = models.FilePathField(path="C:/Users/USER/Desktop/bloomerfit/bloomerfit/user/static/user/images")  
    def __str__(self):
        return self.title
   
class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    def __str__(self):
        return self.author

