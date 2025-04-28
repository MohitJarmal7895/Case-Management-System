from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cases.models import Case
from appointments.models import Appointment
from clients.models import Client
from django.utils import timezone  # Add this at the top with other imports

@login_required
def dashboard(request):
    recent_cases = Case.objects.all().order_by('-created_at')[:5]
    upcoming_appointments = Appointment.objects.filter(date_time__gte=timezone.now()).order_by('date_time')[:5]
    recent_clients = Client.objects.all().order_by('-created_at')[:5]
    
    context = {
        'recent_cases': recent_cases,
        'upcoming_appointments': upcoming_appointments,
        'recent_clients': recent_clients,
    }
    return render(request, 'dashboard.html', context)