from django.shortcuts import render
from .models import Post
# Create your views here.

def posts_list(request):
	posts = Post.objects.order_by('-create_at')
	return render(request, 'blogs/posts_list.html', context={'posts': posts})
