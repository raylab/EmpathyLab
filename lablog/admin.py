from django.contrib import admin

# Register your models here.

from .models import Subject, Stimulae, Experiment, Record, Feedback

# Minimal registration of Models.
admin.site.register(Experiment)
admin.site.register(Subject)
admin.site.register(Record)
admin.site.register(Stimulae)
admin.site.register(Feedback)
