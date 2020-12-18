from django.db import models
import datetime
from . import helpers
# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=300)
    pub_date = models.DateTimeField('Date Published',default=datetime.datetime.now())
    open_for_all = models.BooleanField(default=True)
    def __str__(self):
        return self.question_text
    def link(self):
        return helpers.inttohex(self.id) 

class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return  self.choice_text