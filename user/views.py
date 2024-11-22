from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib import messages

from user.forms import LoginForm, RegisterForm


# Create your views here.

def login_user(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].lower()
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Başarıyla giriş yapıldı! {user.username}")
                return HttpResponseRedirect('/')
            else:
                messages.warning(request, "Tekrar oturum açmayı deneyin")
                return HttpResponseRedirect('/login')

    else:
        login_form = LoginForm
        context = {
            "form":login_form
        }

        return render(request, "login.html", context)


def register_user(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username'].lower()
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)

            # current_user = user
            # data = UserProfile()
            # data.user_id = current_user.id
            # data.save()
            messages.success(request, "Hesabınız başarıyla oluşturuldu!")
            return HttpResponseRedirect("/")
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/register")
        
    else:
        register_form = RegisterForm
        context= {
            "form":register_form
        }

        return render(request, "register.html", context)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")