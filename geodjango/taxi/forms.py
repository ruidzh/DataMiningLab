from django import forms
from .models import Tripset


class TripsetForm(forms.Form):
    name = forms.CharField(max_length=200)
    limit = forms.IntegerField(required=False)
    def __init__(self, *args, **kwargs):
        super(TripsetForm, self).__init__(*args)
        datetime_filters = kwargs.pop('datetime_filters')
        for f in datetime_filters:
            self.fields[f] = forms.DateTimeField(required=False)
        decimal_filters = kwargs.pop('decimal_filters')
        for f in decimal_filters:
            self.fields[f] = forms.DecimalField(required=False)