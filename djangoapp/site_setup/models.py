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

    def __str__(self):
        return self.text