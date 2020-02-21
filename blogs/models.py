from django.db import models
from helpers.models import BaseModel
from users.models import User


# Create your models here.
class Post(BaseModel):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=255, blank=False, verbose_name='타이틀')
	content = models.TextField(verbose_name='내용')
	image = models.ImageField(blank=True, null=True, verbose_name='이미지')
