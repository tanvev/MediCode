from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from patients.views import PatientViewSet
from appointments.views import AppointmentViewSet
from visits.views import VisitViewSet

router = DefaultRouter()
router.register('patients', PatientViewSet)
router.register('appointments', AppointmentViewSet)
router.register('visits', VisitViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # App URLs
    path('patients/', include('patients.urls')),
    path('doctor/', include('doctors.urls')),
    path('analytics/', include('analytics.urls')),
    path('', include('accounts.urls')),
    path('expenses/', include('expenses.urls')),

    # DRF router URLs
    path('', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
