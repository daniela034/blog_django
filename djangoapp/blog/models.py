from django.db import models
from utils import rands
from django.contrib.auth.models import User
from utils.images import resize_image


# Create your models here.
class Tag(models.Model):
    class Meta:
        verbose_name ='Tag'
        verbose_name_plural = 'Tags'
        
    name = models.CharField(max_length = 255)
    # slug -> texto que vai representar a tag na url (como se fosse o id da tag)
    slug = models.SlugField(unique=True, default = None, null=True, blank=True,
                            max_length=255)
    
    def save(self, *args, **kwargs): 
        if not self.slug: 
            self.slug = rands.new_slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    

class Category(models.Model):
    class Meta:
        verbose_name ='Category'
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length = 255)
    # slug -> texto que vai representar a tag na url (como se fosse o id da tag)
    slug = models.SlugField(unique=True, default = None, null=True, blank=True,
                            max_length=255)
    
    def save(self, *args, **kwargs): 
        if not self.slug: 
            self.slug = rands.new_slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
        
        
        
class Page(models.Model): 
    class Meta:
        verbose_name ='Page'
        verbose_name_plural = 'Pages'
        
    title = models.CharField(max_length=65,)
    slug = models.SlugField(unique=True, default = None, null=True, blank=True,
                            max_length=255)
    is_published = models.BooleanField(default=False)
    content = models.TextField()
    
    def save(self, *args, **kwargs): 
        if not self.slug: 
            self.slug = rands.new_slugify(self.title)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    

class Post(models.Model): 
    class Meta:
        verbose_name ='Post'
        verbose_name_plural = 'Posts'
        
    title = models.CharField(max_length=65,)
    slug = models.SlugField(unique=True, default = None, null=True, blank=True,
                            max_length=255)
    # resumo do nosso post
    excerpt = models.CharField(max_length=150,)
    
    is_published = models.BooleanField(default=False)
    content = models.TextField()
    cover = models.ImageField(upload_to='posts/%Y/%m', blank=True, default='')
    cover_in_post_content = models.BooleanField(
        default=True,
        help_text='show the cover image inside the content')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # category - pode ter muitos posts na mesma categoria 
    #   categoria é pai do post 
    #   no caso do menu link é ao contrario (é o filho)
    # neste caso precisamos de ter uma categoria para criarmos um post
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, null=True, blank=True, default=None,
    )
    # tag a relação é diferente 
    # 1 post pode ter varias tags e vice-versa
    tags = models.ManyToManyField(Tag, blank=True,default='')
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='post_created_by'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='post_updated_by'
    )
    
    
    def save(self, *args, **kwargs): 
        if not self.slug: 
            self.slug = rands.new_slugify(self.title)
            
        current_cover_name = str(self.cover.name)
        super_save =super().save(*args, **kwargs)
        cover_changed = False

        if self.cover:
            cover_changed = current_cover_name != self.cover.name

        if cover_changed:
            resize_image(self.cover, 900)
            
        return super_save
    
    def __str__(self):
        return self.title