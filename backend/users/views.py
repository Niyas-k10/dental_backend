import json
import re
from datetime import date

from django.http import JsonResponse
from django.contrib.auth import get_user_model, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.http import HttpResponse

from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


# =========================
# 🔐 VALIDATION FUNCTIONS
# =========================

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def is_valid_phone(phone):
    return re.match(r"^[6-9]\d{9}$", phone)


def is_valid_password(password):
    return len(password) >= 6


def is_valid_dob(dob):
    try:
        year, month, day = map(int, dob.split('-'))
        birth_date = date(year, month, day)
        return birth_date < date.today()
    except:
        return False


# =========================
# 📝 REGISTER API
# =========================

@csrf_exempt
def register_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    try:
        data = json.loads(request.body)

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone')
        dob = data.get('dob')

        # 🔴 Required fields
        if not username or not email or not password:
            return JsonResponse({'error': 'Username, email and password are required'}, status=400)

        # 🔴 Validations
        if not is_valid_email(email):
            return JsonResponse({'error': 'Invalid email format'}, status=400)

        if phone:
            if not is_valid_phone(phone):
                return JsonResponse({'error': 'Invalid phone number'}, status=400)

            if User.objects.filter(phone=phone).exists():
                return JsonResponse({'error': 'Phone number already registered'}, status=400)

        if not is_valid_password(password):
            return JsonResponse({'error': 'Password must be at least 6 characters'}, status=400)

        if dob and not is_valid_dob(dob):
            return JsonResponse({'error': 'Invalid date of birth'}, status=400)

        # 🔴 Duplicate check
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already registered'}, status=400)

        # 🟢 Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone=phone,
            dob=dob,
            address=data.get('address', ''),
            sex=data.get('sex', '')
        )

        # 📧 Send email (real)
        try:
            send_mail(
                subject='Registration Successful',
                message=f'Hello {username}, welcome to our Dental Clinic!',
                from_email='yourgmail@gmail.com',
                recipient_list=[email],
                fail_silently=True   # IMPORTANT 
            )
        except Exception as mail_error:
            print("Email error:", mail_error)

        return JsonResponse({
            'message': 'User registered successfully'
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# =========================
# 🔑 LOGIN API (EMAIL + JWT)
# =========================

@csrf_exempt
def login_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    try:
        data = json.loads(request.body)

        email = data.get('email')
        password = data.get('password')

        # 🔴 Required
        if not email or not password:
            return JsonResponse({'error': 'Email and password are required'}, status=400)

        # 🔴 Validate email format
        if not is_valid_email(email):
            return JsonResponse({'error': 'Invalid email format'}, status=400)

        # 🔴 Find user
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid email or password'}, status=401)

        # 🔴 Authenticate
        user = authenticate(username=user_obj.username, password=password)

        if user is None:
            return JsonResponse({'error': 'Invalid email or password'}, status=401)

        # 🟢 Generate JWT
        refresh = RefreshToken.for_user(user)

        return JsonResponse({
            'message': 'Login successful',
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': {
                'username': user.username,
                'email': user.email
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def users_list(request):
    return HttpResponse("users API Working")