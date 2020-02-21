from django.db import models


# Create your models here.
class BaseModel(models.Model):
	# auto_now_add : 생성될때
	# auto_now : 수정될때
	create_at = models.DateTimeField(verbose_name='등록일자', auto_now_add=True)
	modified_at = models.DateTimeField(verbose_name='수정일자', auto_now=True)
	
	class Meta:
		# abstract 추상클래스로 사용 / 추상클래스는 table로 생성되지 않음.
		abstract = True
