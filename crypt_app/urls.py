from django.urls import path
from . import views

#TEMPLATE TAGGING
app_name = 'crypt_app'

urlpatterns = [
    path('registration/',views.registration,name='registration'),
    path('user_login/',views.user_login,name='user_login'),
]
