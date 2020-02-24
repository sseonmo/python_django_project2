from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'user', 'create_at')


class CommentAdmin(admin.ModelAdmin):
	list_display = ('content', 'post', 'user')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
