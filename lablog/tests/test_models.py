from django.test import TestCase
from lablog.models import Subject, Feedback, Stimulae
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest import mock


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


class StimulaeModelTest(TestCase):

    @classmethod
    def save_side_effect(*args, **kwargs):
        return str(args[2])

    @classmethod
    @mock.patch('django.core.files.storage.default_storage._wrapped')
    def setUpTestData(cls, storage_mock):
        storage_mock.save = mock.Mock(side_effect=cls.save_side_effect)
        media1 = SimpleUploadedFile(
            name='test_video_file.mov',
            content=b'mov content',
            content_type='video/mp4')
        media2 = SimpleUploadedFile(
            name='test_audio_file.mp3',
            content=b'mp3 content',
            content_type='audio/mpeg')

        Stimulae.objects.create(
            name='Fantasy',
            media1=media1,
            media2=media2,
        )

    def test_has_name(self):
        stimulae = Stimulae.objects.get(id=1)
        self.assertEquals(stimulae.name, 'Fantasy')

    def test_has_media_files_assigned(self):
        stimulae = Stimulae.objects.get(id=1)
        self.assertIn('test_video_file', stimulae.media1.name)
        self.assertIn('test_audio_file', stimulae.media2.name)

    def test_representation_is_a_name(self):
        stimulae = Stimulae.objects.get(id=1)
        self.assertEquals(stimulae.name, str(stimulae))

    def test_has_absolute_url(self):
        stimulae = Stimulae.objects.get(id=1)
        self.assertEquals(
            stimulae.get_absolute_url(), reverse(
                'stimulae-detail', args=['1']))
