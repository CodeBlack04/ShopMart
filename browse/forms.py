from django import forms
from product.models import Category

class CategoryForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(
        queryset = Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'onChange': 'this.form.submit()'}),
        required= False,
    )