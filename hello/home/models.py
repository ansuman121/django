from django.db import models

# Create your models here.
class contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.BigIntegerField()
    desc = models.TextField()
    date = models.DateTimeField()


    def __str__(self):
        return self.name
class blog_post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title

