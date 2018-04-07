from django.db import models

# Create your models here.

# Used to generate urls by reversing the URL patterns
from django.urls import reverse


class Stimulae(models.Model):
    """
    Model representing a stimulate description and resourse reference.
    """
    name = models.CharField(
        max_length=200,
        help_text="Enter stimulate description and resourse reference")

    media1 = models.FileField(
        default='/dev/null',
        help_text='First media file')

    media2 = models.FileField(
        default='/dev/null',
        null=True,
        help_text='Optional media file')

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

    def get_absolute_url(self):
        """
        Returns the url to access a particular stimulae instance.
        """
        return reverse('stimulae-detail', args=[str(self.id)])


class Feedback(models.Model):
    """
    Model representing a feedback arrangement.
    """
    electrode1 = models.IntegerField(
        default=1, help_text='Position of first electrode')
    electrode2 = models.IntegerField(
        default=1, help_text='Position of second electrode')
    electrode3 = models.IntegerField(
        default=1, help_text='Position of third electrode')
    electrode4 = models.IntegerField(
        default=1, help_text='Position of fourth electrode')
    analysis = models.CharField(
        max_length=100,
        default='default',
        help_text='Analysis setup')

    def __str__(self):
        """
        String for representing Feedback object.
        """
        return 'Feedback {self.id} ({self.electrode1}, {self.electrode2}, {self.electrode3}, {self.electrode4}, \"{self.analysis}\")'.format(
            self=self)

    def get_absolute_url(self):
        """
        Returns the url to access a particular feedback instance.
        """
        return reverse('feedback-detail', args=[str(self.id)])


class Subject(models.Model):
    """
    Model representing test subgect.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)

    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER,
        blank=True,
        default='O',
        help_text='Subject Gender')

    notes = models.TextField(blank=True)

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


class Record(models.Model):
    """
    Model representing a specific record.
    """

    EEG = models.TextField(blank=True)
    StartTime = models.DateTimeField(null=True, blank=True)
    StopTime = models.DateTimeField(null=True, blank=True)
    TENSControl = models.TextField(blank=True)
    ObservationMedia1 = models.CharField(max_length=200, blank=True)
    ObservationMedia2 = models.CharField(max_length=200, blank=True)

    class Meta:
        permissions = (("can_change_status", "Set record status"),)


class Experiment(models.Model):
    """
    Model representing a experiment (but not a specific record).
    """
    title = models.CharField(max_length=200)
    summary = models.TextField(
        max_length=1000,
        help_text="Enter a brief description of the experiment")
    DateTime = models.DateTimeField(null=True, blank=True)
    subjects = models.ManyToManyField(Subject)
    stimulae = models.OneToOneField(
        Stimulae, on_delete=models.PROTECT,
        help_text="Select a stimulae for this experiment")
    feedback = models.OneToOneField(
        Feedback, on_delete=models.PROTECT,
        help_text="Select a feedback for this experiment")
    records = models.ManyToManyField(
        Record, blank=True, help_text="Select a records for this experiment")

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
