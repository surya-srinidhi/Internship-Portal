from django.urls import path
from . import views

app_name = 'internships'

urlpatterns = [
    path('', views.InternshipListView.as_view(), name='list'),
    path('internship/<int:pk>/', views.InternshipDetailView.as_view(), name='detail'),
    path('internship/<int:pk>/apply/', views.apply_internship, name='apply'),
    
    # Dashboards
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('admin-portal/', views.admin_dashboard, name='admin_dashboard'),
    
    # Application Actions
    path('application/<int:pk>/update-status/<str:status>/', views.update_application_status, name='update_status'),
    
    # Auth
    path('register/', views.register_view, name='register'),
]
