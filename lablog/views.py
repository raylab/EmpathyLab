from django.shortcuts import render

#import pdb; pdb.set_trace()

# Create your views here.

from .models import Experiment, Subject, Record, Stimulae

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

class SubjectListView(generic.ListView):
    """
    Generic class-based list view for a list of authors.
    """
    model = Subject
    paginate_by = 10 


class SubjectDetailView(generic.DetailView):
    """
    Generic class-based detail view for an author.
    """
    model = Subject


from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedRecordsByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing records to current user. 
    """
    model = Record
    template_name ='lablog/record_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return Record.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
        

# Added as part of challenge!
from django.contrib.auth.mixins import PermissionRequiredMixin

class LoanedRecordsAllListView(PermissionRequiredMixin,generic.ListView):
    """
    Generic class-based view listing all records. Only visible to users with can_mark_returned permission.
    """
    model = Record
    permission_required = 'lablog.can_mark_returned'
    template_name ='lablog/record_list_borrowed_all.html'
    paginate_by = 10
    
    def get_queryset(self):
        return Record.objects.filter(status__exact='o').order_by('due_back')  


from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import permission_required

from .forms import RenewBookForm

@permission_required('lablog.can_mark_returned')
def renew_record_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    record_inst=get_object_or_404(Record, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            record_inst.due_back = form.cleaned_data['renewal_date']
            record_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'lablog/record_renew_librarian.html', {'form': form, 'record':record_inst})
    
    
    
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Subject


class SubjectCreate(PermissionRequiredMixin, CreateView):
    model = Subject
    fields = '__all__'
    initial={'date_of_death':'12/10/2016',}
    permission_required = 'lablog.can_mark_returned'

class SubjectUpdate(PermissionRequiredMixin, UpdateView):
    model = Subject
    fields = ['first_name','last_name','date_of_birth','date_of_death']
    permission_required = 'lablog.can_mark_returned'

class SubjectDelete(PermissionRequiredMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy('authors')
    permission_required = 'lablog.can_mark_returned'
    

#Classes created for the forms challenge
class ExperimentCreate(PermissionRequiredMixin, CreateView):
    model = Experiment
    fields = '__all__'
    initial={'date_of_death':'12/10/2016',}
    permission_required = 'lablog.can_mark_returned'

class ExperimentUpdate(PermissionRequiredMixin, UpdateView):
    model = Experiment
    fields = '__all__'
    permission_required = 'lablog.can_mark_returned'

class ExperimentDelete(PermissionRequiredMixin, DeleteView):
    model = Experiment
    success_url = reverse_lazy('experiments')
    permission_required = 'lablog.can_mark_returned'
