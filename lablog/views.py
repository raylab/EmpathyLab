from django.shortcuts import render
from .models import Experiment, Subject, Record, Stimulae, Feedback
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import ExperimentForm


def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_experiments = Experiment.objects.count()
    num_records = Record.objects.count()
    num_subjects = Subject.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Render the HTML template index.html with the data in the context
    # variable.
    return render(
        request,
        'index.html',
        context={
            'num_experiments': num_experiments,
            'num_records': num_records,
            'num_subjects': num_subjects,
            'num_visits': num_visits},
    )


class ExperimentListView(generic.ListView):
    """
    Generic class-based view for a list of experiments.
    """
    model = Experiment
    paginate_by = 10


class ExperimentDetailView(generic.DetailView):
    """
    Generic class-based detail view for a experiment.
    """
    model = Experiment


class StimulaeListView(generic.ListView):
    """
    Generic class-based list view for a list of records.
    """
    model = Stimulae
    paginate_by = 10


class StimulaeDetailView(generic.DetailView):
    """
    Generic class-based list view for a list of records.
    """
    model = Stimulae


class SubjectListView(generic.ListView):
    """
    Generic class-based list view for a list of subjects.
    """
    model = Subject
    paginate_by = 10


class FeedbackListView(generic.ListView):
    """
    Generic class-based list view for a list of records.
    """
    model = Feedback
    paginate_by = 10


class FeedbackDetailView(generic.DetailView):
    """
    Generic class-based list view for a list of records.
    """
    model = Feedback


class SubjectDetailView(generic.DetailView):
    """
    Generic class-based detail view for subject.
    """
    model = Subject


class RecordListView(generic.ListView):
    """
    Generic class-based list view for a list of records.
    """
    model = Record
    paginate_by = 10


class RecordDetailView(generic.DetailView):
    """
    Generic class-based list view for a list of records.
    """
    model = Record


class RecordsAllListView(PermissionRequiredMixin, generic.ListView):
    """
    Generic class-based view listing all records. Only visible to users with can_mark_returned permission.
    """
    model = Record
    permission_required = 'lablog.can_change_status'
    template_name = 'lablog/record_list_all.html'
    paginate_by = 10

    def get_queryset(self):
        return Record.objects.filter(status__exact='o').order_by('due_back')


class FeedbackCreate(PermissionRequiredMixin, CreateView):
    model = Feedback
    fields = '__all__'
    permission_required = 'lablog.can_change_status'


class FeedbackUpdate(PermissionRequiredMixin, UpdateView):
    model = Feedback
    fields = '__all__'
    permission_required = 'lablog.can_change_status'


class FeedbackDelete(PermissionRequiredMixin, DeleteView):
    model = Feedback
    success_url = reverse_lazy('feedbacks')
    permission_required = 'lablog.can_change_status'


class StimulaeCreate(PermissionRequiredMixin, CreateView):
    model = Stimulae
    fields = '__all__'
    permission_required = 'lablog.can_change_status'


class StimulaeUpdate(PermissionRequiredMixin, UpdateView):
    model = Stimulae
    fields = '__all__'
    permission_required = 'lablog.can_change_status'


class StimulaeDelete(PermissionRequiredMixin, DeleteView):
    model = Stimulae
    success_url = reverse_lazy('stimulaes')
    permission_required = 'lablog.can_change_status'


class SubjectCreate(PermissionRequiredMixin, CreateView):
    model = Subject
    fields = '__all__'
    permission_required = 'lablog.can_change_status'


class SubjectUpdate(PermissionRequiredMixin, UpdateView):
    model = Subject
    fields = '__all__'
    permission_required = 'lablog.can_change_status'


class SubjectDelete(PermissionRequiredMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy('subjects')
    permission_required = 'lablog.can_change_status'


class RecordCreate(PermissionRequiredMixin, CreateView):
    model = Record
    fields = '__all__'
    permission_required = 'lablog.can_change_status'


class RecordUpdate(PermissionRequiredMixin, UpdateView):
    model = Record
    fields = '__all__'
    permission_required = 'lablog.can_change_status'


class RecordtDelete(PermissionRequiredMixin, DeleteView):
    model = Record
    success_url = reverse_lazy('records')
    permission_required = 'lablog.can_change_status'


# Classes created for the forms challenge
class ExperimentCreate(PermissionRequiredMixin, CreateView):
    form_class = ExperimentForm
    model = Experiment
    permission_required = 'lablog.can_change_status'


class ExperimentUpdate(PermissionRequiredMixin, UpdateView):
    form_class = ExperimentForm
    model = Experiment
    permission_required = 'lablog.can_change_status'


class ExperimentDelete(PermissionRequiredMixin, DeleteView):
    model = Experiment
    success_url = reverse_lazy('experiments')
    permission_required = 'lablog.can_change_status'
