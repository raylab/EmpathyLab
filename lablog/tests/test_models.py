from django.test import TestCase
from lablog.models import Subject, Feedback
from django.urls import reverse


class SubjectModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Subject.objects.create(
            first_name='Big',
            last_name='Bob',
            notes='TestNotes')

    def test_first_name_label(self):
        subject = Subject.objects.get(id=1)
        field_label = subject._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')

    def test_last_name_label(self):
        subject = Subject.objects.get(id=1)
        field_label = subject._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label, 'last name')

    def test_date_of_birth_label(self):
        subject = Subject.objects.get(id=1)
        field_label = subject._meta.get_field('date_of_birth').verbose_name
        self.assertEquals(field_label, 'date of birth')

    def test_gender_label(self):
        subject = Subject.objects.get(id=1)
        field_label = subject._meta.get_field('gender').verbose_name
        self.assertEquals(field_label, 'gender')

    def test_first_name_max_length(self):
        subject = Subject.objects.get(id=1)
        max_length = subject._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 100)

    def test_last_name_max_length(self):
        subject = Subject.objects.get(id=1)
        max_length = subject._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        subject = Subject.objects.get(id=1)
        expected_object_name = '%s, %s' % (
            subject.last_name, subject.first_name)
        self.assertEquals(expected_object_name, str(subject))

    def test_get_absolute_url(self):
        subject = Subject.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(subject.get_absolute_url(), '/lablog/subject/1')

    def test_subject_has_notes(self):
        subject = Subject.objects.get(id=1)
        self.assertEquals(subject.notes, 'TestNotes')


class FeedbackModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Feedback.objects.create(
            electrode1=1,
            electrode2=2,
            electrode3=3,
            electrode4=4,
            analysis='AnalysisText')

    def test_has_electorode_positions(self):
        feedback = Feedback.objects.get(id=1)
        self.assertEquals(feedback.electrode1, 1)
        self.assertEquals(feedback.electrode2, 2)
        self.assertEquals(feedback.electrode3, 3)
        self.assertEquals(feedback.electrode4, 4)

    def test_has_analysis_text(self):
        feedback = Feedback.objects.get(id=1)
        self.assertEquals(feedback.analysis, 'AnalysisText')

    def test_representation_includes_positions_and_analysis(self):
        feedback = Feedback.objects.get(id=1)
        self.assertEquals(
            'Feedback 1 (1, 2, 3, 4, "AnalysisText")',
            str(feedback))

    def test_has_absolute_url(self):
        feedback = Feedback.objects.get(id=1)
        self.assertEquals(
            feedback.get_absolute_url(), reverse(
                'feedback-detail', args=['1']))
