from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Profile, Question, Answer, Tag, LikeQuestion, LikeAnswer

# Create your views here.
def index(request):
    questions_page = Question.objects.all().prefetch_related('author', 'tag')
    questions = paginate(questions_page, request)
    tags_page = Tag.objects.most_popular()
    context = {'questions': questions, 'tags': tags_page}
    return render(request, "index.html", context)

def question(request, question_id):
    tags_page = Tag.objects.most_popular()
    if question_id >= len(models.QUESTIONS):
        return HttpResponseNotFound('Invalid question ID')
    context = {'question': models.QUESTIONS[question_id],
               'answers': sorted(models.ANSWERS, key=lambda x: x['rating'], reverse=True),
               'tags': models.TAGS}
    return render(request, "question.html", context)

def hot(request):
    # сортирует значения и возращает max 10 элементов
    new_questions = sorted(models.QUESTIONS, key=lambda x: x['rating'], reverse=True)[:10]
    context = {'questions': new_questions, 'tags' : models.TAGS}
    return render(request, "hot.html", context)

def tag(request, name_tag):
    filtered_questions = []
    for question in models.QUESTIONS:
        if any(tag['name'] == name_tag for tag in question['tags']):
            filtered_questions.append(question)

    if not filtered_questions:
        return HttpResponseNotFound('Invalid tag question')

    questions_page = paginate(filtered_questions, request);
    context = {'questions': questions_page, 'tag' : name_tag, 'tags' : models.TAGS}
    return render(request, "tag.html", context)

def login(request):
    context = { 'tags' : models.TAGS}
    return render(request, "login.html", context)

def register(request):
    context = {'tags': models.TAGS}
    return render(request, "register.html", context)

def ask(request):
    context = {'tags': models.TAGS}
    return render(request, "ask.html", context)

def settings(request):
    context = {'tags': models.TAGS}
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
