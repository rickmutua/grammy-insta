from .models import Profile, Post, Comment
from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):

    class Meta:

        model = User

        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = ('bio', 'gender')


class PostForm(forms.ModelForm):

    class Meta:

        model = Post

        fields = ('image', 'caption')


class ProfPicForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = ('profpic',)


class CommentForm(forms.ModelForm):

    class Meta:

        model = Comment

        fields = ('content',)