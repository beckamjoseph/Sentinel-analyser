from django.urls import path
from .views import analyze_url, scan_history, clear_history

urlpatterns = [
    path('analyze/', analyze_url),
    path('history/', scan_history),
    path('clear-history/', clear_history),
]
