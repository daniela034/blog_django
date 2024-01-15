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
    
        