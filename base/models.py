from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

#1 room will have 1 topic
#1 topic will have many room 
#1 to many relation 
class Room(models.Model):
    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True) #1 host(like admin) many participants
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True) #while submitting forms it can be empty so using blank
    participants=models.ManyToManyField(User,related_name='participants', blank=True,)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True) #only takes timestamp of 1st created
    class Meta:
        ordering=['-updated','-created']
    def __str__(self):
        return self.name

class Message(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True) #only takes timestamp of 1st created
    

    def __str__(self):
        return self.body[0:50]