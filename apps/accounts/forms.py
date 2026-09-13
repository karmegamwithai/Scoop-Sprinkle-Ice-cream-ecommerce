from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={"class": "form-input", "placeholder": "Choose a username"}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"class": "form-input", "placeholder": "you@example.com"}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(
        attrs={"class": "form-input", "placeholder": "Phone number"}))
    address = forms.CharField(required=False, widget=forms.Textarea(
        attrs={"class": "form-input", "rows": 3, "placeholder": "Delivery address"}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-input", "placeholder": "Password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-input", "placeholder": "Confirm password"}))

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") != cleaned.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-input", "placeholder": "Username"}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-input", "placeholder": "Password"}))


class ProfileForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-input"}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={"class": "form-input"}))
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-input", "rows": 3}))
