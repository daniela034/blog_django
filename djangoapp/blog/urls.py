from blog.views import PostDetailView, PageDetailView, PostListView, CreatedByListView, CategoryListView, TagListView, SearchListView
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('page/<slug:slug>/', PageDetailView.as_view(), name='page'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post'),
    path('created_by/<int:id>/', CreatedByListView.as_view(), name='created_by'),
    path('category/<slug:slug>/', CategoryListView.as_view(), name='category'),
    path('tag/<slug:slug>/', TagListView.as_view(), name='tag'),
    path('search/', SearchListView.as_view(), name='search'),

]