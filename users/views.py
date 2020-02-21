from django.shortcuts import render
from .forms import RegisterForm


# Create your views here.
def register(request):
	if request.POST == 'POST':
		user_form = RegisterForm(request.POST)
		#  유효성 검사 성공하면
		if user_form.is_valid():
			user = user_form.save(commit=False)
			user.set_password(user_form.cleaned_data['password'])
			user.save()
			return render(request, 'login.html', {'user', user})
	else:
		user_form = RegisterForm()
	
	return render(request, 'register.html', {'user_form': user_form})

