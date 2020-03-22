from django.db import models
from helpers.models import BaseModel
from users.models import User
from django.conf import settings
import os
from taggit.managers import TaggableManager

# Create your models here.
class Post(BaseModel):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=255, blank=False, verbose_name='타이틀')
	content = models.TextField(verbose_name='내용')
	image = models.ImageField(blank=True, null=True, verbose_name='이미지', upload_to='%Y/%m/%d')
	likes = models.ManyToManyField(User, related_name='likes', blank=True)
	tags = TaggableManager()

	# delete 오버라이딩
	def delete(self, *args, **kargs):
		os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
		# 원래의 delete 함수를 실행
		super(Post, self).delete(*args, **kargs)

	def total_likes(self):
		return self.likes.count()

	def __str__(self):
		return '%s - %s' % (self.title, self.user.email)


class Comment(BaseModel):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField(verbose_name='댓글')
	
	def __str__(self):
		return '%s - %s' % (self.id, self.user)
