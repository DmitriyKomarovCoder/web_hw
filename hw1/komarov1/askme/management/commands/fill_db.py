from django.core.management.base import BaseCommand
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from random import choice, random, sample
from askme.models import Profile, Question, Answer, Tag, LikeQuestion, LikeAnswer


class Command(BaseCommand):
    help = 'Fill database with sample data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Number of entities to create for each user')

    def handle(self, *args, **options):
        ratio = options['ratio']

        profiles = []
        for i in range(1, ratio + 1):
            user = User.objects.create(username=f'user{i}')
            profile = Profile.objects.create(user=user, name=f'User {i}', avatar='default-avatar.png')
            profiles.append(profile)

        tags = [Tag(name=f'Tag {i}') for i in range(1, ratio+1)]
        Tag.objects.bulk_create(tags)

        questions = []
        for i in range(1, ratio * 10 + 1):
            question = Question(title=f'Title {i}', text=f'Text {i}', author=choice(profiles))
            question.save()
            question.tag.add(*sample(tags, len(tags)))
            questions.append(question)

        answers = []
        for i in range(1, ratio * 100 + 1):
            answer = Answer(author=choice(profiles), text=f'Text {i}', question=choice(questions))
            answer.save()
            answers.append(answer)

        like_questions = []
        for profile in profiles:
            for question in questions:
                like_question, created = LikeQuestion.objects.get_or_create(
                    user=profile, question=question,
                    defaults={'user': profile, 'question': question}
                )
                if created:
                    like_questions.append(like_question)

        LikeQuestion.objects.bulk_create(like_questions)

        like_answers = []
        for profile in profiles:
            for answer in answers:
                like_answer, created = LikeAnswer.objects.get_or_create(
                    user=profile, answer=answer,
                    defaults={'user': profile, 'answer': answer}
                )
                if created:
                    like_answers.append(like_answer)

        LikeAnswer.objects.bulk_create(like_answers)

        self.stdout.write(self.style.SUCCESS(f'Successfully added {ratio} users, {len(questions)} questions, {len(answers)} answers, {len(tags)} tags, {len(like_questions + like_answers)} likes'))