from django import forms
from .models import BlogPost, Comment, Reply
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirm Password')

    class Meta:
        model = User
        fields = ['username']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1!= password2:
            raise forms.ValidationError('Passwords must match')
        return password2

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        if user:
           user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user    


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='username')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='password')

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
