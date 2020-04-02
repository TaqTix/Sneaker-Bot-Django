from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
#My Views
from .forms import NewUserForm, UserUpdateForm, NikeTaskForm, WebsiteProfileForm
from NikeBotBackend import NikeBot



# def nike_view(request):
#     form = NikeForm(request.POST or None)
#     if form.is_valid():
#         form.save()

#     context{
#         'object': obj
#     }
#     return render(request, "nike_test.html", context)

def output(request):
    if request.is_ajax():
        url3 = 'https://www.nike.com/launch/t/pg-4-gatorade-gx/'
        login_username = 'acrypto91@gmail.com'
        login_temp_pass = 'Charlie123!'
        nikeObject = NikeBot.NikeBot(url3, 'M 7.5', login_username, login_temp_pass)
        nikeObject.main_loop()
        return render(request, 'output.html', {'output': "success, look for screenshots"})

# Create your views here.
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "login.html",
                    context={"form":form})

def logout_request(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return render(request, 'logout.html')

def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            messages.success(request, f'Account created for {username}!')
            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            return redirect('dashboard') 
    else:
        form = NewUserForm()
        for msg in form.error_messages:
            messages.error(request, f"{msg}: {form.error_messages}")
            #print(form.error_messages[msg]) 
    return render(request = request, 
                    template_name = 'register.html',
                    context= {'form': form})

@login_required
def dashboard(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = WebsiteProfileForm(request.POST,
                                   request.FILES,
                                   instance=None)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = WebsiteProfileForm(instance=None)

        context = {
            'u_form': u_form,
            'p_form': p_form,
        }

    return render(request, 'dashboard.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = WebsiteProfileForm(request.POST,
                                   request.FILES,
                                   instance=request.user.WebProfile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = WebsiteProfileForm(instance=request.user.WebProfile)

        context = {
            'u_form': u_form,
            'p_form': p_form,
        }

    return render(request, 'dashboard.html', context)