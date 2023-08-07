from django import forms


class UpdateCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
