from django.db import models

# Create your models here.

from django.urls import reverse #Used to generate urls by reversing the URL patterns


class Stimulae(models.Model):
    """
    Model representing a stimulate description and resourse reference.
    """
    name = models.CharField(max_length=200, help_text="Enter stimulate description and resourse reference")
    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name
        
        
class Feedback(models.Model):
    """
    Model representing a feedback arrangement.
    """
    name = models.CharField(max_length=200, help_text="Enter a feedback arrangement.)")
    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name
        
        
class Experiment(models.Model):
    """
    Model representing a experiment (but not a specific record).
    """
    title = models.CharField(max_length=200)
    subject = models.ForeignKey('Subject', on_delete=models.SET_NULL, null=True)
      # Foreign Key used because subject can only have one author, but subjects can have multiple experiments
      # Author as a string rather than object because it hasn't been declared yet in file.
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the experiment")
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    stimulae = models.ManyToManyField(Stimulae, help_text="Select a stimulae for this experiment")
      # ManyToManyField used because Subject can contain many experiment. experiment can cover many subjects.
      # Subject declared as an object because it has already been defined.
    feedback = models.ForeignKey('Feedback', on_delete=models.SET_NULL, null=True)
      
    def display_stimulae(self):
        """
        Creates a string for the Stimulae. This is required to display stimulae in Admin.
        """
        return ', '.join([ stimulae.name for stimulae in self.stimulae.all()[:3] ])
        display_stimulae.short_description = 'Stimulae'
    
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular record.
        """
        return reverse('record-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title
        
        
import uuid # Required for unique record instances
from datetime import date

from django.contrib.auth.models import User #Required to assign User as a borrower

class Record(models.Model):
    """
    Model representing a specific record.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular record across whole library")
    experiment = models.ForeignKey('Experiment', on_delete=models.SET_NULL, null=True) 
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
        

    LOAN_STATUS = (
        ('d', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status= models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='d', help_text='Record status')

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set record as returned"),)   

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s (%s)' % (self.id,self.experiment.title)
        

class Subject(models.Model):
    """
    Model representing test subgect.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular subject instance.
        """
        return reverse('subject-detail', args=[str(self.id)])
    

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s, %s' % (self.last_name, self.first_name)
