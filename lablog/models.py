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
        

class Observation(models.Model):
    """
    Model representing a feedback arrangement.
    """
    name = models.CharField(max_length=200, help_text="Enter a observation arrangement.)")
    
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
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the experiment")
    subjects = models.ManyToManyField('Subject')
    #subject = models.ForeignKey('Subject', on_delete=models.SET_NULL, null=True)
    isbn = models.CharField('ISBN',max_length=13, help_text='13 CharacterISBN number')  
    stimulae = models.ManyToManyField(Stimulae, help_text="Select a stimulae for this experiment")
    feedback = models.ManyToManyField(Feedback, help_text="Select a feedback for this experiment")
      
    def display_stimulae(self):
        """
        Creates a string for the Stimulae. This is required to display stimulae in Admin.
        """
        return ', '.join([ stimulae.name for stimulae in self.stimulae.all()[:3] ])
        display_stimulae.short_description = 'Stimulae'

    def display_feedback(self):
        """
        Creates a string for the Feedback. This is required to display feedback in Admin.
        """
        return ', '.join([ feedback.name for feedback in self.feedback.all()[:3] ])
        display_feedback.short_description = 'Feedback'



    class Meta:
        ordering = ['title']
    
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular record.
        """
        return reverse('experiment-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title
        
        

class Subject(models.Model):
    """
    Model representing test subgect.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    experiments = models.ManyToManyField(Experiment, blank=True) # , on_delete=models.SET_NULL, null=True)

    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER, blank=True, default='O', help_text='Subject Gender')

    class Meta:
       ordering = ['last_name']
    
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



import uuid # Required for unique record instances
from datetime import date

from django.contrib.auth.models import User #Required to assign User as a attendant

import plyvel

class Record(models.Model):
    """
    Model representing a specific record.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular record across whole log")
    experiment = models.ForeignKey(Experiment, on_delete=models.SET_NULL, null=True) 
    imprint = models.CharField(max_length=200)
    rec_date = models.DateField(null=True, blank=True)
    attendant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    observation = models.ForeignKey(Observation, on_delete=models.SET_NULL, null=True, blank=True)
    
    RECORD_STATUS = (
        ('d', 'Maintenance'),
        ('a', 'Available'),
        ('r', 'Restricted'),
    )

    status= models.CharField(max_length=1, choices=RECORD_STATUS, blank=True, default='d', help_text='Record status')

    class Meta:
        permissions = (("can_change_status", "Set record status"),)   
    
    def get_recorddb(self):
        myStr = 'records/'+str(self.id)+'db'
        db = plyvel.DB(myStr, create_if_missing=True)
        return db
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular subject instance.
        """
        return reverse('record-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s (%s)' % (self.id, self.experiment.title)
