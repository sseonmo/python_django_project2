from django.urls import path
from .views import posts_list

urlpatterns = [
	path('post/', posts_list, name='posts_list')
]