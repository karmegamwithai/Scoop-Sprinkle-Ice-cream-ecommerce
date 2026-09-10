from django import forms


class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea(
        attrs={"class": "form-input", "rows": 3, "placeholder": "Delivery address"}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={"class": "form-input", "placeholder": "Contact phone number"}))
