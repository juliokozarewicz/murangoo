from django.contrib import admin
from .models import Post


@admin.register(Post)

class Post_admin(admin.ModelAdmin):

    exclude = ('author',)

    list_display = ('title', 'published','author', 'status')

    search_fields = ('title', 'content')
    
    list_filter = ('status', 'published')

    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

