from django.db import models

# Create your models here.
class tasks(models.Model):
    name = models.CharField(max_length=255)
    task = models.TextField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name