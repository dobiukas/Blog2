from . import views
from django.urls import path,include
from .views import LoginPage, LogOutPage, RegisterPage

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('register/',RegisterPage,name='register'),
    path('login/',LoginPage,name='login'),
	path('logout/',LogOutPage,name='logout'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]