from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appointment
from clients.models import Client
from .forms import AppointmentForm
from django.utils import timezone
from datetime import datetime, timedelta

@login_required
def appointment_list(request):
    appointments = Appointment.objects.all().order_by('date_time')
    context = {
        'appointments': appointments,
        'clients': Client.objects.all(),
    }
    return render(request, 'appointments/appointment_list.html', context)

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.created_by = request.user
            appointment.save()
            return redirect('appointments:appointment_list')
    else:
        form = AppointmentForm()
    
    return render(request, 'appointments/appointment_form.html', {
        'form': form,
        'action': 'Create'
    })

@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'appointments/appointment_detail.html', {'appointment': appointment})

@login_required
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointments:appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointments/appointment_form.html', {'form': form})

@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointments:appointment_list')
    return render(request, 'appointments/appointment_confirm_delete.html', {'appointment': appointment})

@login_required
def appointment_calendar(request):
    today = timezone.now()
    appointments = Appointment.objects.filter(
        date_time__year=today.year,
        date_time__month=today.month
    ).order_by('date_time')
    
    context = {
        'appointments': appointments,
        'current_month': today.strftime('%B %Y')
    }
    return render(request, 'appointments/appointment_calendar.html', context)
