from django.db import models
from utils import rands

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