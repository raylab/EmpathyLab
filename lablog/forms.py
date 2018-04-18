from django import forms
from .models import Experiment, Analysis
from django.forms.widgets import TextInput, Textarea, DateTimeInput, SelectMultiple, Select, NumberInput


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
            'A': NumberInput(attrs={'class': 'form-control'}),
            'B': NumberInput(attrs={'class': 'form-control'}),
            'C': NumberInput(attrs={'class': 'form-control'}),
            'D': NumberInput(attrs={'class': 'form-control'}),
            'H': NumberInput(attrs={'class': 'form-control'}),
            'L': NumberInput(attrs={'class': 'form-control'}),
        }
