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
            profile = Profile(user=user, name=f'User {i}', avatar='default-avatar.png')
            profiles.append(profile)
        Profile.objects.bulk_create(profiles)

        tags = [Tag(name=f'Tag {i}') for i in range(1, ratio+1)]
        Tag.objects.bulk_create(tags)

        questions = []
        for i in range(1, ratio * 10 + 1):
            question = Question(title=f'Title {i}', text=f'Text {i}', author=choice(profiles))
            question.save()
            question.tag.add(*sample(tags, 3))
            questions.append(question)

        answers = []
        for i in range(1, ratio * 100 + 1):
            answer = Answer(author=choice(profiles), text=f'Text {i}', question=choice(questions))
            answers.append(answer)
        Answer.objects.bulk_create(answers)

        #like_questions = [LikeQuestion(user=profile, question=question, estimation=choice([True, False]))
        #                  for profile in profiles for question in questions]
        #LikeQuestion.objects.bulk_create(like_questions)

        #like_answers = [LikeAnswer(user=profile, answer=answer, estimation=choice([True, False]))
        #                for profile in profiles for answer in answers]
        #LikeAnswer.objects.bulk_create(like_answers)

        like_questions = []
        for profile in profiles:
            for question in questions:
                if len(like_questions) >= ratio * 100:
                    break
                like_questions.append(LikeQuestion(user=profile, question=question, estimation=choice([True, False])))

        LikeQuestion.objects.bulk_create(like_questions)

        like_answers = []
        for profile in profiles:
            for answer in answers:
                if len(like_answers) >= ratio * 100:
                    break
                like_answers.append(LikeAnswer(user=profile, answer=answer, estimation=choice([True, False])))

        LikeAnswer.objects.bulk_create(like_answers)
        self.stdout.write(self.style.SUCCESS(f'Successfully added {ratio} users, {len(questions)} questions, {len(answers)} answers, {len(tags)} tags, {len(like_questions + like_answers)} likes'))
