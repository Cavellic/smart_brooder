from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import http.client
import json
import urllib.request
import urllib.error
from django.http import HttpResponse, HttpResponseRedirect
from urllib.request import urlopen
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import requests
from .models import *
import datetime
import os
from .forms import FeedingTimeTableForm, UserUpdateForm, ChicksManagementForm
from django.contrib.auth.decorators import login_required
from apscheduler.schedulers.blocking import BlockingScheduler

@login_required(login_url='login')
def index(request):
      
    eggs_produced = Egg.objects.all().order_by("-date")
    
    total_eggs = []
    dates = []
    total_quantity = 0
    
    for eggs in eggs_produced:
        total_eggs.append(eggs.quantity)
        dates.append(eggs.date)
        total_quantity += eggs.quantity
        
    print(total_quantity)
    
    try:
        
        BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?'

        API_KEY = 'd05fb11504c932ff4a2460516ee99e18'

        url = 'http://ipinfo.io/json'

        geo_response = urlopen(url)
        data = json.load(geo_response)

        print(data)

        CITY = data['city']
        url = BASE_URL + (f"q={CITY}&appid={API_KEY}&units=metric")
            
        response = requests.get(url).json()

        current_temp = response['main']['temp']
        current_humidity = response['main']['humidity']
            
        msg_danger = 'Low'
        
        msg_normal = 'Normal'
        
        msg_high = 'High'
                
        x = datetime.datetime.now()

        current_time = x.strftime("%H:%M:%S")
        
    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code} - {e.reason}")
        
    context = {
            'CITY': CITY,
            'current_temp': current_temp,
            'current_time': current_time,
            'current_humidity': current_humidity,
            'msg_danger': msg_danger, 
            'msg_normal': msg_normal,
            'msg_high': msg_high,
            'eggs_produced': eggs_produced,
            'total_quantity': total_quantity,
            'total_eggs': total_eggs,
            'dates': dates
        }
        
    return render(request, 'home.html', context)

