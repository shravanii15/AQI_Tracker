"""
URL configuration for Breatheasy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from AQI.views import index,signup,user_home,signin,track_aqi,maharashtra,gujarat,uttarpradesh,kerala,punjab,user_logout,CalculateAQI, places
from AQI.views import result,predict,dashboard,Rajasthan,Ajmer,ahemdabad,chattisgarh,change_passworduser,Logout
from AQI.views import Jodhpur,Kota,Jamnagar,Surat,Nashik,Mumbai,Odisha,Kolkata,WestBengal,Chennai,Gorakhpur,Nagpur,Bihar,Jalgaon,Varanasi
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name="index"),
    path('dashboard',dashboard,name="dashboard"),
    path('places',places,name="places"),
    path('signup',signup,name="signup"),
    path('Logout',Logout,name="Logout"),
    path('track_aqi',track_aqi,name="track_aqi"),
    path('signin',signin,name="signin"),
    path('user_home',user_home,name="user_home"),
    path('maharashtra',maharashtra, name="maharashtra"),
    path('gujarat',gujarat, name="gujarat"),
    path('uttarpradesh',uttarpradesh, name="uttarpradesh"),
    path('kerala',kerala, name="kerala"),
    path('punjab',punjab, name="punjab"),
    path('user-logout',user_logout, name="user-logout"),
    path('result/<str:pk>',predict, name='result'),
    path('predict',predict,name="predict"),
    path('Rajasthan',Rajasthan,name="Rajasthan"),
    path('Ajmer',Ajmer,name="Ajmer"),
    path('Jodhpur',Jodhpur,name="Jodhpur"),
    path('Kota',Kota,name="Kota"),
    path('Jamnagar',Jamnagar,name="Jamnagar"),
    path('Surat',Surat,name="Surat"),
    path('Nashik',Nashik,name="Nashik"),
    path('Mumbai',Mumbai,name="Mumbai"),
    path('Odisha',Odisha,name="Odisha"),
    path('Kolkata',Kolkata,name="Kolkata"),
    path('WestBengal',WestBengal,name="WestBengal"),
    path('Chennai',Chennai,name="Chennai"),
    path('Nagpur',Nagpur,name="Nagpur"),
    path('Jalgaon',Jalgaon,name="Jalgaon"),
    path('Varanasi',Varanasi,name="Varanasi"),
    path('Gorakhpur',Gorakhpur,name="Gorakhpur"),
    path('Bihar',Bihar,name="Bihar"),
    path('ahemdabad',ahemdabad,name="ahemdabad"),
    path('chattisgarh',chattisgarh,name="chattisgarh"),
    path('change_passworduser',change_passworduser,name="change_passworduser"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)