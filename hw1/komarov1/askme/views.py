from . import models
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    context = {'questions': models.QUESTIONS}
    return render(request, "index.html", context)

def question(request, question_id):
    context = {'question': models.QUESTIONS[question_id]}
    return render(request, "question.html", context)
