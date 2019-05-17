from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=90)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subcontent = models.TextField(default='')
    content = models.TextField(default='')
    slug = models.CharField(max_length=60, default='')
    post_id = models.IntegerField(default=None, unique=True)
    date = models.DateTimeField(auto_now=True)
    comment_cnt = models.IntegerField(default=0)
    image = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def get_comments(self):
        return self.comments.filter(parent=None).order_by('-date')

    def get_absolute_url(self):
        return reverse('post', kwargs={
            'slug': self.slug,
            'post_id': self.post_id
        })


class Comment(models.Model):
    likes = models.ManyToManyField(User, default=1, blank=True, related_name='comment_likes')
    dislikes = models.ManyToManyField(User, default=1, blank=True, related_name='comment_dislikes')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(
        'Post', related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='replies', on_delete=models.CASCADE)
