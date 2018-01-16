from django.shortcuts import render

#import pdb; pdb.set_trace()

# Create your views here.

from .models import Experiment, Subject, Record, Stimulae, Feedback

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_experiments=Experiment.objects.all().count()
    num_records=Record.objects.all().count()
    # Available records
    num_records_available=Record.objects.filter(status__exact='a').count()
    num_subjects=Subject.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    
    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_experiments':num_experiments,'num_records':num_records,'num_records_available':num_records_available,'num_subjects':num_subjects,
            'num_visits':num_visits},
    )

from django.views import generic


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


from django.contrib.auth.mixins import LoginRequiredMixin

class RecordsByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing records to current user. 
    """
    model = Record
    template_name ='lablog/record_list_by_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return Record.objects.filter(attendant=self.request.user).filter(status__exact='o').order_by('due_back')
        


# Added as part of challenge!
from django.contrib.auth.mixins import PermissionRequiredMixin

class RecordsAllListView(PermissionRequiredMixin,generic.ListView):
    """
    Generic class-based view listing all records. Only visible to users with can_mark_returned permission.
    """
    model = Record
    permission_required = 'lablog.can_change_status'
    template_name ='lablog/record_list_all.html'
    paginate_by = 10
    
    def get_queryset(self):
        return Record.objects.filter(status__exact='o').order_by('due_back')  


from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import permission_required

#from .forms import RenewBookForm

#@permission_required('lablog.can_mark_returned')
#def renew_record_librarian(request, pk):
#    """
#    View function for renewing a specific Record by attendant
#    """
#    record_inst=get_object_or_404(Record, pk = pk)
#
#    # If this is a POST request then process the Form data
#    if request.method == 'POST':
#
#        # Create a form instance and populate it with data from the request (binding):
#        form = RenewBookForm(request.POST)
#
#        # Check if the form is valid:
#        if form.is_valid():
#            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
#            record_inst.due_back = form.cleaned_data['renewal_date']
#            record_inst.save()
#
#            # redirect to a new URL:
#            return HttpResponseRedirect(reverse('all-borrowed') )
#
#    # If this is a GET (or any other method) create the default form
#    else:
#        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
#        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})
#
#    return render(request, 'lablog/record_renew_librarian.html', {'form': form, 'record':record_inst})
    
    
    
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
#from .models import Subject


class FeedbackCreate(PermissionRequiredMixin, CreateView):
    model = Feedback
    fields = '__all__'
    permission_required = 'lablog.can_change_status'

class FeedbackUpdate(PermissionRequiredMixin, UpdateView):
    model = Feedback
    permission_required = 'lablog.can_change_status'

class FeedbackDelete(PermissionRequiredMixin, DeleteView):
    model = Feedback
    success_url = reverse_lazy('feedback')
    permission_required = 'lablog.can_change_status'

class StimulaeCreate(PermissionRequiredMixin, CreateView):
    model = Stimulae
    fields = '__all__'
    permission_required = 'lablog.can_change_status'

class StimulaeUpdate(PermissionRequiredMixin, UpdateView):
    model = Stimulae
    permission_required = 'lablog.can_change_status'

class StimulaeDelete(PermissionRequiredMixin, DeleteView):
    model = Stimulae
    success_url = reverse_lazy('stimulae')
    permission_required = 'lablog.can_change_status'


class SubjectCreate(PermissionRequiredMixin, CreateView):
    model = Subject
    fields = '__all__'
    permission_required = 'lablog.can_change_status'

class SubjectUpdate(PermissionRequiredMixin, UpdateView):
    model = Subject
    fields = ['first_name','last_name','date_of_birth','gender']
    permission_required = 'lablog.can_change_status'

class SubjectDelete(PermissionRequiredMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy('subjects')
    permission_required = 'lablog.can_change_status'
    

#Classes created for the forms challenge
class ExperimentCreate(PermissionRequiredMixin, CreateView):
    model = Experiment
    fields = '__all__'
    permission_required = 'lablog.can_change_status'

class ExperimentUpdate(PermissionRequiredMixin, UpdateView):
    model = Experiment
    fields = '__all__'
    permission_required = 'lablog.can_change_status'

class ExperimentDelete(PermissionRequiredMixin, DeleteView):
    model = Experiment
    success_url = reverse_lazy('experiments')
    permission_required = 'lablog.can_change_status'
