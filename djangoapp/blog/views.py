from django.shortcuts import render
from django.core.paginator import Paginator 
from blog.models import Post

PER_PAGE = 9

# Create your views here.
def index(request):
    posts = Post.objects.get_published() # type: ignore
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )
    
def created_by(request,id):
    posts = Post.objects.get_published().filter(created_by__pk=id) # type: ignore
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )

def category(request,slug):
    posts = Post.objects.get_published().filter(category__slug=slug) # type: ignore
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )

def page(request,slug):

    return render(
        request,
        'blog/pages/page.html',
        {
            # 'page_obj': page_obj,
        }
    )


def post(request, slug):
    post = Post.objects.get_published().filter(slug=slug).first() # type: ignore
    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post,
        }
    )