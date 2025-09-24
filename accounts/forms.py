# forms.py
from django import forms
from .models import NewsletterSubscription

class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if NewsletterSubscription.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError("This email is already subscribed.")
        return email