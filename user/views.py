from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required



import datetime


from user.forms import LoginForm, RegisterForm
from user.models import staffTrack, staffVacation, staffLate, staffRequest

# Create your views here.
def warn_boss(user_id):
    # if staff vacation 3 or below, warn
    # if staff asks for vacation, warn
    # if staff comes late, warn
    pass

def check_staff_is_late(user, date):
    data = staffTrack.objects.filter(user_id = user.id, todays_date = date)
    work_start_str = "08:00:00"
    work_start = datetime.datetime.strptime(work_start_str, '%H:%M:%S')

    work_end_str = "18:00:00"
    work_end = datetime.datetime.strptime(work_end_str, '%H:%M:%S')

    staff_started_work_str = data[0].login_time.strftime('%H:%M:%S')
    staff_started_work = datetime.datetime.strptime(staff_started_work_str, '%H:%M:%S')


    now=datetime.datetime.now()
    today_date = now.strftime('%Y-%m-%d')
    today_day_name = now.strftime('%A')

    if(today_day_name == "Saturday" or today_day_name == "Sunday"):
        print("Haftasonu iş yok!")
    elif(user.is_staff == 1):
        print("Siz patronsunuz!")
    else:

        if(work_start < staff_started_work):


            diff = staff_started_work - work_start

            
            print("todays date: ", today_date, "late diff: ", diff, "user: ", user.id)

            late = staffLate.objects.filter(user_id = user.id, todays_date = today_date)

            if(not late):
                stflate = staffLate(todays_date = today_date, late_diff = str(diff), user_id = user.id, active = False)
                stflate.save()


            stfVacation = staffVacation.objects.get(user_id = user.id)

            vacation_time = stfVacation.vacationTime

            time_inf = []

            value = ""

            index = 0
            for i in vacation_time:
                if(i == ":" or index+1>=len(vacation_time)):
                    time_inf.append(value)
                    value = ""
                else:
                    value+=i
                index += 1

            vacation_time = datetime.timedelta(hours = int(time_inf[0]), minutes=int(time_inf[1]), seconds=int(time_inf[2]))

            
            new_vacation_time = vacation_time - diff

            total_second = new_vacation_time.total_seconds()
            
            hours = int(total_second // 3600)  # 1 saat = 3600 saniye
            minutes = int(total_second % 3600) // 60  # Kalan saniyelerden dakikaları hesapla
            seconds = int(total_second % 60)  # Kalan saniyeler

            new_vacation_time = str(hours) + ":" + str(minutes) + ":" + str(seconds)

            staffVacation.objects.filter(user_id = user.id).update(vacationTime = new_vacation_time)

            # warn_boss(user.id)
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

                if(current_user.is_staff):
                    pass
                else:
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



def register_admin(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            non_user = form.save(commit=False)
            non_user.is_staff = True
            non_user.save()

            username = form.cleaned_data['username'].lower()
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)


            current_user = request.user
            if(current_user.is_staff):
                pass
            else:
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
            if(current_user.is_staff):
                pass
            else:
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
    
    today_day_name = now.strftime('%A')

    if(today_day_name == "Saturday" or today_day_name == "Sunday"):
        print("Haftasonu iş yok!")
    else:
        staffTrack.objects.filter(user_id = current_user.id, todays_date = today_date).update(logout_time = now)

    logout(request)
    return HttpResponseRedirect("/")

@login_required(login_url='/login')  # Check login
def seeDatas(request):
    current_user = request.user

    lateData = staffLate.objects.filter(user_id = current_user.id)
    vacationData = staffVacation.objects.get(user_id = current_user.id)

    time_inf = []

    vac_info = vacationData.vacationTime
    
    value = ""
    index = 0

    for i in vac_info:
        if(i==":"):
            time_inf.append(value)
            value = ""
        elif(index+1 == len(vac_info)):
            value += vac_info[index]
            time_inf.append(value)
            value = ""

        else:
            value+=i
        
        index += 1


    vacationDays = datetime.timedelta(hours= int(time_inf[0]), minutes=int(time_inf[1]), seconds=int(time_inf[2]))

    check_recent_request = staffRequest.objects.filter(user_id = current_user.id)

    if check_recent_request:

        for i in check_recent_request:
            if i.status == "Bekliyor":
                show_request_bar = False
                break      
            else:
                show_request_bar = True
    else:
        show_request_bar = True

    staffs = User.objects.filter(is_staff=1)

    context = {
        "lateData" : lateData,
        "vacationData": vacationData,
        "vacationDays" :vacationDays,
        "show_request_bar":show_request_bar,
        "recentRequests":check_recent_request,
        "staffs":staffs

    }

    return render(request, "seedata.html", context)

@login_required(login_url='/login')  # Check login
def checkStaff(request):
    
    staffData = staffLate.objects.all()
    staffVacationData = staffVacation.objects.all()
    staffTrackData = staffTrack.objects.all().order_by('todays_date')


    context = {
        "staffData":staffData,
        "staffVacationData":staffVacationData,
        "staffTrackData":staffTrackData
    }

    return render(request, "seeStaff.html", context)

@login_required(login_url='/login')  # Check login
def checkMessages(request):
    all_requests = staffRequest.objects.all()

    context = {
        "all_requests":all_requests,
    }

    return render(request, "seeMessages.html", context)

@login_required(login_url='/login')  # Check login
def requestVacation(request):
    if request.method == 'POST':
        current_user = request.user

        vacationDuration = request.POST["vacationDuration"]
        staff_id = request.POST.get("staffList")

        check_recent_request = staffRequest.objects.filter(user_id = current_user.id, status="Bekleniyor")

        if(not check_recent_request):
            vac_req = staffRequest()


            vac_req.user = current_user
            vac_req.requestedVacationTime = vacationDuration
            vac_req.staff = User.objects.filter(is_staff=1).first()

            vac_req.save()
            return HttpResponseRedirect("/vacation")
        else:
            
            messages.add_message(request, messages.INFO, "Zaten bir istekte bulundunuz!")
            return HttpResponseRedirect("/vacation")


    else:
        return HttpResponseRedirect("/vacation")

@login_required(login_url='/login')  # Check login
def requestApproved(request):
    if request.method == 'POST':
        current_user = request.user

        request_id = request.POST["approvedId"]
        request_user_id = request.POST["approvedUserId"]

        now = datetime.datetime.now()

        stf_req = staffRequest.objects.get(id=request_id)
        stf_requested_vacation_time = stf_req.requestedVacationTime
        stf_req.status = "Onaylandı"
        stf_req.active = 0
        stf_req.update_at = now
        stf_req.staff = current_user

        stf_req.save()


        time_inf = []
        stf_vac = staffVacation.objects.get(user_id = request_user_id)

        stf_vacTime = stf_vac.vacationTime

        value = ""
        index = 0

        for i in stf_vacTime:
            if(i==":"):
                time_inf.append(value)
                value = ""
            elif(index+1 == len(stf_vacTime)):
                value += stf_vacTime[index]
                time_inf.append(value)
                value = ""

            else:
                value+=i
            
            index += 1


        vacationDays = datetime.timedelta(hours= int(time_inf[0]), minutes=int(time_inf[1]), seconds=int(time_inf[2]))
        
        stf_requested_vacation_time = int(stf_requested_vacation_time * 24)
        stf_requested_vacation_time_hours = datetime.timedelta(hours=stf_requested_vacation_time)

        new_vacationTime = stf_requested_vacation_time_hours + vacationDays

        total_second = new_vacationTime.total_seconds()
        
        hours = int(total_second // 3600)  # 1 saat = 3600 saniye
        minutes = int(total_second % 3600) // 60  # Kalan saniyelerden dakikaları hesapla
        seconds = int(total_second % 60)  # Kalan saniyeler

        new_vacationTime = str(hours) + ":" + str(minutes) + ":" + str(seconds)


        stf_vac.vacationTime = new_vacationTime

        stf_vac.save()

        return HttpResponseRedirect("/mymessages")


    else:
        return HttpResponseRedirect("/mymessages")

@login_required(login_url='/login')  # Check login
def requestDeclined(request):
    if request.method == 'POST':
        request_id = request.POST["declined"]
        current_user = request.user


        now = datetime.datetime.now()

        stf_req = staffRequest.objects.get(id=request_id)

        stf_req.status = "Reddedildi"
        stf_req.update_at = now
        stf_req.active = 0
        stf_req.staff = current_user



        stf_req.save()
        return HttpResponseRedirect("/mymessages")


    else:
        return HttpResponseRedirect("/mymessages")

