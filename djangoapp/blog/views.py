from django.shortcuts import render
from django.core.paginator import Paginator 
from blog.models import Post
from django.db.models import Q

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
    
def tag(request,slug):
    posts = Post.objects.get_published().filter(tags__slug=slug) # type: ignore
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
    
    
def search(request):
    search_value = request.GET.get('search', '').strip()
     # title have search value or excerpt have search value
     # or content have search value
     # Q -> using pipe | for the or 
    posts = (Post.objects.get_published() .filter(Q(title__icontains=search_value) | Q(excerpt__icontains=search_value) |Q(content__icontains=search_value)) )[0:PER_PAGE] #type:ignore


    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value' : search_value,
        }
    )