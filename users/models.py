from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.
GENDER_CHOICES = (
	(0, 'Male'),
	(1, 'Female'),
	(2, 'Not to disclose')
)

class UserManager(BaseUserManager):
	use_in_migrations = True
	
	# _ : prefix 클래스 내부에서만 사용하겠다는 의미
	def _create_user(self, email, username, password, gender=2, **extra_fields):
		"""
		Create and save a user with the given username, email, and password.
		"""
		if not email:
			raise ValueError('The given email must be set')
		email = self.normalize_email(email)
		username = self.model.normalize_username(username)
		user = self.model(email=email, username=username, gender=gender, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user
	
	def create_user(self, email, username='', password=None, **extra_fields):
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, username, password, **extra_fields)
	
	def create_superuser(self, email, username='', password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		
		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')
		
		return self._create_user(email, '', password, **extra_fields)


class User(AbstractUser):
	email = models.EmailField(verbose_name='email', max_length=125, unique=True)
	username = models.CharField(max_length=30)
	gender = models.SmallIntegerField(choices=GENDER_CHOICES)
	
	objects = UserManager()
	USERNAME_FIELD = 'email'
	# 필수를 받고 싶은 필드을 넣기위한
	REQUIRED_FIELDS = []
	
	def __str__(self):
		return "<%d %s>" % (self.pk, self.email)
