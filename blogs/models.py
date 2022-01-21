from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    """A text post."""
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=2500)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """Return a string representation of the model."""
        return self.title

class Comment(models.Model):
    """A comment on a post."""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """Return a string representation of the model."""
        return self.text[:100]