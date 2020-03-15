
## django 기본
### django project 생성  
    django-admin startproject [프로젝트명]
### app 생성  
    python manage.py startapp [app명]  
    manage.py startapp [app명]  
    django-admin startapp [app명]

### db migration
    - python manage.py makemigrations users
    - python manage.py migrate 
 
### templates 경로
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
     
### User model를 custom 할경우
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

### django 내장되어 있는 로그인, 로그아웃을 사용하는 경우
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

### custom 모델 상속 Tip
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
	# auto_now : 생성될때, 수정될때
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
### URL Reverse 
- 참조사이트
    > https://wayhome25.github.io/django/2017/05/05/django-url-reverse/  
    https://docs.djangoproject.com/en/3.0/ref/urlresolvers/
> reverse
```python

# urls.py

path('post/', posts_list, name='posts_list'),   # /blog/post/
path('post/<int:post_id>', post_detail, name='post_detail'),    # /blog/1/

---

# reverse(viewname, urlconf=None, args=None, kwargs=None, current_app=None)

from django.core.urlresolvers import reverse

reverse('blog:post_list')                       # '/blog/'
reverse('blog:post_detail', args=[10])          # '/blog/10/' args 인자로 리스트 지정 필요 - 순서대로 매핑
reverse('blog:post_detail', kwargs={'post_id':10})   # '/blog/10/'
reverse('/hello/')                              # NoReverseMatch 오류 발생
```
> resolve_url
```python
# 내부적으로 reverse() 사용
# resolve_url(to, *args, **kwargs):

from django.shortcuts import resolve_url

resolve_url('post_list') # '/blog/'
resolve_url('post_detail', 10) # '/blog/10/'
resolve_url('post_detail', post_id=10) # '/blog/10/'
resolve_url('/hello/') # '/hello/' 문자열 그대로 리턴
```
> redirect  
- 리턴형식 : HttpResponseRedirect  
- 내부적으로 resolve_url() 사용  
- views 함수 내에서 특정 url로 이동 하고자 할 때 사용 (Http Response)
```python
from django.shortcuts import redirect

redirect('post_detail', 10)
```
>url template tag
- 내부적으로 reverse() 사용
```html
<li><a href="{% url 'post_detail' post.id %}">{{ post.title }}</a> </li>
```


### 이미지파일
- pilrow lib 설치필요
```python
# setting.py

"""
파일업로드 관련
MEDIA_URL 은 MEDIA_ROOT에 접근할 URL을 뜻한다 - 항상 / 로 끝나도록 설정
MEDIA_ROOT 는 파일을 업로드할 장소를 뜻한다면,
"""
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

---

# urls.py

from django.conf import settings
from django.conf.urls.static import static

"""
MEDIA_URL 을 활성화 시켜줬다면 http://localhost:8000/media/FILE_NAME 과 같은 URL로 파일을 불러올 수 있다.
- static(templates) 파일과는 다르게 개발서버에서 기본 서빙 미지원
- 개발 편의성 목적으로 서빙 rule 추가 가능
- settings.DEBUG = False 일때는 static 함수에서 빈 리스트 리턴
"""
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

---

# models.py

# Create your models here.
class Post(BaseModel):
    
    ...
    """
    - upload_to 인자를 함께 넣어 경로를 설정할수 있다. 
    - MEDIA_ROOT경로 이후로 upload_to 경로가 더해서 저장됨
    - 제출된 파일, 이미지는 settings.MEDIA_ROOT 경로에 파일을 저장하고,
    - DB 필드에는 settings.MEDIA_ROOT 내 저장된 하위 경로를 저장
        저장경로 : MEDIA_ROOT/2017/05/10/xxxx.jpg 경로에 저장
        DB필드   : 'MEDIA_URL/2017/05/10/xxxx.jpg' 문자열 저장
    """
    image = models.ImageField(blank=True, null=True, verbose_name='이미지', upload_to='%Y/%m/%d')
    ...
    
    # delete 오버라이딩 - 삭제시 이미지 파일도 삭제하기 위해서 
    def delete(self, *args, **kargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
        # 원래의 delete 함수를 실행
        super(Post, self).delete(*args, **kargs)
```
> write.html
```html
# write.html
<!--
template html의 form에서 유저가 파일을 업로드 하기 위해서는 몇 가지 설정이 필요하다.
form method : 반드시 POST 로 설정이 필요하다.
form enctype : multipart/form-data 로 설정이 필요하다.
-->
<!-- 업로드시 -->
<form method="post" action="{% url 'post_write' %}" enctype="multipart/form-data">    
    {% csrf_token %}
    ...
    <div class="form-group">
        <label for="image">이미지</label>
        <input type="file" class="form-control-file" id="image" name="image">
    </div>
    ...
</form>

<!-- 보여질때 -->
<h2>{{ post.title }}</h2>
{% if post.image %}
    path :{{ post.image.path }}
    url : {{ post.image.url }}
    <img src="{{ post.photo.url }}" alt="">
{% endif %}
```
























  
    
      
      
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


