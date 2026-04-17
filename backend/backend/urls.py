from django.contrib import admin
from django.urls import path, include

# for media files (images)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # users app
    path('api/users/', include('users.urls')),

    # doctors app
    path('api/doctors/', include('doctors.urls')),
]

# media support (for images)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)