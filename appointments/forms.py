from django import forms
from .models import Appointment
from cases.models import Case

class AppointmentForm(forms.ModelForm):
    case = forms.ModelChoiceField(
        queryset=Case.objects.all(),
        required=False,
        empty_label="Select a Case"
    )
    
    class Meta:
        model = Appointment
        fields = ['title', 'client', 'case', 'date_time', 'status', 'description']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'status': forms.Select(choices=[
                ('SCHEDULED', 'Scheduled'),
                ('COMPLETED', 'Completed'),
                ('CANCELLED', 'Cancelled'),
                ('RESCHEDULED', 'Rescheduled'),
            ])
        }