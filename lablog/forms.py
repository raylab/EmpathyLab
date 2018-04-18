from django import forms
from .models import Experiment, Analysis
from django.forms.widgets import TextInput, Textarea, DateTimeInput, SelectMultiple, Select, NumberInput


class RangeInput(NumberInput):
    input_type = "range"


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


class AnalysisForm(forms.ModelForm):
    class Meta(object):
        model = Analysis
        fields = ['name', 'A', 'B', 'C', 'D', 'H', 'L']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'A': RangeInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'B': RangeInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'C': RangeInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'D': RangeInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'H': RangeInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'L': RangeInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
        }
