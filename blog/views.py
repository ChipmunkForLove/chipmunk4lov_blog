from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView,CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post,Tag,Comment,Category
from django.core.exceptions import PermissionDenied
from .forms import CommentForm
from django.shortcuts import get_object_or_404


class CommentUpdate(LoginRequiredMixin,UpdateView):
    model= Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request,*args,**kwargs)
        else:
            raise PermissionDenied

class PostList(ListView):
    model = Post
    template_name = 'blog/index.html'
    ordering = '-pk'
    def get_context_data(self, *, object_list=None, **kwargs):
        parent_list = Category.objects.filter(parent=None)
        post_cnt_list = [];
        categories_list = Category.objects.all()
        for c in Category.objects.all():
            if (c.parent == None):
                length = len(Post.objects.filter(category__parent=c))
                post_cnt_list.append(length)
            else:
                post_cnt_list.append(0)

        categories = zip(categories_list, post_cnt_list)

        context=super(PostList,self).get_context_data()
        context['categories'] = categories
        context['all_post'] = len(Post.objects.all())

        return context

class PostDetail(DetailView):
    model= Post


    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['comment_form'] = CommentForm
        return context


class PostCreate(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','hook_text','content','file_upload']

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(PostCreate,self).form_valid(form)
        else:
            return redirect('/blog/')

class PostUpdate(LoginRequiredMixin,UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'file_upload']
    template_name = 'blog/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author :
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)

        else:
            raise PermissionDenied


def new_comment(request,pk):
    if request.user.is_authenticated:
        post= get_object_or_404(Post,pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied

def delete_comment(request, pk):
    comment = get_object_or_404(Comment,pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied

def show_category(request,slug):
    slug_list = slug.split("|")
    parent=None
    category=None

    parent_list = Category.objects.filter(parent=None)
    post_cnt_list=[];
    categories_list = Category.objects.all()
    for c in Category.objects.all():
        if(c.parent==None):
           post_cnt_list.append(len(Post.objects.filter(category__parent=c)))
        else:
            post_cnt_list.append(0)

    if len(slug_list) == 2 :
        category = Category.objects.filter(slug=slug_list[-1])
        category = list(category)
    elif len(slug_list) ==1:
        parent = get_object_or_404(Category,slug=slug,parent=None)
        category = list(parent.children.all())

    categories = zip(categories_list,post_cnt_list)

    return render(
        request,
        "blog/index.html",
        {
            'all_post' : len(Post.objects.all()),
            'post_list': Post.objects.filter(category__in=category),
            'categories': categories,
            'category':category,
        }
    )

