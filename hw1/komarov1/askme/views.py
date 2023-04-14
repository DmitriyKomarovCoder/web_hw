from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Profile, Question, Answer, Tag, LikeQuestion, LikeAnswer
from django.db.models import Count
# Create your views here.
def index(request):
    questions_page = Question.objects.new()
    questions = paginate(questions_page, request)
    tags_page = Tag.objects.most_popular()
    best_members = Profile.objects.most_popular()
    context = {'questions': questions,
               'tags': tags_page,
               'best_members': best_members}
    return render(request, "index.html", context)

def question(request, question_id):
    tags_page = Tag.objects.most_popular()
    question_page = Question.objects.get_id(question_id)
    answers = paginate(Answer.objects.most_popular(question_page), request)
    best_members = Profile.objects.most_popular()

    context = {'question': question_page,
               'tags': tags_page,
               'answers': answers,
               'best_members': best_members}
    return render(request, "question.html", context)

def hot(request):
    tags_page = Tag.objects.most_popular()
    question_page = paginate(Question.objects.get_popular(), request)
    best_members = Profile.objects.most_popular()
    context = {'questions': question_page,
               'tags' : tags_page,
               'best_members': best_members}
    return render(request, "hot.html", context)

def tag(request, name_tag):
    questions_page = Question.objects.get_tag(name_tag)
    tags_page = Tag.objects.most_popular()
    best_members = Profile.objects.most_popular()
    if not questions_page:
        return HttpResponseNotFound('Invalid tag question')

    questions_page = paginate(questions_page, request);
    context = {'questions': questions_page,
               'tag' : name_tag,
               'tags' : tags_page,
               'best_members' : best_members}
    return render(request, "tag.html", context)

def login(request):
    tags_page = Tag.objects.most_popular()
    best_members = Profile.objects.most_popular()
    context = {'tag' : tags_page,
               'best_members' : best_members}
    return render(request, "login.html", context)

def register(request):
    tags_page = Tag.objects.most_popular()
    best_members = Profile.objects.most_popular()
    context = {'tags': tags_page,
               'best_members': best_members}
    return render(request, "register.html", context)

def ask(request):
    tags_page = Tag.objects.most_popular()
    best_members = Profile.objects.most_popular()
    context = {'tags': tags_page,
               'best_members': best_members}
    return render(request, "ask.html", context)

def settings(request):
    tags_page = Tag.objects.most_popular()
    best_members = Profile.objects.most_popular()
    context = {'tags': tags_page,
               'best_members': best_members}
    return render(request, "settings.html", context)
def paginate(objects_list, request, per_page=5):
    paginator  = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    try:
        objects_page = paginator.page(page)
    except PageNotAnInteger:
        objects_page = paginator.page(1)
    except EmptyPage:
        objects_page = paginator.page(paginator.num_pages)
    return objects_page
