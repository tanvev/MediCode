from django.urls import path
from .views import OwnerDashboardView, owner_dashboard_page, load_demo

urlpatterns = [
    path('owner-dashboard/', OwnerDashboardView.as_view()),  # API
    path('dashboard/', owner_dashboard_page, name='owner-dashboard-ui'),  # UI
    path('load-demo/', load_demo),
]
