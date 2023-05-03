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
from django.http import Http404
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
import psycopg2

class QuestionManager(models.Manager):
    def get_id(self, id):
        try:
            question = Question.objects.annotate(num_answers=Count('answer')).prefetch_related('author', 'tag').get(id=id)
        except ObjectDoesNotExist:
            raise Http404
        return question
    def new(self):
        questions = Question.objects.annotate(num_answers=Count('answer')).prefetch_related('author', 'tag').order_by(
            '-date_create')
        return questions

    def get_tag(self, tag_name):
        try:
            tag = Tag.objects.get(name=tag_name)
            return self.filter(tag=tag).order_by('-date_create')
        except Tag.DoesNotExist:
            return None

    def get_popular(self):
        return Question.objects.annotate(num_answers=Count('answer')).prefetch_related('author', 'tag').order_by(
            '-score')
class TagManager(models.Manager):
    def most_popular(self):
        # кэшируем запрос т.к. очень затратная операция, и не требует частого обновления
        cache_key = 'most_popular_tags'
        popular_tag = cache.get(cache_key)
        if not popular_tag:
            three_months_ago = timezone.now() - timedelta(days=90)
            popular_tags = Tag.objects.annotate(num_questions=Count('question',
                           filter=Q(question__date_create__gte=three_months_ago))).order_by('-num_questions')[:10]
            cache.set(cache_key, popular_tag, 604800)
        return popular_tags

class AnswerManager(models.Manager):
    def most_popular(self, question):
        return self.all().filter(question=question).order_by('-is_correct', '-score')


class ProfileManager(models.Manager):
    def most_popular(self):
        # кэшируем запрос т.к. очень затратная операция, и не требует частого обновления
        cache_key = 'most_popular_users'
        popular_users = cache.get(cache_key)
        if not popular_users:
            three_months_ago = timezone.now() - timedelta(days=90)
            popular_users = Profile.objects.annotate(
                num_questions=Count('question', filter=Q(question__date_create__gte=three_months_ago)) +
                              Count('answer', filter=Q(question__date_create__gte=three_months_ago))).order_by(
                '-num_questions')[:5]
            cache.set(cache_key, popular_users, 604800)  # cache for 5 minutes
        return popular_users
# ========================================================================
class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField(max_length=500)
    date_create = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    tag = models.ManyToManyField('Tag')
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    objects = QuestionManager()
class Answer(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

    objects = AnswerManager()
class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    objects = TagManager()
    def __str__(self):
        return self.text
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    last_update = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to='static/img', default='static/img/avatar2.png')
    score = models.IntegerField(default=0)

    def __str__(self):
        return f'Profile {self.name}'

    objects = ProfileManager()

class LikeQuestion(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    estimation = models.BooleanField(default=True)
    class Meta:
        unique_together = ('user', 'question')

class LikeAnswer(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    estimation = models.BooleanField(default=True)
    class Meta:
        unique_together = ('user', 'answer')
