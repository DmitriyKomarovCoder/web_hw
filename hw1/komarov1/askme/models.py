from django.db import models

QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'text': f'Text{i}',
    } for i in range(3)
]
