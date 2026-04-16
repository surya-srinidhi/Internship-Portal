from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Company, Internship

# Unregister unnecessary models from Django Admin
# since we have our own Admin Dashboard for users and applications!
admin.site.unregister(Group)
admin.site.unregister(User)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    # Only show the specific fields the user requested when adding/editing
    fields = ('company', 'title', 'start_date', 'end_date', 'stipend', 'description')
    list_display = ('title', 'company', 'start_date', 'end_date')
    list_filter = ('company',)
