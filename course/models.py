from django.db import models




class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):  
        return self.name


class Level(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    name = models.CharField(max_length=255)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CourseMaterial(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    summary = models.TextField()
    audio = models.FileField(upload_to='audio/', null=True, blank=True)
    summary_audio = models.FileField(upload_to='audio/summaries/', null=True, blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
