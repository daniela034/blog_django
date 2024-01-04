from django.contrib import admin
from django.http.request import HttpRequest
from site_setup.models import MenuLink, SiteSetup

# Register your models here.

#podemos comentar isto e apenas trabalhamos com o menulinkinline e sitesetup
#@admin.register(MenuLink)
#class MenuLinkAdmin(admin.ModelAdmin): 
#    list_display = 'id', 'text', 'url_or_path',
#    list_display_links = 'id', 'text', 'url_or_path',
#    search_fields = 'id', 'text', 'url_or_path',
    
# queremos criar um inline que dentro do sitesetup vão aparecer os campos dos menulinks 
class MenuLinkInline(admin.TabularInline): 
    model = MenuLink
    extra = 1     
    
@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin): 
    list_display = 'title', 'description', 
    inlines = MenuLinkInline, 
    
    #impedir que ao criar um registo, o user não possa criar mais nenhum 
    # este método já existe, se retornarmos true o Adicionar aparece, se for false não aparece
    def has_add_permission(self, request) :
        return not SiteSetup.objects.exists()