"""cloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from main import views

urlpatterns = [
    # Login
    path('', views.login, name="login"),
    path('index', views.index, name="index"),
    path('profile', views.profile, name="profile"),
    path('sign_in', views.sign_in, name="sign_in"),
    path('find_id_reset_pw', views.find_id_reset_pw, name="find_id_reset_pw"),
    path('logout', views.logout, name='logout'),
    path('movetots', views.movetots, name='movetots'),
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    path('movetoresetpw', views.movetoresetpw, name='movetoresetpw'),
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
]
