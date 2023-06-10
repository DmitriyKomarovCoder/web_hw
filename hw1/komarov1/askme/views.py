import json
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.forms import model_to_dict
from django.contrib import auth
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_http_methods

from .forms import LoginForm, RegistrationForm, AnswerForm, QuestionForm, SettingsForm
from .models import Profile, Question, Answer, Tag, LikeQuestion, LikeAnswer
from django.db.models import Count
# Create your views here.

#@login_required(login_url='login/', redirect_field_name='continue')
def index(request):
    questions_page = Question.objects.new()
    questions = paginate(questions_page, request)
    tags_page = Tag.objects.most_popular()
    best_members = Profile.objects.most_popular()
    context = {'questions': questions,
               'tags': tags_page,
               'best_members': best_members}
    return render(request, "index.html", context)

def question(request, question_id, page_num=1):
    if request.method == 'GET':
        answer_form = AnswerForm()
    question_page = Question.objects.get_id(question_id)
    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(request.user.profile, question_page)
            answers = paginate(Answer.objects.most_popular(question_page), request)
            page_num = answers.paginator.num_pages
            return redirect(reverse('question_page', args=(question_id, page_num)) + f'?page={page_num}#{answer.id}')

        else:
            answer_form.add_error("Invalid parameters")
    tags_page = Tag.objects.most_popular()
    answers = paginate(Answer.objects.most_popular(question_page), request)
    best_members = Profile.objects.most_popular()
    context = {'question': question_page,
               'tags': tags_page,
               'answers': answers,
               'best_members': best_members,
               'form': answer_form,
               'page_num': page_num}
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

    questions_page = paginate(questions_page, request)
    context = {'questions': questions_page,
               'tag' : name_tag,
               'tags' : tags_page,
               'best_members' : best_members}
    return render(request, "tag.html", context)

def log_in(request):
    if request.method == 'GET':
        login_form = LoginForm(request.GET.get('next'))
        print("Выводим параметр", request.GET)
    elif request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request=request, **login_form.cleaned_data)
            if user:
                login(request, user)
                #redirect_uri = request.GET.get('redirect_uri', reverse('index'))
                return redirect('index')
            login_form.add_error(None, "Invalid username or password")

    tags_page = Tag.objects.most_popular()
    best_members = Profile.objects.most_popular()
    context = {'tags' : tags_page,
               'best_members' : best_members,
               'form': login_form}
    return render(request, "login.html", context)

@login_required
def log_out(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))

def register(request):
    if request.method == 'GET':
        user_form = RegistrationForm()
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                return redirect('index')
            else:
                user_form.add_error(field=None, error="User saving error!")
    tags_page = Tag.objects.most_popular()
    best_members = Profile.objects.most_popular()
    context = {'tags': tags_page,
               'best_members': best_members,
               'form': user_form}
    return render(request, "register.html", context)

@login_required(login_url='login')
def ask(request):
    if request.method == 'GET':
        question_form = QuestionForm()
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(request.user.profile)
            return redirect('question', question.id)
    tags_page = Tag.objects.most_popular()
    best_members = Profile.objects.most_popular()
    context = {'tags': tags_page,
               'best_members': best_members,
               'form': question_form}
    return render(request, "ask.html", context)

@login_required
@require_http_methods(['GET', 'POST'])
def settings(request):
    #profile = request.user.profile
    if request.method == 'GET':
        data = model_to_dict(request.user)
        settings_form = SettingsForm(initial=data)
    if request.method == 'POST':
        settings_form = SettingsForm(request.POST, files=request.FILES, instance=request.user)
        if settings_form.is_valid():
            settings_form.save()
            return redirect('settings')

    tags_page = Tag.objects.most_popular()
    best_members = Profile.objects.most_popular()
    context = {'tags': tags_page,
               'best_members': best_members,
               'form': settings_form}
    return render(request, "settings.html", context)

def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page') or request.POST.get('page')
    try:
        objects_page = paginator.page(page)
    except PageNotAnInteger:
        objects_page = paginator.page(1)
    except EmptyPage:
        objects_page = paginator.page(paginator.num_pages)
    return objects_page

@login_required
@require_POST
def vote_up(request):
    question_id = request.POST['question_id']
    question = Question.objects.get(id=question_id)
    question.score += 1
    question.save()

    like = LikeQuestion.objects.create(question=question, user=request.user.profile)
    like.save()
    return JsonResponse({
        'new_rating': question.score
    })