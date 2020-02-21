from django import forms
from .models import User


class RegisterForm(forms.ModelForm):
	"""
	회원가입 폼
	장고에서는 HTML 입력요소를 widget(위젯)이라고 말한다.
	"""
	password = forms.CharField(label='password', widget=forms.PasswordInput, required=True,
	                           error_messages={'required': '비밀번호를 입력해주세요'})
	confirm_password = forms.CharField(label='confirm_password', widget=forms.PasswordInput, required=True,
	                                   error_messages={'required': '비밀번호를 입력해주세요'})
	
	class Meta:
		model = User
		field_classes = ['username', 'first_name', 'last_name', 'gender', 'email']
	
	# def clean(self):
	# 	cd = self.cleaned_data
	# 	if cd.get('password') != cd.get('confirm_password'):
	# 		self.error_class('password', '비밀번호가 일치하지 않습니다.')
	# 		self.error_class('confirm_password', '비밀번호가 일치하지 않습니다.')
	
	def clean_confirm_password(self):
		cd = self.cleaned_data
		if cd.get('password') != cd.get('confirm_password'):
			raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
		
		return cd.get('confirm_password')
