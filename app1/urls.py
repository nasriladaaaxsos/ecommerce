
#https://www.mywebsite.com/login

# /login

#routes 
from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),  
    path('login', views.login),   
    path('matches/<int:leagueId>/<str:leagueCountry>', views.display_matches),
    path('reg' , views.reg_form),
    path('reg_post' , views.reg_form_post),
    path('home' , views.home_page),
    path('logout' , views.logout,  name= 'logout'),
    path('update' , views.update_user),
    path('update_post' , views.update_post),
    path('deleteform' , views.delete_form),
    path('delete_user_by_id_form' , views.delete_by_user_id),
    path('addaddress' , views.addaddress),
    path( 'addressform' , views.address_add_form  ),
    path('showaddresses' , views.show_addresses),
    path('login_form' , views.login_form)

]