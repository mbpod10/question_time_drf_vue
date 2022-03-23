import uuid as uuid_lib

from django.conf import settings
from django.db import models
from core.models import TimeStampModel


class Question(TimeStampModel):
    content = models.CharField(max_length=240)
    """ uniqueness created from questions/signals.py """
    slug = models.SlugField(max_length=255, unique=True)
    """ settings: AUTH_USER_MODEL = 'users.CustomUser' """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.content


class Answer(TimeStampModel):
    """ 
        use uuid to identify different answers 
        use uuid instead of incrimental ids so users 
        wont know how many objects are in database 
        when QUERYING database in the url; NOT USED AS primary key
    """
    uuid = models.UUIDField(
        db_index=True, default=uuid_lib.uuid4, editable=False)
    body = models.TextField()
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers')
    """ settings: AUTH_USER_MODEL = 'users.CustomUser' """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answers')
    voters = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='likes')

    def __str__(self):
        return self.author.username
