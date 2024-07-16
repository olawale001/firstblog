from django import forms
from .models import BlogPost, Comment, Reply


class PostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply']