def send_sms(msg):
    conn = http.client.HTTPSConnection("e55mz2.api.infobip.com")
    payload = json.dumps({
            "messages": [
                {
                    "destinations": [{"to":"263774793728"}],
                    "from": "447491163443",
                    "text": "{msg}"
                }
            ]
        })
    headers = {
            'Authorization': 'App 5d27bb47a8d26cbc9d26ac6dbac43b7f-92799359-2390-4b7e-94ee-bc580c7fd216',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    conn.request("POST", "/sms/2/text/advanced", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

@login_required(login_url='login')
def chicksManagement(request):
    batches = ChicksManagement.objects.all().order_by('-date')
    current_date = datetime.date.today()
        
    BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?'

    API_KEY = 'd05fb11504c932ff4a2460516ee99e18'

    url = 'http://ipinfo.io/json'

    geo_response = urlopen(url)
    data = json.load(geo_response)

    print(data['city'])

    CITY = data['city']
    url = BASE_URL + (f"q={CITY}&appid={API_KEY}&units=metric")
        
    response = requests.get(url).json()
        
    print(response)

    current_temp = response['main']['temp']
    current_humidity = response['main']['humidity']


        
    context = {
            'batches':batches,
            'current_date':current_date,
            'current_temp': current_temp,
            'current_humidity': current_humidity,
            'CITY':CITY,
        }  
        
        
    return render(request, 'chicksManagement.html', context)

@login_required(login_url='login')
def batchInfo(request, pk):
    batch = ChicksManagement.objects.get(id=pk)
    
    current_date = datetime.date.today()
        
    BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?'

    API_KEY = 'd05fb11504c932ff4a2460516ee99e18'

    url = 'http://ipinfo.io/json'

    geo_response = urlopen(url)
    data = json.load(geo_response)

    print(data['city'])

    CITY = data['city']
    url = BASE_URL + (f"q={CITY}&appid={API_KEY}&units=metric")
        
    response = requests.get(url).json()
        
    print(response)

    current_temp = response['main']['temp']
    current_humidity = response['main']['humidity']


        
    context = {
            'batch':batch,
            'current_date':current_date,
            'current_temp': current_temp,
            'current_humidity': current_humidity,
            'CITY':CITY,
        }  
    
    return render(request, 'batchInfo.html', context)

@login_required(login_url='login')
def eggProduction(request):
    eggs_produced = Egg.objects.all().order_by("-date")
    
    if request.method == 'POST':
        quantity = request.POST.get('eggs_quantity')
        
        eggs = Egg(quantity=quantity)
        eggs.save()
        messages.success(request, 'Todays record successfully saved.')
        
    context = {
        'eggs_produced': eggs_produced
    }
    return render(request, 'eggProduction.html', context)

@login_required(login_url='login')
def timeTable(request):
    
    if request.method == 'POST':
        form = FeedingTimeTableForm(request.POST)
        if form.is_valid():
            form.save()  # Redirect to a list or detail page after saving
    else:
        form = FeedingTimeTableForm()
        
    time_tables = FeedingTimeTable.objects.all().order_by('-time')
                        
    x = datetime.datetime.now()

    current_time = x.strftime("%H:%M")
    current_date = datetime.date.today()
                
    msg = ""
    defaultMsg = "No events to display"
    
    for time_table in time_tables:
            if current_time == time_table.time.strftime("%H:%M"):
                send_sms(time_table.description)
            elif current_date > time_table.date:
                time_table.delete()
            else:
                pass
        
    context = {
                    'time_tables': time_tables,
                    'current_time':current_time,
                    'msg':msg,
                    'defaultMsg':defaultMsg,
                    'form' : form
                }
        
        
        
    
    return render(request, 'feedingTimeTable.html', context)

def loginUser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if request.GET.get('next', None):
                return HttpResponseRedirect(request.GET['next'])
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Update the session with the new password hash so the user is not logged out
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully changed!')
            return redirect('profile')  # Redirect to some profile page after success
        else:
            messages.error(request, 'Password must contain at least 8 characters or the password is too similar to the email..')
    else:
        form = PasswordChangeForm(user=request.user)
        # messages.error(request, 'Passwords didnt match or the old password is incorrect')
    
    return render(request, 'change_password.html', {'form': form})

@login_required(login_url='login')
def create_chicks_management(request):
    if request.method == 'POST':
        form = ChicksManagementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New batch created successfully!")
            return redirect('chicks_management')  # Replace 'chicks_list' with the name of your list view
    else:
        form = ChicksManagementForm()

    return render(request, 'addNewBatch.html', {'form': form})



@login_required(login_url='login')  # Ensure the user is logged in to access this
def userProfile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')  # Redirect to some page after updating
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from .models import ChicksManagement
from .forms import ChicksManagementForm

@login_required(login_url='login')
def update_chicks(request, pk):
    # Fetch the specific record to update
    chicks_instance = get_object_or_404(ChicksManagement, pk=pk)
    
    # If the form is submitted
    if request.method == 'POST':
        form = ChicksManagementForm(request.POST, instance=chicks_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Batch updated successfully!")
            return redirect('chicks_management')  # Redirect to some page (replace 'chicks_list' with your actual URL)
    else:
        # Display the form with pre-filled data
        form = ChicksManagementForm(instance=chicks_instance)

    return render(request, 'updateBatch.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from .models import ChicksManagement
from django.contrib import messages

@login_required(login_url='login')
def delete_chicks_management(request, pk):
    # Get the specific entry by primary key
    chicks_management_entry = get_object_or_404(ChicksManagement, pk=pk)
    
    if request.method == 'POST':
        chicks_management_entry.delete()  # Delete the entry
        messages.success(request, "Batch deleted successfully!")
        return redirect('chicks_management')  # Replace 'chicks_list' with your list view or home page URL

    return render(request, 'confirmDelete.html', {'entry': chicks_management_entry})


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('/')