from django import forms
from .models import Case, NotificationPreference

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['title', 'client','case_number','assigned_attorney','status','filing_date','court_name','description']

class NotificationPreferenceForm(forms.ModelForm):
    class Meta:
        model = NotificationPreference
        fields = ['email_notifications', 'notification_types']
        widgets = {
            'notification_types': forms.CheckboxSelectMultiple
        }