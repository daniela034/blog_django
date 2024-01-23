from django.shortcuts import render
from django.core.paginator import Paginator 
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404

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
            'page_title' : 'Home - ',
        }
    )
    
def created_by(request,id):
    user = User.objects.filter(pk=id).first()
    
    if user == None:
       raise Http404() 
    
    posts = Post.objects.get_published().filter(created_by__pk=id) # type: ignore
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    user_full_name = user.username
    if user.first_name: 
        user_full_name = f'{user.first_name} {user.last_name}'
        
    page_title = user_full_name + ' posts -'

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title' : page_title,
        }
    )

def category(request,slug):
    posts = Post.objects.get_published().filter(category__slug=slug) # type: ignore
    
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    if len(page_obj) == 0: 
        raise Http404()
    
    page_title = f'{page_obj[0].category.name} - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title' : page_title,
        }
    )

def page(request,slug):
    page = Page.objects.filter(is_published=True).filter(slug=slug).first() # type: ignore

    if page is None: 
        raise Http404()
    
    page_title = f'{page.title} - '
    
    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page,
            'page_title' : page_title,
        }
    )


def post(request, slug):
    post = Post.objects.get_published().filter(slug=slug).first() # type: ignore
    
    if post is None: 
        raise Http404()
    
    page_title = f'{post.title} - '
    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post,
            'page_title' : page_title,
        }
    )
    
def tag(request,slug):
    posts = Post.objects.get_published().filter(tags__slug=slug) # type: ignore
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0: 
        raise Http404()
    
    page_title = f'{page_obj[0].tags.first().name} - '
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title' : page_title,
        }
    )
    
    
def search(request):
    search_value = request.GET.get('search', '').strip()
     # title have search value or excerpt have search value
     # or content have search value
     # Q -> using pipe | for the or 
    posts = (Post.objects.get_published() .filter(Q(title__icontains=search_value) | Q(excerpt__icontains=search_value) |Q(content__icontains=search_value)) )[0:PER_PAGE] #type:ignore
    
    page_title = f'{search_value[:10]} - '
    
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value' : search_value,
            'page_title' : page_title,
        }
    )