from django.db import models

#TAGS = [
#    {
#        'id' : i,
#        'name' : f'Text{i}',
#    } for i in range(5)
#]
#
#QUESTIONS = [
#    {
#        'id': i,
#        'rating' : i,
#        'title': f'Question {i}',
#        'tags': [TAGS[0], TAGS[1]],
#        'text': f'Text{i}',
#    } for i in range(15)
#]
#
#ANSWERS = [
#    {
#        'id': i,
#        'rating' : i,
#        'tag' : TAGS[0],
#        'text': f'Text{i}',
#    } for i in range(15)
#]
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q
import psycopg2

class TagManager(models.Manager):
    def most_popular(self):
        three_months_ago = timezone.now() - timedelta(days=90)
        popular_tags = Tag.objects.annotate(num_questions=Count('question', filter=Q(question__date_create__gte=three_months_ago))).order_by('-num_questions')[:10]
        return popular_tags
# ========================================================================
class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    tag = models.ManyToManyField('Tag')
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.title
class Answer(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    text = models.TextField()
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
class Tag(models.Model):
    name = models.CharField(max_length=255)

    objects = TagManager()
    def __str__(self):
        return self.text
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    last_update = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to='img/')
    score = models.IntegerField(default=0)

    def __str__(self):
        return f'Profile {self.name}'

class LikeQuestion(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'question')

class LikeAnswer(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        unique_together = ('user', 'answer')
