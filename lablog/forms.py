from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.

from django import forms
from .models import Experiment
from django.forms.widgets import TextInput, Textarea, DateTimeInput, SelectMultiple, Select


class ExperimentForm(forms.ModelForm):
    """
    Form for a editing experiment.
    """

    class Meta(object):
        model = Experiment
        fields = [
            'title',
            'summary',
            'DateTime',
            'subjects',
            'stimulae',
            'feedback']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'summary': Textarea(attrs={'class': 'form-control'}),
            'DateTime': DateTimeInput(attrs={'class': 'form-control'}),
            'subjects': SelectMultiple(attrs={'class': 'form-control'}),
            'stimulae': Select(attrs={'class': 'form-control'}),
            'feedback': Select(attrs={'class': 'form-control'}),
        }
