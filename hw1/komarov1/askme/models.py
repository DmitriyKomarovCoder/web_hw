from django.db import models

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
        'tags': [TAGS[0], TAGS[1]],
        'text': f'Text{i}',
    } for i in range(15)
]

ANSWERS = [
    {
        'id': i,
        'rating' : i,
        'tag' : TAGS[0],
        'text': f'Text{i}',
    } for i in range(15)
]