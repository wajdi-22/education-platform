from enum import Enum
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm


class Level(models.Model):
    number = models.IntegerField()



    def __str__(self):
        return f'Level :{self.number}'

class Avatar(models.Model):
    score=models.IntegerField(default=0)
    name=models.CharField(max_length=50)


class Learning_Style(Enum):
    VISUAL = 1
    AUDITORY = 2
    READ_WRITE = 3

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    avatar= models.OneToOneField(Avatar,on_delete=models.CASCADE)
    learning_style = models.IntegerField(choices=[(style.value, style.name) for style in Learning_Style])
    score = models.IntegerField(default=0)
    playtime = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.first_name} role: student'


class Parent(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    kid=models.OneToOneField(Student,on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=8)


    def __str__(self):
        return f'{self.user.first_name} role: parent of {self.kid.user.first_name}'






class Subject(models.Model):
    name = models.CharField(max_length=255)
    # description = models.TextField()
    level = models.ForeignKey(Level,on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.level.__str__()} -- {self.name} '

class Teacher(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject)
    # level= models.ForeignKey(Level,on_delete=models.CASCADE)

    def __str__(self):
        return f' {self.user.first_name} role: teacher'







class Chapter(models.Model):
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.subject.__str__()} -- {self.name} '


class CourseMaterial(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    summary = models.TextField()
    audio = models.FileField(upload_to='course/static/audio/', null=True, blank=True)
    summary_audio = models.FileField(upload_to='course/static/audio/summaries/', null=True, blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
