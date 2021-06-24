from django import forms

from .models import Inventory

class InventoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    price = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','step':'.01'}))
    unit = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'hours/mins/day/other'}),required=False)
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control-file'}),required=False)
    ## serviced_item = forms.CharField(widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    class Meta:
        model = Inventory
        fields = ('name','description','price','unit','image','serviced_item')