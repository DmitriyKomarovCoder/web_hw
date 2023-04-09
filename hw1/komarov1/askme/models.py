from django.db import models

ANSWERS = [
    {
        'id': i,
        'rating' : i,
        'text': f'Text{i}',
    } for i in range(15)
]

TAGS = [
    {
        'id' : i,
        'name' : f'Text{i}',
    } for i in range(5)
]

QUESTIONS = [
    {
        'id': i,
        'rating' : i,
        'title': f'Question {i}',
        'tag': TAGS[0],
        'text': f'Text{i}',
    } for i in range(15)
]