from typing import Any
from django.db.models.query import QuerySet

from django.shortcuts import render, redirect
from django.core.paginator import Paginator 
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest
from django.views.generic import ListView

PER_PAGE = 9

#class based view for the function based views index
# how to make the same thing 
class PostListView(ListView):
    model = Post
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    ordering = '-pk',
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published() # type: ignore 
    
    # example of an method that show us only the is_published posts in the index
    # def get_queryset(self): 
    #   queryset = super().get_queryset()
    #   queryset = queryset.filter(is_published=True)
    #   return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context.update({
            'page_title' : 'Home - ',
        })
        return context 
    

#def index(request):
#    posts = Post.objects.get_published() # type: ignore
#    paginator = Paginator(posts, PER_PAGE)
#    page_number = request.GET.get("page")
#    page_obj = paginator.get_page(page_number)

#    return render(
#        request,
#        'blog/pages/index.html',
#        {
#            'page_obj': page_obj,
#            'page_title' : 'Home - ',
#        }
#    )
 

# we will reuse some of the things of the PostListView so the new class based view for 
# the created by is going to be based on this class 
class CreatedByListView(PostListView): 
    # edit init for define a temporary context
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}
        
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self._temp_context['user']
        user_full_name = user.username
        if user.first_name: 
            user_full_name = f'{user.first_name} {user.last_name}'
        
        page_title = user_full_name + ' posts -'
        
        ctx.update({
            'page_title' : page_title,
        })
        
        return ctx
    
    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context['user'].pk)
        return qs
    
    def get(self, request, *args, **kwargs):
        
        id = self.kwargs.get('id')
        user = User.objects.filter(pk=id).first()
    
        if user == None:
            raise Http404() 
        
        self._temp_context.update({
            'id' : id, 
            'user' : user,
        })
        
        return super().get(request, *args, **kwargs)
    
#def created_by(request,id):
#    user = User.objects.filter(pk=id).first()
    
#    if user == None:
#       raise Http404() 
    
#    posts = Post.objects.get_published().filter(created_by__pk=id) # type: ignore
#    paginator = Paginator(posts, PER_PAGE)
#    page_number = request.GET.get("page")
#    page_obj = paginator.get_page(page_number)
    
#    user_full_name = user.username
#    if user.first_name: 
#        user_full_name = f'{user.first_name} {user.last_name}'
        
#    page_title = user_full_name + ' posts -'

#    return render(
#        request,
#        'blog/pages/index.html',
#        {
#            'page_obj': page_obj,
#            'page_title' : page_title,
#        }
#    )

class CategoryListView(PostListView):
    allow_empty = False # error HTTP404
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('slug')
        )
        
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = f'{self.object_list[0].category.name} - ' # type: ignore
        ctx.update({
            'page_title': page_title,
        })
        
        return ctx
    
    
    
#def category(request,slug):
#    posts = Post.objects.get_published().filter(category__slug=slug) # type: ignore
    
#    paginator = Paginator(posts, PER_PAGE)
#    page_number = request.GET.get("page")
#    page_obj = paginator.get_page(page_number)
    
#    if len(page_obj) == 0: 
#        raise Http404()
    
#    page_title = f'{page_obj[0].category.name} - '

#    return render(
#        request,
#        'blog/pages/index.html',
#        {
#            'page_obj': page_obj,
#            'page_title' : page_title,
#        }
#    )

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
    
class TagListView(PostListView):
    allow_empty = False # error HTTP404
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            tags__slug=self.kwargs.get('slug')
        )
        
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = f'{self.object_list[0].tags.first().name} - ' # type: ignore
        ctx.update({
            'page_title': page_title,
        })
        
        return ctx
    
#def tag(request,slug):
#    posts = Post.objects.get_published().filter(tags__slug=slug) # type: ignore
#    paginator = Paginator(posts, PER_PAGE)
#    page_number = request.GET.get("page")
#    page_obj = paginator.get_page(page_number)

#    if len(page_obj) == 0: 
#        raise Http404()
    
#    page_title = f'{page_obj[0].tags.first().name} - '
#    return render(
#        request,
#        'blog/pages/index.html',
#        {
#            'page_obj': page_obj,
#            'page_title' : page_title,
#        }
#    )

class SearchListView(PostListView):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._search_value = ''
        
    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)
    
    def get_queryset(self):
        return super().get_queryset().filter(Q(title__icontains=self._search_value) | Q(excerpt__icontains=self._search_value) |Q(content__icontains=self._search_value))[0:PER_PAGE]
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'search_value' : self._search_value,
            'page_title' : f'{self._search_value[:10]} - ',
        })
        return ctx
    
    def get(self, request, *args, **kwargs):
        if self._search_value=='':
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)
         
    
#def search(request):
#    search_value = request.GET.get('search', '').strip()
     # title have search value or excerpt have search value
     # or content have search value
     # Q -> using pipe | for the or 
#    posts = (Post.objects.get_published().filter(Q(title__icontains=search_value) | Q(excerpt__icontains=search_value) |Q(content__icontains=search_value)) )[0:PER_PAGE] #type:ignore
    
#    page_title = f'{search_value[:10]} - '
    
#    return render(
#        request,
#        'blog/pages/index.html',
#        {
#            'page_obj': posts,
#            'search_value' : search_value,
#            'page_title' : page_title,
#        }
#    )