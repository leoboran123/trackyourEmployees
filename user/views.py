from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib import messages
import datetime

from user.forms import LoginForm, RegisterForm
from user.models import staffTrack, staffVacation, staffLate

# Create your views here.
def check_staff_is_late(user, date):
    data = staffTrack.objects.filter(user_id = user.id, todays_date = date)
    work_start_str = "08:00:00"
    work_start = datetime.datetime.strptime(work_start_str, '%H:%M:%S')

    staff_started_work_str = data[0].login_time.strftime('%H:%M:%S')
    staff_started_work = datetime.datetime.strptime(staff_started_work_str, '%H:%M:%S')

    if(work_start < staff_started_work):

        now=datetime.datetime.now()
        today_date = now.strftime('%Y-%m-%d')

        diff = staff_started_work - work_start

        
        print("todays date: ", today_date, "late diff: ", diff, "user: ", user.id)


        stflate = staffLate(todays_date = today_date, late_diff = diff, user_id = user.id)
        stflate.save()

    else:
        print("staff is NOT late")

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
                
                current_user = request.user
                now=datetime.datetime.now()
                today = now

                todays_date = now.strftime('%Y-%m-%d')

                todays_data = staffTrack.objects.filter(user_id = current_user.id, todays_date = todays_date)
                

                if(todays_data):
                    if(len(todays_data) > 1):

                        todays_data[0].login_time = now
                        todays_data[0].save()
                    else:
                        todays_data[0].login_time = now
                        todays_data[0].save()
                else:
                    data = staffTrack()

                    data.user_id = current_user.id
                    data.username = username
                    data.todays_date = today.strftime('%Y-%m-%d')
                    data.login_time = today


                    data.save()

                check_staff_is_late(current_user, todays_date)

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

            current_user = request.user
            now=datetime.datetime.now()
            today = now

            todays_date = now.strftime('%Y-%m-%d')

            todays_data = staffTrack.objects.filter(user_id = current_user.id, todays_date = todays_date)


            if(todays_data):
                if(len(todays_data) > 1):

                    todays_data[0].login_time = now
                    todays_data[0].save()
                else:
                    todays_data[0].login_time = now
                    todays_data[0].save()
            else:
                data = staffTrack()

                data.user_id = current_user.id
                data.username = username
                data.todays_date = today.strftime('%Y-%m-%d')
                data.login_time = today


                data.save()
            check_staff_is_late(current_user, todays_date)

            
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
    now=datetime.datetime.now()
    current_user = request.user

    today_date = now.strftime('%Y-%m-%d')


    staffTrack.objects.filter(user_id = current_user.id, todays_date = today_date).update(logout_time = now)

    logout(request)
    return HttpResponseRedirect("/")