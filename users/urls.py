from django.urls import path
from .views import register
from blogs.views import posts_list
urlpatterns = [
	path('', posts_list),
	path('register/', register, name='register'),
]
