from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user/', views.user_view, name='user'),
    path('select_image/', views.select_image, name='select_image'),
]
