from django import forms
from .models import Profile, Answer, Question, Tag
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)
    next = forms.CharField(widget = forms.HiddenInput(), required = False)

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ["username", "name", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_check = cleaned_data.get('password_check')
        username = cleaned_data.get('username')

        if password != password_check:
            raise forms.ValidationError("Passwords do not match.")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")

        return cleaned_data

    def save(self, commit=True):
        self.cleaned_data.pop('password_check')
        user = User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        profile = Profile.objects.create(user=user, name=self.cleaned_data['name'])
        return profile

class AnswerForm(forms.ModelForm):
    text = forms.CharField(max_length=500, widget=forms.Textarea)
    class Meta:
        model = Answer
        fields = ["text"]

    def save(self, profile, question):
        super().clean()
        new_answer = Answer.objects.create(author=profile, question=question, text=self.cleaned_data['text'])
        return new_answer

class QuestionForm(forms.ModelForm):
    title = forms.CharField(max_length=50)
    text = forms.CharField(max_length=500, widget=forms.Textarea)
    tags = forms.CharField(required=False)
    tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    def save(self, profile):
        super().clean()
        tags_names = []
        if self.cleaned_data['tags']:
            tags_names.extend(self.cleaned_data['tags'].split(','))
        if self.cleaned_data['tag']:
            tags_names.extend([tag.name for tag in self.cleaned_data['tag']])

        tags = []
        for tag_name in tags_names:
            if Tag.objects.filter(name=tag_name).exists():
                tags.append(Tag.objects.get(name=tag_name))
            else:
                new_tag = Tag(name=tag_name)
                new_tag.save()
                tags.append(new_tag)

        new_question = Question.objects.create(author=profile,
                                        title=self.cleaned_data['title'],
                                        text=self.cleaned_data['text'])
        new_question.tag.set(tags)
        return new_question

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags', 'tag']

class SettingsForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ["username", "last_name", "first_name", "avatar"]

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        #self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your name'
        #self.fields['avatar'].widget.attrs['placeholder'] = 'Choose your avatar'

    def save(self, commit=True):
        user = super().save(commit)

        profile = user.profile
        profile.avatar = self.cleaned_data['avatar']
        profile.save()
        return user