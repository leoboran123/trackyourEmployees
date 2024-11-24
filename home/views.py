from django.shortcuts import render
import datetime


from user.models import staffTrack

# Create your views here.
def index(request):
    current_user = request.user
    now=datetime.datetime.now()
    todays_date = now.strftime('%Y-%m-%d')


    data = staffTrack.objects.filter(user_id = current_user.id, todays_date = todays_date)
    deneme = len(data)

    context = {
        "data" : data,
        "deneme": deneme
    }

    return render(request, 'index.html', context)