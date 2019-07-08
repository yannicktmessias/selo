from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import UserCreationForm, UserChangeForm
from .models import User

@login_required(login_url='login')
def user_info(request, rf = None):
	if rf == None:
		rf = request.user.rf
	usr = User.objects.get(rf=rf)
	return render(request, 'accounts/user_info.html', {'usr': usr})

@login_required(login_url='login')
def edit_user(request, rf = None):
	if rf == None:
		rf = request.user.rf
	usr = User.objects.get(rf=rf)

	if request.method == 'POST':
		form = UserChangeForm(request.POST, instance=usr)

		if form.is_valid():
			form.save()
			return redirect('user_info', rf=rf)
		
		args = {'form': form}
		return render(request, 'accounts/edit_user.html', args)
	else:
		form = UserChangeForm(instance=usr)

		args = {'form': form}
		return render(request, 'accounts/edit_user.html', args)

@login_required(login_url='login')
def delete_user(request, rf):
	return redirect('delete_user_confirmation', rf=rf)

@login_required(login_url='login')
def delete_user_confirmation(request, rf):
	usr = User.objects.get(rf=rf)
	if request.method == 'POST':
		User.objects.get(rf=rf).delete()
		return redirect('list_users')
	else:
		return render(request, 'accounts/delete_user_confirmation.html', {'usr': usr})

@login_required(login_url='login')
def new_user(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('user_info', rf=request.POST['rf'])

		args = {'form': form}
		return render(request, 'accounts/new_user.html', args)
	else:
		form = UserCreationForm()

		args = {'form': form}
		return render(request, 'accounts/new_user.html', args)

@login_required(login_url='login')
def list_users(request):
	users = User.objects.all()
	return render(request, 'accounts/list_users.html', {'users': users})

@login_required(login_url='login')
def search_user(request):
	# provisório
	users = User.objects.all()
	return render(request, 'accounts/list_users.html', {'users': users})
