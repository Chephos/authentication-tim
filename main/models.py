from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User 

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)

    
    def __str__(self):
        return self.title + "\n" + self.description

    def save(self, *args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args,**kwargs)

