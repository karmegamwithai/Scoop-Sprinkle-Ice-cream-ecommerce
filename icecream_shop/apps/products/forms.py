from django import forms

CATEGORY_CHOICES = [
    ("Tub", "Tub"),
    ("Cone", "Cone"),
    ("Cup", "Cup"),
    ("Sundae", "Sundae"),
    ("Popsicle", "Popsicle"),
]


class ProductForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"class": "form-input", "placeholder": "e.g. Strawberry Bliss"}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={"class": "form-input", "rows": 3, "placeholder": "Short description"}))
    price = forms.DecimalField(min_value=0, decimal_places=2, widget=forms.NumberInput(
        attrs={"class": "form-input", "placeholder": "0.00", "step": "0.01"}))
    flavor = forms.CharField(max_length=50, required=False, widget=forms.TextInput(
        attrs={"class": "form-input", "placeholder": "e.g. Strawberry"}))
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={"class": "form-input"}))
    stock = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={"class": "form-input"}))
    image_url = forms.URLField(required=False, widget=forms.URLInput(
        attrs={"class": "form-input", "placeholder": "https://..."}))
