from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('contact/', views.contact, name='contact'),
    path('addcontact/', views.addcontact, name='addcontact'),
    path('deletecontact/<int:id>/', views.deletecontact, name='deletecontact'),
    path('editcontact/<int:id>/', views.editcontact, name='editcontact'),
    path('logout/',views.logout,name='logout'),

]
