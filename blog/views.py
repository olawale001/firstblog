from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, Comment, Reply
from .forms import PostForm, CommentForm, ReplyForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


def sign_up(req):
    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(req, 'registration/signup.html', {'form': form})

def home(req):
    posts = BlogPost.objects.all()
    return render(req, 'blog/index.html', {'posts': posts})


def post_detail(req, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = Comment.objects.filter(post=post)
    if req.method == 'POST':
        comment_form = CommentForm(req.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    return render(req, 'blog/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})


@login_required
def post_new(req):
    if req.method == 'POST':
        form = PostForm(req.POST, req.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = req.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(req, 'blog/post_edit.html', {'form': form})