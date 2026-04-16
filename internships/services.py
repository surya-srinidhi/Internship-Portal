from django.core.mail import send_mail
from django.conf import settings
from .models import Application

def send_application_received_email(application: Application):
    """Sends email to student and admin when a new application is submitted."""
    
    # Send to student
    student_subject = f"Application Received: {application.internship.title} at {application.internship.company.name}"
    student_message = (
        f"Hi {application.student.user.first_name or application.student.user.username},\n\n"
        f"We have successfully received your application for the {application.internship.title} role at {application.internship.company.name}.\n"
        f"You can track your application status in your dashboard.\n\n"
        f"Best regards,\nInternship Portal Team"
    )
    send_mail(
        subject=student_subject,
        message=student_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[application.student.user.email] if application.student.user.email else [],
        fail_silently=False,
    )

    # Send to admin (for simplicity, using DEFAULT_FROM_EMAIL as admin email or getting superusers)
    from django.contrib.auth.models import User
    admin_emails = list(User.objects.filter(is_superuser=True).values_list('email', flat=True))
    if admin_emails:
        admin_subject = f"New Application for {application.internship.title}"
        admin_message = (
            f"A new application has been submitted by {application.student.user.username} for {application.internship.title} at {application.internship.company.name}.\n"
            f"Please log in to the admin portal to review."
        )
        send_mail(
            subject=admin_subject,
            message=admin_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=admin_emails,
            fail_silently=False,
        )

def send_application_status_update_email(application: Application):
    """Sends email to student when their application status changes to Shortlisted or Rejected."""
    
    status = application.status
    subject = f"Update on your application for {application.internship.title}"
    
    if status == 'Shortlisted':
         message = (
            f"Hi {application.student.user.first_name or application.student.user.username},\n\n"
            f"Great news! Your application for the {application.internship.title} role at {application.internship.company.name} has been SHORTLISTED.\n"
            f"The employer will reach out to you soon with further instructions.\n\n"
            f"Best regards,\nInternship Portal Team"
        )
    elif status == 'Rejected':
        message = (
            f"Hi {application.student.user.first_name or application.student.user.username},\n\n"
            f"Thank you for applying to the {application.internship.title} role at {application.internship.company.name}.\n"
            f"Unfortunately, your application was not selected to move forward at this time.\n"
            f"Keep exploring other opportunities on our Internship Portal!\n\n"
            f"Best regards,\nInternship Portal Team"
        )
    else:
        return # Do not send for Pending
        
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[application.student.user.email] if application.student.user.email else [],
        fail_silently=False,
    )
