from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required for application updates.")
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

from .models import Internship, StudentProfile, Application
from .services import send_application_received_email, send_application_status_update_email

class InternshipListView(ListView):
    model = Internship
    template_name = 'internships/internship_list.html'
    context_object_name = 'internships'
    queryset = Internship.objects.filter(is_published=True).order_by('-created_at')

class InternshipDetailView(DetailView):
    model = Internship
    template_name = 'internships/internship_detail.html'

class ApplyForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume']

@login_required
def apply_internship(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    
    # Check if student profile exists, if not create one
    student, created = StudentProfile.objects.get_or_create(user=request.user)
    
    # Check if already applied
    if Application.objects.filter(internship=internship, student=student).exists():
        messages.warning(request, "You have already applied for this internship.")
        return redirect('internships:detail', pk=pk)

    if request.method == 'POST':
        form = ApplyForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.student = student
            app.internship = internship
            app.save()
            
            # Send Email
            try:
                send_application_received_email(app)
            except Exception as e:
                print(f"Error sending email: {e}")

            messages.success(request, "Application submitted successfully! Check your email for confirmation.")
            return redirect('internships:dashboard')
    else:
        form = ApplyForm()
    return render(request, 'internships/apply.html', {'form': form, 'internship': internship})

@login_required
def student_dashboard(request):
    if request.user.is_superuser or request.user.is_staff:
        return redirect('internships:admin_dashboard')
        
    student, _ = StudentProfile.objects.get_or_create(user=request.user)
    applications = Application.objects.filter(student=student).order_by('-applied_at')
    return render(request, 'internships/student_dashboard.html', {'applications': applications})

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def admin_dashboard(request):
    applications = Application.objects.all().order_by('-applied_at')
    context = {
        'applications': applications,
        'pending_count': applications.filter(status='Pending').count(),
        'shortlisted_count': applications.filter(status='Shortlisted').count(),
        'rejected_count': applications.filter(status='Rejected').count(),
    }
    return render(request, 'internships/admin_dashboard.html', context)

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def update_application_status(request, pk, status):
    if request.method == 'POST':
        application = get_object_or_404(Application, pk=pk)
        if status in [choice[0] for choice in Application.StatusChoices.choices]:
            application.status = status
            application.save()
            
            # Send status update email
            try:
                send_application_status_update_email(application)
                messages.success(request, f"Application marked as {status} and email sent.")
            except Exception as e:
                messages.warning(request, f"Status updated, but email failed: {e}")
                
        return redirect('internships:admin_dashboard')
    return redirect('internships:admin_dashboard')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('internships:list')
        
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            StudentProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Registration successful! Welcome to the Internship Portal.")
            return redirect('internships:list')
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
