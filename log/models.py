from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return "{}:{}".format(self.user_id, self.password)