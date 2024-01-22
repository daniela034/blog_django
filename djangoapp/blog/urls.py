from blog.views import index, post, page, created_by, category
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('page/<slug:slug>/', page, name='page'),
    path('post/<slug:slug>/', post, name='post'),
    path('created_by/<int:id>/', created_by, name='created_by'),
    path('category/<slug:slug>/', category, name='category'),

]