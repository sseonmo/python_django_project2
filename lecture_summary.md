
## django 기본
- django project 생성  
`django-admin startproject [프로젝트명]`
- app 생성  
`python manage.py startapp [app명]`  
`manage.py startapp [app명]`  
`django-admin startapp [app명]`

- db migration
    - python manage.py makemigrations users
    - python manage.py migrate 
 
- templates 경로
    - 각 app의 하위에 templates 디렉토리에 html를 생성했을 경우는 별도의 templates 경로설정이 필요없다.
    - 기본적으로 template 파일을 검색할때 기본적으로 app의 templates 디렉토리를 검사하기 때문이다.
     ```python
    # setting.py
    # templates 위치지정 DIR[] 에 정의해야함. - os.path.join(BASE_DIR, 'templates')
    TEMPLATES = [
        {
            ....
            'DIRS': [
                os.path.join(BASE_DIR, 'templates')
            ],
            ....
        },
    ]    
    ```
     
- User model를 custom 할경우
    ```python
    # setting.pyUser 
    
    """
    api.User.groups: (fields.E304) Reverse accessor for 'User.groups' clashes with reverse accessor for 'User.groups'.
    HINT: Add or change a related_name argument to the definition for 'User.groups' or 'User.groups'.
    api.User.user_permissions: (fields.E304) Reverse accessor for 'User.user_permissions' clashes with reverse accessor for 'User.user_permissions'.
    HINT: Add or change a related_name argument to the definition for 'User.user_permissions' or 'User.user_permissions'.
    User 모델을 커스터마이징 했을 때 발생하는 에러.
    settings.py에 다음을 추가해준다.
    """
    AUTH_USER_MODEL = 'users.User'
    ```
- django 내장되어 있는 로그인, 로그아웃을 사용하는 경우
```python
# urls.py
urlpatterns = [
	path('accounts/', include('django.contrib.auth.urls')),
]

---
# django.contrib.auth.urls
"""
로그인과 로그아웃는 아래위치에 template 파일이 위치해야함
lib source에 하드코딩되어있음
registration/login.html
registration/logged_out.html
"""
 
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

---
# setting.py
# 아래 로그인, 로그아웃 변수는 꼭 셋팅해야함
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```

- custom 모델 상속 Tip
````python
"""
공통적인 부분을 추상클래스로 만들어 사용한다.
추상클래스로 만들면 실제 table는 생성되지 않는다. 
"""
# helper/models.py
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
# blogs/models.py

from django.db import models
from helpers.models import BaseModel
from users.models import User

# Create your models here.
class Post(BaseModel):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=255, blank=False, verbose_name='타이틀')
	content = models.TextField(verbose_name='내용')
	image = models.ImageField(blank=True, null=True, verbose_name='이미지')


````
## package
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


