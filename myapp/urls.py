from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('request_user/', views.request_user, name='request_user'),
    path('sendrequest/<int:id>/',views.sendrequest,name='sendrequest'),
    path('acceptrequest/<int:id>/',views.acceptrequest,name='acceptrequest'),
    path('declinerequest/<int:id>/',views.declinerequest,name='declinerequest'),
    # path('contact/', views.contact, name='contact'),
    path('addcontact/', views.addcontact, name='addcontact'),
    path('deletecontact/<int:id>/', views.deletecontact, name='deletecontact'),
    path('editcontact/<int:id>/', views.editcontact, name='editcontact'),
    path('user_logout/',views.user_logout,name='user_logout'),

]
