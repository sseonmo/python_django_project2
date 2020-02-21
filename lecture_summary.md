
- django project 생성  
`django-admin startproject [프로젝트명]`
- app 생성  
`python manage.py startapp [app명]`  
`manage.py startapp [app명]`  
`django-admin startapp [app명]`

- db migration
    - python manage.py makemigrations users
    - python manage.py migrate 
 
- pilrow 팩키지
    - model imageField를 사용하기 위해선 필수적으로 필요한다. 
    - 설치 : pip install pillow
        - 설치시 에러발생 할 경우 pip 재설치  
        `easy_install -U pip`
    
```python
# BaseModel.py
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

---

# Post.py
from django.db import models

class Post(BaseModel):
...    	
image = models.ImageField(blank=True, null=True, verbose_name='이미지')
...
```