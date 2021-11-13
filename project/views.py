from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView,CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post,Tag
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

class PostList(ListView):
    model = Post
    template_name = 'project/project_list.html'
    ordering = '-pk'


class PostDetail(DetailView):
    model= Post



