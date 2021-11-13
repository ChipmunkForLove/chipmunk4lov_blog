from django.shortcuts import render
from blog.models import Post


# Create your views here.
def landing(request):
    recent_posts = Post.objects.order_by('-pk')[:3]
    for i in recent_posts:
        i.created_at = i.created_at.strftime("%b %d, %Y")

    return render(
        request,
        'landing_page/landing.html',
        {'recent_posts': recent_posts,}
    )


