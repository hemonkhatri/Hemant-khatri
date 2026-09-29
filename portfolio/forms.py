from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Bots fill hidden fields; humans never see this one.
    company_website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "autocomplete": "email"}),
            "subject": forms.TextInput(attrs={"placeholder": "What is this about?"}),
            "message": forms.Textarea(attrs={"rows": 7, "placeholder": "Tell me a bit about it."}),
        }

    @property
    def is_spam(self):
        return bool(self.cleaned_data.get("company_website"))

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 15:
            raise forms.ValidationError("Add a little more detail — at least 15 characters.")
        return message
