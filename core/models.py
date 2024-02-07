from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

user=get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(user,on_delete=models.CASCADE)
    id_user = models.IntegerField()
    profPic=models.ImageField(upload_to="profile_images",default='blank-profile-picture.png')
    bio=models.TextField(blank=True)
    location=models.CharField(max_length=100,blank=True)
    
    def __str__(self):
        return self.user.get_username()