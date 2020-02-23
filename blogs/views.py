from django.shortcuts import render, redirect, reverse, get_object_or_404, resolve_url
from .models import Post
from django.contrib.auth.decorators import login_required

# Create your views here.

def posts_list(request):
	posts = Post.objects.order_by('-create_at')
	return render(request, 'blogs/posts_list.html', context={'posts': posts})

def post_detail(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	# post = Post.objects.filter(pk=post_id)
	return render(request, 'blogs/posts_detail.html', context={'post': post})

# @login_required
def post_write(request):
	errors = []

	if request.method == 'POST':
		title = request.POST.get('title', '').strip()
		content = request.POST.get('content', '').strip()
		image = request.FILES.get('image')

		if not title:
			errors.append('제목을 입려해주세요')
		elif not content:
			errors.append('내용을 입려해주세요')

		if not errors:
			post = Post.objects.create(user=request.user, title=title, content=content, image=image)
			# return redirect(reverse('post_detail', kwargs={'post_id': post.id}))
			return redirect(resolve_url('post_detail', post_id=post.id))

	return render(request, 'blogs/posts_write.html', {'user': request.user, 'errors': errors})

"""
from django.shortcuts import get_object_or_404

example)
q = get_object_or_404(Question, pk=id)
- 첫번째 모델, 두번재 키워드, 만약 키워드가 없으면 404 에러를 발생

-- reverse, redirect 
참조 - https://wayhome25.github.io/django/2017/05/05/django-url-reverse/
"""
