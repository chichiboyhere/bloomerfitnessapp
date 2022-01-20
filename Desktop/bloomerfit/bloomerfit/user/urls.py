from django.urls import path
from . import views

app_name='user'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.index, name='index'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('fitnessMeter/', views.fitnessMeter, name='fitnessMeter'),
    path('profile/', views.profile, name='profile'),
    path('members/', views.members, name='members'),
    path('m_converter/', views.m_converter, name="m_converter"),
    path('metric_converter/', views.metric_converter, name="metric_converter"),
    path('metric_converter_two/', views.metric_converter_two, name="metric_converter_two"),
    path('weight_tracker/', views.weight_tracker, name="weight_tracker"),
    path('contact/', views.contact, name="contact"),   
 ]