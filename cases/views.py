from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Case, NotificationPreference
from .forms import CaseForm, NotificationPreferenceForm
from .utils import send_case_notification
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import EmailNotification
# from clients.models import Client

@login_required
def case_list(request):
    cases = Case.objects.all().order_by('-created_at')
    return render(request, 'cases/case_list.html', {'cases': cases})

@login_required
def case_detail(request, pk):
    case = get_object_or_404(Case, pk=pk)
    return render(request, 'cases/case_detail.html', {'case': case})

@login_required
def case_create(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            case = form.save()
            send_case_notification(request, case, 'filing')
            messages.success(request, 'Case created successfully.')
            return redirect('cases:case_detail', pk=case.pk)
    else:
        form = CaseForm()
    return render(request, 'cases/case_form.html', {'form': form})

@login_required
def case_update(request, pk):
    case = get_object_or_404(Case, pk=pk)
    if request.method == 'POST':
        form = CaseForm(request.POST, instance=case)
        if form.is_valid():
            case = form.save()
            if form.has_changed():
                send_case_notification(request, case, 'update', {
                    'update_description': 'Case details have been updated.'
                })
            messages.success(request, 'Case updated successfully.')
            return redirect('cases:case_detail', pk=pk)
    else:
        form = CaseForm(instance=case)
    return render(request, 'cases/case_form.html', {'form': form})

@login_required
def case_status_update(request, pk):
    case = get_object_or_404(Case, pk=pk)
    if request.method == 'POST':
        old_status = case.status
        status = request.POST.get('status')
        if status in dict(Case.STATUS_CHOICES):
            case.status = status
            case.save()
            if old_status != status:
                send_case_notification(request, case, 'update', {
                    'update_description': f'Case status changed to {case.get_status_display()}'
                })
            messages.success(request, 'Case status updated successfully.')
        else:
            messages.error(request, 'Invalid status value.')
    return redirect('cases:case_detail', pk=pk)

@login_required
def case_delete(request, pk):
    case = get_object_or_404(Case, pk=pk)
    if request.method == 'POST':
        case.delete()
        messages.success(request, 'Case deleted successfully.')
        return redirect('cases:case_list')
    return render(request, 'cases/case_confirm_delete.html', {'case': case})


@login_required
def track_email_open(request, tracking_id):
    notification = get_object_or_404(EmailNotification, tracking_id=tracking_id)
    notification.status = 'OPENED'
    notification.save()
    
    # Return a 1x1 transparent pixel
    pixel = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
    return HttpResponse(pixel, content_type='image/gif')

@login_required
def track_email_click(request, tracking_id):
    notification = get_object_or_404(EmailNotification, tracking_id=tracking_id)
    notification.status = 'CLICKED'
    notification.save()
    
    redirect_url = request.GET.get('url', '/')
    return HttpResponseRedirect(redirect_url)


@login_required
def notification_dashboard(request):
    notifications = EmailNotification.objects.select_related('case').all()
    
    stats = {
        'total': notifications.count(),
        'sent': notifications.filter(status='SENT').count(),
        'opened': notifications.filter(status='OPENED').count(),
        'clicked': notifications.filter(status='CLICKED').count(),
        'failed': notifications.filter(status='FAILED').count(),
    }
    
    context = {
        'notifications': notifications,
        'stats': stats,
    }
    return render(request, 'cases/notification_dashboard.html', context)


@login_required
def notification_preferences(request):
    preference, created = NotificationPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = NotificationPreferenceForm(request.POST, instance=preference)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notification preferences updated successfully.')
            return redirect('cases:notification_dashboard')
    else:
        form = NotificationPreferenceForm(instance=preference)
    
    return render(request, 'cases/notification_preferences.html', {'form': form})
