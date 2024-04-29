from urllib import request
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import auth
from AQI.models import StudentUser,Location
import pandas as pd
import joblib
import requests
from .models import Location
from plotly.offline import plot
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from django.shortcuts import render
import pandas as pd
import plotly.express as px
from django.shortcuts import render
import seaborn as sns
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import plotly.graph_objs as go
AQI_KEY = "11c84b2c972b7519fe150cf25f5fcb7f"

# Load your trained model
model = joblib.load('airquality.joblib')

def dashboard(request):
    # Retrieve data from the database
    locations = Location.objects.all()

    # Prepare data for Plotly graphs
    x_data = [location.place for location in locations]
    pm25_data = [location.pm25 for location in locations]
    pm10_data = [location.pm10 for location in locations]
    o3_data = [location.o3 for location in locations]
    so2_data = [location.so2 for location in locations]
    no2_data = [location.no2 for location in locations]
    co_data = [location.co for location in locations]

    # Create Plotly graphs for each parameter
    fig_pm25 = go.Figure([go.Bar(x=x_data, y=pm25_data)])
    fig_pm10 = go.Figure([go.Bar(x=x_data, y=pm10_data)])
    fig_o3 = go.Figure([go.Bar(x=x_data, y=o3_data)])
    fig_so2 = go.Figure([go.Bar(x=x_data, y=so2_data)])
    fig_no2 = go.Figure([go.Bar(x=x_data, y=no2_data)])
    fig_co = go.Figure([go.Bar(x=x_data, y=co_data)])

    # Update layout for smaller size
    for fig in [fig_pm25, fig_pm10, fig_o3, fig_so2, fig_no2, fig_co]:
        fig.update_layout(
            autosize=True,
            margin=dict(l=20, r=20, t=40, b=20),  # Adjust margins for smaller size
            paper_bgcolor='rgba(0,0,0,0)',  # Set background color to transparent
            plot_bgcolor='rgba(0,0,0,0)',  # Set plot area background color to transparent
            height=600,  # Set height to 300 pixels
            width=700  # Set width to 500 pixels
        )

    # Convert Plotly graphs to HTML
    plot_div_pm25 = fig_pm25.to_html(full_html=False)
    plot_div_pm10 = fig_pm10.to_html(full_html=False)
    plot_div_o3 = fig_o3.to_html(full_html=False)
    plot_div_so2 = fig_so2.to_html(full_html=False)
    plot_div_no2 = fig_no2.to_html(full_html=False)
    plot_div_co = fig_co.to_html(full_html=False)

    # Pass data to the template
    context = {
        'locations': locations,
        'plot_div_pm25': plot_div_pm25,
        'plot_div_pm10': plot_div_pm10,
        'plot_div_o3': plot_div_o3,
        'plot_div_so2': plot_div_so2,
        'plot_div_no2': plot_div_no2,
        'plot_div_co': plot_div_co
    }

    return render(request, 'dashboard.html', context)



def index(request):
    return render(request,'index.html')

def places(request):
    places = Location.objects.all()
    context = {
        'places' : places
    }
    return render(request, 'places.html', context)

def track_aqi(request):
    return render(request,'track_aqi.html')

def CalculateAQI(request):
    return render(request,'CalculateAQI.html')

def signin(request):
    error=""
    if request.method == "POST":
        u = request.POST['uname'];
        p = request.POST['password'];
        user = authenticate(username=u,password=p)
        if user:
            try:
                user1 = StudentUser.objects.get(user=user)
                if user1.type == "student":
                    login(request,user)
                    error="no"
                else:
                    error="yes"
            except:
                error="yes"
        else:
            error="yes"

    d = {'error':error}
    return render(request,'signin.html',d)

def predict(request, pk):
    location = Location.objects.get(id=pk)
    lat = location.latitude
    lon = location.longitude
    place = location.place
    

    weather_response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={AQI_KEY}&units=metric')
    weather_data = weather_response.json()
    
    # Fetch weather forecast data for Uttar Pradesh
    forecast_response = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={AQI_KEY}&units=metric')
    forecast_data = forecast_response.json()

    # Fetch AQI data for Uttar Pradesh

    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={AQI_KEY}"
    response = requests.get(url)
    data = response.json()
    pollutants = data['list'][0]['components']
    pm25 = pollutants['pm2_5']
    pm10 = pollutants['pm10']
    so2 = pollutants['so2']
    no2 = pollutants['no2']
    co = pollutants['co']
    o3 = pollutants['o3']

    # Create a sample data array for prediction
    sample = [[pm25, pm10, o3, no2, co, so2]]

    # Make predictions using the loaded model
    prediction = model.predict(sample)
    print(f'Prediction: {prediction}')

    if prediction < 50:
        result = 'Air Quality is Good'
        conclusion = 'The air quality is excellent. It poses little or no risk to human health.'
    elif 51 <= prediction < 100:
        result = 'Air Quality is Satisfactory'
        conclusion = 'The air quality is satisfactory, but there may be a slight risk for some individuals who are unusually sensitive to air pollution.'
    elif 101 <= prediction < 200:
        result = 'Air Quality is Moderately Polluted'
        conclusion = 'The air quality is moderately polluted. People with respiratory or heart conditions may experience health effects. The general public is not likely to be affected.'
    elif 201 <= prediction < 300:
        result = 'Air Quality is Poor'
        conclusion = 'The air quality is poor and may cause health effects to everyone. People with respiratory or heart conditions may experience more serious health effects.'
    elif 301 <= prediction < 400:
        result = 'Air Quality is Very Poor'
        conclusion = 'The air quality is very poor, and it may have a severe impact on health. The entire population is likely to be affected.'
    else:
        result = 'Air Quality is Severe'
        conclusion = 'The air quality is severe, posing a serious health risk to everyone. The situation requires immediate attention and action to protect public health.'

    # Pass the result to a Django template
    return render(request, 'result.html', {'prediction': prediction/4,'lat': lat, 'lon':lon,'place': place, 'result': result, 'conclusion': conclusion,
                                           'forecast_data':forecast_data, 'weather_data':weather_data})


