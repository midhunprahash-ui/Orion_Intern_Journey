# your_app_name/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),  
    path('employee/<str:emp_id>/', views.employee_detail, name='employee_detail'),
    path('servers/', views.server_list, name='server_list'), 
    path('apps/', views.apps_list, name='apps_list'),  
    path('employee/<str:emp_id>/edit/', views.edit_employee, name='edit_employee'),
    path('access', views.data, name='data'), 
    path('access/edit/<int:access_key>/', views.edit_access_details, name='edit_access_details'), 
    path('access/<int:access_key>/', views.access_detail, name='access_detail_page'), 
    path('unauthorized-employees/', views.unauthorized_employees, name='unauthorized_employees'),
]
