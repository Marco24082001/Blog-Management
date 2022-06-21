from django.db import models

# Create your models here.

from pyexpat import model
from unicodedata import category
from venv import create
from django.db import models
from django.utils.text import slugify
from user_profile.models import User
from .slugs import generate_unique_slug
from ckeditor.fields import RichTextField
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Tag(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(null=True, blank=True)
    created_date = models.DateField(auto_now_add = True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    

class Blog(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user_blogs',
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        related_name='category_blogs',
        on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tag_blogs',
        blank=True
    )
    likes = models.ManyToManyField(
            User,
            related_name='user_likes',
            blank=True
        )
    title = models.CharField(
        max_length=250
    )
    slug = models.SlugField(null = True, blank=True)
    banner = models.ImageField(upload_to = 'blog_banner')
    description = RichTextField()
    view = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.slug = generate_unique_slug(self, self.title)
            super().save(*args, **kwargs)
        super().save(*args, **kwargs)

class Comment(models.Model):
    user = models.ForeignKey(
            User,
            related_name = 'user_comments',
            on_delete = models.CASCADE
        )
    blog = models.ForeignKey(
                Blog,
                related_name = 'blog_comments',
                on_delete=models.CASCADE
            )
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.text
    
class Reply(models.Model):
    user = models.ForeignKey(
            User,
            related_name = 'user_replies',
            on_delete = models.CASCADE
        )
    comment = models.ForeignKey(
                Comment,
                related_name = 'comment_replies',
                on_delete=models.CASCADE
            )
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.text
    

class CateReport(models.Model):
    name = models.CharField(max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default= 1)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    category = models.ForeignKey(CateReport, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.blog.title