from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

#from email.policy import default

# Create your models here.
#database set up in django

#===============================================================================
# class user(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=50)
#     #get rid of userId its auto gen by django 
#     username = models.CharField(max_length=20)
#     password = models.CharField(max_length=20)
#     status = models.CharField(max_length=18)
#===============================================================================
    
status = models.CharField(max_length=18, default='Student')
status.contribute_to_class(User, 'status')

class course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courseName = models.CharField(max_length=50)
    courseType = models.CharField(max_length=30)
    
class courseusers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(course, on_delete=models.CASCADE)    
     
class questions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(course, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    date = models.CharField(max_length=20)
    comment = models.CharField(max_length=400)
    category = models.CharField(max_length=20)
 
class answers(models.Model):   
    #edit variable below
    question = models.ForeignKey(questions, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.CharField(max_length=400)
    comments = models.CharField(max_length=200)
    rating = models.IntegerField(default=0)
    date = models.CharField(max_length=20)

    class meta:
        ordering = ['rating']
 
class userratings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(answers, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=1)
 
class comments(models.Model):
    #edit variable below
    question = models.ForeignKey(questions, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    date = models.CharField(max_length=20) 

class category(models.Model):
    intent = models.CharField(max_length=50)
    
class botanswers(models.Model):
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    answer = models.CharField(max_length=400)
    rating = models.IntegerField(default=0)
    entities = models.CharField(max_length=200)
    
    
class keywords(models.Model):
    intent = models.CharField(max_length=50)
    
class courseinfo(models.Model):
    fkCourseId = models.ForeignKey(course, on_delete=models.CASCADE)
    intent = models.CharField(max_length=50)
    entities = models.CharField(max_length=200)    
    infoData = models.TextField()
    courseId = models.CharField(max_length = 15)

    
    
    
