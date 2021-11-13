from django.db import models
from django.contrib.auth.models import User
import os
from markdownx.models import MarkdownxField
from markdownx.utils import markdown


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/project/tag/{self.slug}/'


class Post(models.Model):
    head_image= models.ImageField(upload_to='project/images/%Y/%m/%d/')
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length= 300,blank=True)
    pin = models.BooleanField(default=False);
    content = MarkdownxField()
    author = models.ForeignKey(User, related_name='project_post_author', on_delete=models.CASCADE)
    file_upload = models.FileField(upload_to='project/files/%Y/%m/%d/', blank=True)
    related_link = models.URLField(blank=True)
    github_link = models.URLField(blank=True)
    video_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/project/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

    def get_content_markdown(self):
        return markdown(self.content)

    def get_github_link(self):
        return str(self.github_link)

    def get_video_link(self):
        return str(self.video_link)
    def get_related_link(self):
        return str(self.related_link)



# Create your models here
