from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('accounts/register/',views.regist,name="register") ,
    path('accounts/verify/',views.verify,name="verify"),
    path('accounts/login/',views.login,name="login"),
     path('accounts/logout/',views.logout,name="logout"),
    path('donate/',views.donate,name="donate"),
    path('seek1/',views.seek1,name="seek1"),
    path('seek2/',views.seek2,name="seek2"),
    path('seek_submit/',views.seek_submit,name="seek_submit"),
    path('accounts/update/',views.update,name="update"),
]
