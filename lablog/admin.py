from django.contrib import admin

# Register your models here.

from .models import Subject, Stimulae, Experiment, Record, Feedback

"""
# Minimal registration of Models.
admin.site.register(Experiment)
admin.site.register(Subject)
admin.site.register(Record)
admin.site.register(Stimulae)
admin.site.register(Feedback)
"""

admin.site.register(Stimulae)
admin.site.register(Feedback)

class RecordsInline(admin.TabularInline):
    """
    Defines format of inline experiment insertion (used in SubjectAdmin)
    """
    model = Record


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """
    Administration object for Author models. 
    Defines:
     - fields to be displayed in list view (list_display)
     - orders fields in detail view (fields), grouping the date fields horizontally
     - adds inline addition of books in author view (inlines)
    """
    list_display = ('last_name', 'first_name', 'date_of_birth', 'gender') #, 'experiment')
    fields = ['first_name', 'last_name', ('date_of_birth', 'gender')]
    inlines = [RecordsInline]

class SubjectInline(admin.TabularInline):
    """
    Defines format of inline record instance insertion (used in SubjectAdmin)
    """
    model = Subject

class RecordInline(admin.TabularInline):
    """
    Defines format of inline record instance insertion (used in RecordAdmin)
    """
    model = Record

class ExperimentAdmin(admin.ModelAdmin):
    """
    Administration object for Experiment models. 
    Defines:
     - fields to be displayed in list view (list_display)
     - adds inline addition of record instances in record view (inlines)
    """
    list_display = ('title', 'display_stimulae', 'display_feedback') # , 'subject')
    #inlines = [SubjectInline] # , RecordInline]
    #fieldsets = ( (None, {'fields': ('')}),)

admin.site.register(Experiment, ExperimentAdmin)


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    """
    Administration object for Record models. 
    Defines:
     - fields to be displayed in list view (list_display)
     - filters that will be displayed in sidebar (list_filter)
     - grouping of fields into sections (fieldsets)
    """
    list_display = ('subject', 'experiment', 'status', 'attendant', 'imprint', 'id')
    list_filter = ('status', 'rec_date')
    
    fieldsets = (
        (None, {
            'fields': ('experiment', 'subject', 'imprint', 'id','observation')
        }),
        ('Details', {
            'fields': ('status', 'rec_date','attendant')
        }),
    )
