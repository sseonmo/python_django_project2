from django import forms
from .models import User


class RegisterForm(forms.ModelForm):
	"""
	회원가입 폼
	장고에서는 HTML 입력요소를 widget(위젯)이라고 말한다.
	"""
	# password = forms.CharField(label='password', widget=forms.PasswordInput, required=True,
	#                            error_messages={'required': '비밀번호를 입력해주세요'})
	# confirm_password = forms.CharField(label='confirm_password', widget=forms.PasswordInput, required=True,
	#                                    error_messages={'required': '비밀번호를 입력해주세요'})
	password = forms.CharField(label='password', widget=forms.PasswordInput)
	confirm_password = forms.CharField(label='confirm_password', widget=forms.PasswordInput)

	class Meta:
		model = User
		# fields = ['username', 'first_name', 'last_name', 'gender', 'email']
		fields = ['username', 'gender', 'email']
		
	# 	유효성 관련된 전체를 처리할수 있음
	# def clean(self):
	# 	print("user form : clean")
	# 	# pass
	# 	cd = self.cleaned_data
	# 	if cd.get('password') != cd.get('confirm_password'):
	# 		# 	에러메세지를 표시해줄 위치 지정이 힘들다.
	# 		raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
		
		# 아래 방식은 forms.Form를 사용할 때 표현할 수 있는 방식\
		# 틀정필드에 에러 메서지를 정의한다.
		# self.error_class('password', '비밀번호가 일치하지 않습니다.')
		# self.error_class('confirm_password', '비밀번호가 일치하지 않습니다.')
	
	# clean_[fieldname] : subfix로 field 붙여서 field 별로 유형성 검사를 할 수 있다.
	# 에러발생시 현재 field 가 아니라 이전 field 에 error message 표시된다.
	def clean_confirm_password(self):
		print("user form : clean_confirm_password")
		cd = self.cleaned_data
		if cd.get('password') != cd.get('confirm_password'):
			raise forms.ValidationError('비밀번호가 일치하지 않습니다.')

		return cd.get('confirm_password')
