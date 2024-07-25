from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, Comment, Reply
from .forms import PostForm, CommentForm, ReplyForm, SignupForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout as auth_logout


def sign_up(req):
    if req.method == 'POST':
        form = SignupForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            # if user is not None:
            login(req, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(req, 'registration/signup.html', {'form': form})


def login_view(req):
    if req.method == 'POST':
        form = UserLoginForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(req, username=username, password=password)
            if user is not None:
                login(req, user)
                return redirect('home')
    else:
        form = UserLoginForm()
    return render(req, 'registration/login.html', {'form': form})



def logout_user(req):
    auth_logout(req)
    return redirect('login')  


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


@login_required
def post_edit(req, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if req.method == 'POST':
        form = PostForm(req.POST, req.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = req.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(req, 'blog/post_edit.html', {'form': form})


@login_required
def post_delete(req, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.delete()
    return redirect('home')


@login_required
def comment_delete(req, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if req.method == 'POST':
        comment.delete()
    return redirect('post_detail', comment.post.pk)

@login_required
def reply_delete(req, reply_pk):
    reply = get_object_or_404(Reply, pk=reply_pk)
    if req.method == 'POST':
        reply.delete()
    return redirect('post_detail', pk=reply.comment.post.pk)

@login_required
def add_comment(req, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if req.method == 'POST':
        form = CommentForm(req.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = req.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(req, 'blog/add_comment.html', {'form': form, 'post': post})


def add_reply(req, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if req.method == 'POST':
        form = ReplyForm(req.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.author = req.user
            reply.save()
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = ReplyForm()
    return render(req, 'blog/add_reply.html', {'form': form, 'comment': comment})
    



