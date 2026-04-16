import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal.settings')
django.setup()

from internships.models import Internship
from django.contrib.auth.models import User

# Update Internship titles to "Software Developer"
updated_count = Internship.objects.all().update(title="Software Developer")
print(f"Updated {updated_count} internships to have the title 'Software Developer'.")

# Ensure all users have an email address so that local console emails don't fail silently
users_without_email = User.objects.filter(email='')
skipped = 0
for user in users_without_email:
    user.email = f"{user.username}@example.com"
    user.save()
    skipped += 1
print(f"Fixed {skipped} users that were missing an email address.")
