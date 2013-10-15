from django.contrib.auth.models import User
from django.db import models
from childcare.models import Childcare


class Classroom(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    childcare = models.ForeignKey(Childcare)
    teachers = models.ManyToManyField(User)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return 'childcare/%s/classroom/%s' % (self.childcare.pk, self.pk)


class Diary(models.Model):
    author = models.ForeignKey(User)
    created = models.DateTimeField()
    modified = models.DateTimeField(auto_now=True)
    classroom = models.ForeignKey(Classroom)
    content = models.TextField()
    #images