"""Defines URL pattern for blogs."""

from django.urls import path
from . import views

app_name = 'blogs'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page for adding a new blog post.
    path('new_post/', views.new_post, name='new_post'),
    # Page for editing a blog post.
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    # Page for deleting a blog post.
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    # Particular post's comment section.
    path('comments/<int:post_id>/', views.comments, name='comments'),
    # Page for commenting on a blog post.
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    # Page for deleting a comment.
    path('delete_comment/<int:comment_id>/', views.delete_comment,
     name='delete_comment'),
]
