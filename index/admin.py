from django.contrib import admin
from .models import *
admin.site.site_title = 'Song qi chen bookstore'
admin.site.site_header = 'Book Store'

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ['label_id', 'label_name']
    search_fields = ['label_name']
    ordering = ['label_id']

@admin.register(Dynamic)
class DynamicAdmin(admin.ModelAdmin):
    list_display = ['dynamic_id','book','dynamic_views','dynamic_search','dynamic_down']
    search_fields = ['book']
    list_filter = ['dynamic_views','dynamic_search','dynamic_down']
    ordering = ['dynamic_id']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment_id','comment_text','comment_user','book','comment_date']
    search_fields = ['comment_user','book','comment_date']
    list_filter = ['book','comment_date']
    ordering = ['comment_id']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['book_id','book_name','book_price','book_bookstock']
    search_fields = ['book_name','book_bookstock','book_pubdate']
    list_filter = ['book_id','book_pubdate']
    ordering = ['book_pubdate']


