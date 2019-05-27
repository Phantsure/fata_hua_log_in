from django.db import models

# Create your models here.
class Blogs(models.Model):
    blog_titles = models.CharField(max_length=100)

    def __str__(self):
        return self.blog_titles