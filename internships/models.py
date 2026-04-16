from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name

class Internship(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='internships')
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    stipend = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateField(blank=True, null=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} @ {self.company.name}"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=50, blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Application(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        SHORTLISTED = 'Shortlisted', 'Shortlisted'
        REJECTED = 'Rejected', 'Rejected'

    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name='applications')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='application_resumes/', null=True, blank=False)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.PENDING)

    def __str__(self):
        return f"{self.student.user.username} -> {self.internship.title}"

