from django.test import TestCase

# Create your tests here.

from lablog.models import Subject


class SubjectModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Subject.objects.create(first_name='Big', last_name='Bob')

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
