from django import forms
from .models import Business

class BusinessForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    logo = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control-file'}))
    country_code = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}),required=False)
    phone = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}),required=False)
    location = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))

    class Meta:
        model = Business
        fields = ('name','logo','country_code','phone','email','location','description')

class BusinessEditForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    logo = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control-file'}),required=False)
    country_code = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}),required=False)
    phone = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}),required=False)
    location = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
