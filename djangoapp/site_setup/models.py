from django.db import models

# Create your models here.
# menu link vai aparecer na area administrativa 

class MenuLink(models.Model):
    class Meta:
        verbose_name = 'Menu Link'
        verbose_name_plural = 'Menu Links'

    # campos que vamos ter 
    text = models.CharField(max_length=50)
    # tem um metodo url 
    # no entanto vai ser usado o charfield para podermos usar os caminhos : / ou /blog ou /blog/1
    # pode colocar o target : #1 
    # pode colocar uma url : https://cenas 
    url_or_path = models.CharField(max_length=2048)
    #new tab-> para saber se vai abrir o url num nova tab ou nao 
    new_tab = models.BooleanField(default=False)
    # foreign key - 1 sitesetup pode ter muitos menu links 
    #   colocamos aqui porque o pai é o sitesetup e o menulink é que vai guardar todas as infos dele 
    site_setup = models.ForeignKey(
        'SiteSetup', 
        on_delete = models.CASCADE, 
        blank = True, 
        null = True, 
        default = None
    )

    def __str__(self):
        return self.text
    
    
class SiteSetup(models.Model): 
    class Meta: 
        verbose_name = 'Setup'
        verbose_name_plural = 'Setup'
        
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=255)
    show_header = models.BooleanField(default=True)
    show_search = models.BooleanField(default=True)
    show_menu = models.BooleanField(default=True)
    show_description = models.BooleanField(default=True)
    show_pagination = models.BooleanField(default=True)
    show_footer = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title