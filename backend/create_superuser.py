import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if username and password:
    user = User.objects.filter(username=username).first()

    if not user:
        user = User.objects.filter(email=email).first()

    if user:
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print("Superuser updated")
    else:
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print("Superuser created")