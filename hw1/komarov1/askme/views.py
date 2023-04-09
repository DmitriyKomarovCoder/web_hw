from . import models
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound


# Create your views here.
def index(request):
    context = {'questions': models.QUESTIONS}
    return render(request, "index.html", context)

def question(request, question_id):
    if question_id >= len(models.QUESTIONS):
        return HttpResponseNotFound('Invalid question ID')
    context = {'question': models.QUESTIONS[question_id],
               'answers': sorted(models.ANSWERS, key=lambda x: x['rating'], reverse=True)}
    return render(request, "question.html", context)

def hot(request):
    # сортирует значения и возращает max 10 элементов
    new_questions = sorted(models.QUESTIONS, key=lambda x: x['rating'], reverse=True)[:10]
    context = {'questions': new_questions}
    return render(request, "hot.html", context)

def tag(request):
    return render(request, "tag.html", context)
