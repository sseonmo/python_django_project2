from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'user', 'create_at')

admin.site.register(Post, PostAdmin)