def Logout(request):
    logout(request)
    return redirect('index')


def change_passworduser(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    if request.method=="POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="no"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'change_passworduser.html',d)

def signup(request):
    error = ""
    if request.method=='POST':
       f =  request.POST['fname']
       l =  request.POST['lname']
       i =  request.FILES['Image']
       p =  request.POST['pwd']
       e =  request.POST['Email']
       con =  request.POST['Contact']
       gen =  request.POST['gender']
       try:
           user = User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
           StudentUser.objects.create(user=user,mobile=con,image=i,gender=gen,type="student")
           error = "no"
       except:
           error = "yes"
    d = {'error':error}
    return render(request,'signup.html',d)

def result(request):
    return render(request,'result.html')

def user_home(request):
    if not request.user.is_authenticated:
        return redirect('index')
    user=request.user
    student = StudentUser.objects.get(user=user)
    error=""
    if request.method == 'POST':
        f = request.POST.get('fname', '')  # Default to an empty string if 'fname' is missing
        l = request.POST.get('lname', '')  # Default to an empty string if 'lname' is missing
        con = request.POST.get('contact', '')  # Default to an empty string if 'contact' is missing
        gen = request.POST.get('gender', '')  # Default to an empty string if 'gender' is missing
      
        student.user.first_name = f
        student.user.last_name = l
        student.mobile = con
        student.gender = gen
        try:
            student.save()
            student.user.save()
            error="no"
        except:
            error="yes"

        try:
            i = request.FILES['image']
            student.image = i
            student.save()
            error="no"
        except:
            pass
    d = {'student': student, 'error':error}
    return render(request,'user_home.html',d)

def user_logout(request):
    auth.logout(request)
    return redirect("")

def maharashtra(request):
    return render(request, 'maharashtra.html')

def Rajasthan(request):
    return render(request, 'Rajasthan.html')

def Jodhpur(request):
    return render(request, 'Jodhpur.html')
    
def Ajmer(request):
    return render(request, 'Ajmer.html')

def chattisgarh(request):
    return render(request, 'chattisgarh.html')

def ahemdabad(request):
    return render(request, 'ahemdabad.html')

def Kota(request):
    return render(request, 'Kota.html')

def Surat(request):
    return render(request, 'Surat.html')

def Nashik(request):
    return render(request, 'Nashik.html')

def Nagpur(request):
    return render(request, 'Nagpur.html')

def Jamnagar(request):
    return render(request, 'Jamnagar.html')

def Mumbai(request):
    return render(request, 'Mumbai.html')

def Kolkata(request):
    return render(request, 'Kolkata.html')

def WestBengal(request):
    return render(request, 'WestBengal.html')

def Chennai(request):
    return render(request, 'Chennai.html')

def Odisha(request):
    return render(request, 'Odisha.html')

def Jalgaon(request):
    return render(request, 'Jalgaon.html')

def Varanasi(request):
    return render(request, 'Varanasi.html')

def Gorakhpur(request):
    return render(request, 'Gorakhpur.html')

def Bihar(request):
    return render(request, 'Bihar.html')

def gujarat(request):
    openweather_key = "11c84b2c972b7519fe150cf25f5fcb7f"
    lat = 23.2156  # Gujarat's latitude
    lon = 72.6369  # Gujarat's longitude
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={openweather_key}"
    response = requests.get(url)
    data = response.json()
    print(data)
    pollutants = data['list'][0]['components']
    pm25 = pollutants['pm2_5']
    pm10 = pollutants['pm10']
    so2 = pollutants['so2']
    no2 = pollutants['no2']
    co = pollutants['co']
    o3 = pollutants['o3']

    print("pm2.5:", pm25)
    print("pm10:", pm10)
    print("SO2:", so2)
    print("NO2:", no2)
    print("CO:", co)
    print("O3:",o3)
    return render(request, 'gujarat.html')

def punjab(request):
    return render(request, 'punjab.html')

def uttarpradesh(request):
    return render(request, 'uttarpradesh.html')

def kerala(request):
    return render(request, 'kerala.html')