from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class icoder(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField((""), max_length=254)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Contacts(models.Model):
    email = models.EmailField((""), max_length=254)
    domain = models.CharField(max_length=255)
    member = models.BooleanField()
    proffesor = models.BooleanField()
    coder = models.BooleanField()
    about_yourself = models.TextField()
    query = models.TextField()

    def __str__(self):
        return self.email

class BlogPost(models.Model):
    author = models.ForeignKey(icoder , on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = RichTextUploadingField()
    domain = models.CharField(max_length=255 )
    subject = models.TextField(default="enter text")
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title




