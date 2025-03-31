from django.contrib import admin
from contact import models
# Register your models here.
@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = 'id','first_name','last_name','phone','email','show','picture','category',
    ordering = '-id',
    search_fields = 'first_name',
    list_display_links = 'first_name','last_name',


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = 'name',


