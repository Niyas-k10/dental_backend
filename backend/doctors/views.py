from django.http import JsonResponse
from .models import Doctor

def doctor_list(request):
    doctors = Doctor.objects.all()

    data = []
    for doctor in doctors:
        data.append({
            'id': doctor.id,
            'name': doctor.name,
            'specialization': doctor.specialization,
            'experience': doctor.experience,
            'image': doctor.image.url if doctor.image else None
        })

    return JsonResponse(data, safe=False)