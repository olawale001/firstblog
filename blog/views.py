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
    



