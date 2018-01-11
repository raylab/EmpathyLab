from django.contrib import admin

# Register your models here.

from .models import Subject, Genre, Experiment, Record, Language

"""
# Minimal registration of Models.
admin.site.register(Experiment)
admin.site.register(Subject)
admin.site.register(Record)
admin.site.register(Genre)
admin.site.register(Language)
"""

admin.site.register(Genre)
admin.site.register(Language)

class RecordsInline(admin.TabularInline):
    """
    Defines format of inline experiment insertion (used in AuthorAdmin)
    """
    model = Experiment


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """
    Administration object for Author models. 
    Defines:
     - fields to be displayed in list view (list_display)
     - orders fields in detail view (fields), grouping the date fields horizontally
     - adds inline addition of books in author view (inlines)
    """
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [RecordsInline]


class RecordInline(admin.TabularInline):
    """
    Defines format of inline book instance insertion (used in BookAdmin)
    """
    model = Record

class ExperimentAdmin(admin.ModelAdmin):
    """
    Administration object for Experiment models. 
    Defines:
     - fields to be displayed in list view (list_display)
     - adds inline addition of record instances in record view (inlines)
    """
    list_display = ('title', 'subject', 'display_genre')
    inlines = [RecordInline]

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
    list_display = ('experiment', 'status', 'borrower','due_back', 'id')
    list_filter = ('status', 'due_back')
    
    fieldsets = (
        (None, {
            'fields': ('experiment','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )
