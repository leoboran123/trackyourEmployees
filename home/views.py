from django.shortcuts import render
import datetime


from user.models import staffTrack

# Create your views here.
def index(request):
    
    return render(request, 'index.html')