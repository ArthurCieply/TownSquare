from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import BlogPost, Comment 
from .forms import BlogPostForm, CommentForm


def check_post_owner(owner, request):
    """Confirm user associated with post matches user trying to access it."""
    if owner != request.user:
        raise Http404

def check_comment_owner(owner, request):
    """Confirm user who made comment matches user trying to delete it."""
    if owner != request.user:
        raise Http404

def index(request):
    """
    The home page for blog.
    Displays all post in chronological order.
    """
    blogposts = BlogPost.objects.order_by('-date_added')
    context = {'blogposts': blogposts}
    return render(request, 'blogs/index.html', context)

@login_required
def new_post(request):
    """Add a new blog post."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = BlogPostForm()
    else:
        # POST data submitted; process data.
        form = BlogPostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            form.save()
            return redirect('blogs:index')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)

@login_required
def edit_post(request, post_id):
    """Edit an existing blog post."""
    post = BlogPost.objects.get(id=post_id)
    text = post.text 
    title = post.title
    check_post_owner(post.owner, request)

    if request.method != 'POST':
        # Initial request: pre-fill with the current post.
        form = BlogPostForm(instance=post)
    else:
        # POST data submitted; process data.
        form = BlogPostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:index')

    context = {'post': post, 'form': form, 'text': text, 'title': title}
    return render(request, 'blogs/edit_post.html', context)

@login_required
def delete_post(request, post_id):
    """Delete an existing post."""
    post = BlogPost.objects.get(id=post_id)
    text = post.text
    title = post.title
    check_post_owner(post.owner, request)

    if request.method != 'POST':            # Initial request
        form = BlogPostForm(instance=post)  # Pre-fill with entry to be deleted.
    else:
        form = BlogPostForm(instance=post, data=request.POST)
        if request.POST.get("delete"):      # Confirmed
            post.delete()                  # Delete entry
            return redirect('blogs:index')  # Redirect to index

    context = {'post': post, 'text': text, 'title': title, 'form': form}
    return render(request, 'blogs/delete_post.html', context)

def comments(request, post_id):
    """Comment section of a particular post."""
    post = BlogPost.objects.get(id=post_id)
    text = post.text 
    title = post.title
    comments = post.comment_set.order_by('-date_added')

    context = {'post': post, 'text': text, 'title': title, 'comments': comments}
    return render(request, 'blogs/comments.html', context) 

@login_required
def add_comment(request, post_id):
    """Add a comment on a specific post."""
    post = BlogPost.objects.get(id=post_id)

    if request.method != 'POST':    # Initial request
        form = CommentForm()        # Create blank form
    else:                                       # Post data submitted
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.owner = request.user
            new_comment.post = post
            new_comment.save()
            return redirect('blogs:comments', post_id=post_id)

    # Display a blank or invalid comment form.
    context = {'post': post, 'form': form}
    return render(request, 'blogs/add_comment.html', context)

@login_required
def delete_comment(request, comment_id):
    """Delete an existing comment."""
    comment = Comment.objects.get(id=comment_id)
    post = comment.post
    check_comment_owner(comment.owner, request)

    if request.method != 'POST':                # Initial request
        form = CommentForm(instance=comment)    # Pre-fill with comment to be deleted
    else:
        form = CommentForm(instance=comment, data=request.POST)
        if request.POST.get("submit"):          # Confirmed
            comment.delete()                    # Delete comment
            return redirect('blogs:comments', post_id=post.id)  # Redirect to comments page

    context = {'comment': comment, 'form': form, 'post': post}
    return render(request, 'blogs/delete_comment.html', context)

