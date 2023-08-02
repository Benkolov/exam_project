from django import forms
from .models import Comment
from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(label='Search', max_length=255)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
