from django.contrib import admin
from django.urls import path, include
from home import views

 
 



urlpatterns = [ 
   path('', views.home, name='home'),
   path('about', views.about, name='about'),
   path('contact', views.contact, name='contact'),
   path('convocation', views.convocation, name='convocation'),
   path('search', views.search, name='search'),
   path('signup', views.handleSignup, name='handleSignup'),
   path('login', views.handleLogin, name='handleLogin'),
   path('logout', views.handleLogout, name='handleLogout'),
   path('CreateNewPost', views.CreateNewPost, name='createpost'),
   path('profile/<str:username>', views.MyProfile, name='MyProfile'),
   path('likepost', views.LikePost, name='likepost'),
   path('deletepost', views.deletepost, name='deletepost'),
   path('filter/<str:type>', views.typeprofile, name='typeart')
   
]