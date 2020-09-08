from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
# The above variable gives the user a choice to select quantity from 1 to 20

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    # TypeChoiceField with coerce=int to convert the input into an integer

    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)