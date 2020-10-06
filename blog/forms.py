from django import forms
from .models import BlogComment, Profile, Blog, Excerpt
from django.contrib.auth.models import User


class PostUpload(forms.ModelForm):
    class Meta:
        model = Blog

        exclude = ['time_to_read', 'slug', 'user', 'views']


class PostEdit(forms.ModelForm):
    class Meta:
        model = Blog

        exclude = ['time_to_read', 'slug', 'user', 'views']


class CommentForm(forms.ModelForm):
    comment = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control',
                                                                     'placeholder': 'Reply '
                                                                                    'here!', 'rows': 2, 'cols': 50}))

    class Meta:
        model = BlogComment
        fields = ["comment"]


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User

        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Profile

        fields = ['dob', 'about', 'photo']


class ExcerptForm(forms.ModelForm):
    excerpt = forms.CharField(required=False)

    class Meta:
        model = Excerpt

        fields = ['excerpt']
