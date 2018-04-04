from django.test import TestCase

# Create your tests here.


from lablog.models import Subject, Record, Experiment, Stimulae, Feedback
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta, date

from django.contrib.auth.models import User, Permission


class SubjectListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create subjects for pagination tests
        number_of_subjects = 13
        for subject_num in range(number_of_subjects):
            Subject.objects.create(
                first_name='Christian %s' %
                subject_num,
                last_name='Surname %s' %
                subject_num,
            )

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/lablog/subjects/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('subjects'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('subjects'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'lablog/subject_list.html')

    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('subjects'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['subject_list']) == 10)

    def test_lists_all_subjects(self):
        # Get second page and confirm it has (exactly) the remaining 3 items
        resp = self.client.get(reverse('subjects') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['subject_list']) == 3)


class LoanedRecordsByUserListViewTest(TestCase):

    def setUp(self):
        # Create two users
        test_user1 = User.objects.create_user(
            username='testuser1', password='DAU12345')
        test_user1.save()
        test_user2 = User.objects.create_user(
            username='testuser2', password='DAU12345')
        test_user2.save()

        # Create a experiment
        test_subject = Subject.objects.create(
            first_name='John', last_name='Smith')
        test_stimulae = Stimulae.objects.create(name='Fantasy')
        test_record = Experiment.objects.create(
            title='Experiment Title',
            summary='My experiment summary',
            isbn='ABCDEFG')
        test_record.save()
        test_record.subjects.add(test_subject)
        # Create stimulae as a post-step
        stimulae_objects_for_record = Stimulae.objects.all()
        # test_record.stimulae = stimulae_objects_for_record ## AB fixed
        # many2many Direct assignment prohibition.
        test_record.stimulae.set(stimulae_objects_for_record)
        test_record.save()

        # Create 30 Record objects
        number_of_record_copies = 30
        for record_copy in range(number_of_record_copies):
            return_date = timezone.now() + timedelta(days=record_copy % 5)
            if record_copy % 2:
                the_attendant = test_user1
            else:
                the_attendant = test_user2
            status = 'm'
            Record.objects.create(
                experiment=test_record,
                imprint='Unlikely Imprint, 2016',
                attendant=the_attendant,
                status=status)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('my-records'))
        self.assertRedirects(resp, '/accounts/login/?next=/lablog/myrecords/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='DAU12345')
        resp = self.client.get(reverse('my-records'))

        # Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(resp, 'lablog/record_list.html')

    def test_only_borrowed_experiments_in_list(self):
        login = self.client.login(username='testuser1', password='DAU12345')
        resp = self.client.get(reverse('my-records'))

        # Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        # Check that initially we don't have any experiments in list (none on
        # loan)
        self.assertTrue('record_list' in resp.context)
        self.assertEqual(len(resp.context['record_list']), 0)

        # Now change all experiments to be on loan
        get_ten_experiments = Record.objects.all()[:10]

        for copy in get_ten_experiments:
            copy.status = 'o'
            copy.save()

        # Check that now we have borrowed experiments in the list
        resp = self.client.get(reverse('my-records'))
        # Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        self.assertTrue('record_list' in resp.context)

        # Confirm all experiments belong to testuser1 and are on loan
        for experimentitem in resp.context['record_list']:
            self.assertEqual(resp.context['user'], experimentitem.attendant)
            self.assertEqual('o', experimentitem.status)

    def test_pages_paginated_to_ten(self):

        # Change all experiments to be on loan.
        # This should make 15 test user ones.
        for copy in Record.objects.all():
            copy.status = 'o'
            copy.save()

        login = self.client.login(username='testuser1', password='DAU12345')
        resp = self.client.get(reverse('my-records'))

        # Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        # Confirm that only 10 items are displayed due to pagination (if
        # pagination not enabled, there would be 15 returned)
        self.assertEqual(len(resp.context['record_list']), 10)


class SubjectCreateViewTest(TestCase):
    """
    Test case for the SubjectCreate view (Created as Challenge!)
    """

    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(
            username='testuser1', password='DAU12345')
        test_user1.save()

        test_user2 = User.objects.create_user(
            username='testuser2', password='DAU12345')
        test_user2.save()

        test_user2.user_permissions.add(Permission.objects.get(
            codename='can_change_status'))
        test_user2.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('subject_create'))
        self.assertRedirects(
            resp,
            '/accounts/login/?next=' +
            reverse('subject_create'))

    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='DAU12345')
        resp = self.client.get(reverse('subject_create'))
        self.assertRedirects(
            resp,
            '/accounts/login/?next=' +
            reverse('subject_create'))

    def test_logged_in_with_permission(self):
        login = self.client.login(username='testuser2', password='DAU12345')
        resp = self.client.get(reverse('subject_create'))
        self.assertEqual(resp.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='DAU12345')
        resp = self.client.get(reverse('subject_create'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'lablog/subject_form.html')

    def test_form_gender_initially_set_to_expected_date(self):
        login = self.client.login(username='testuser2', password='DAU12345')
        resp = self.client.get(reverse('subject_create'))
        self.assertEqual(resp.status_code, 200)

        expected_initial_date = date(2016, 12, 10)
        # response_date=resp.context['form'].initial['gender']
        #response_date=datetime.datetime.strptime(response_date, "%m/%d/%Y").date()
        #self.assertEqual(response_date, expected_initial_date )

    def test_redirects_to_detail_view_on_success(self):
        login = self.client.login(username='testuser2', password='DAU12345')
        resp = self.client.post(
            reverse('subject_create'), {
                'first_name': 'Christian Name', 'last_name': 'Surname', })
        # Manually check redirect because we don't know what subject was
        # created
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/lablog/subject/'))


class FeedbackCreateViewTest(TestCase):
    """
    Test case for Feedback creation view.
    """

    def setUp(self):
        User.objects.create_user(username='unprivileged', password='DAU12345')

        user2 = User.objects.create_user(
            username='scientist', password='DAU12345')
        user2.user_permissions.add(
            Permission.objects.get(codename='can_change_status'))
        user2.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('feedback_create'))
        self.assertRedirects(
            resp,
            '/accounts/login/?next=' +
            reverse('feedback_create'))

    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='unprivileged', password='DAU12345')
        resp = self.client.get(reverse('feedback_create'))
        self.assertRedirects(
            resp,
            '/accounts/login/?next=' +
            reverse('feedback_create'))

    def test_logged_in_with_permission(self):
        login = self.client.login(username='scientist', password='DAU12345')
        resp = self.client.get(reverse('feedback_create'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'lablog/feedback_form.html')

    def test_redirects_to_detail_view_on_success(self):
        login = self.client.login(username='scientist', password='DAU12345')
        form_data = {
            'electrode1': '1',
            'electrode2': '2',
            'electrode3': '3',
            'electrode4': '4',
            'analysis': 'default',
        }
        resp = self.client.post(reverse('feedback_create'), form_data)
        self.assertRedirects(resp, reverse('feedback-detail', args=['1']))


class StimulaeCreateViewTest(TestCase):
    """
    Test case for Stimulae creation view.
    """

    def setUp(self):
        User.objects.create_user(username='unprivileged', password='DAU12345')

        user2 = User.objects.create_user(
            username='scientist', password='DAU12345')
        user2.user_permissions.add(
            Permission.objects.get(codename='can_change_status'))
        user2.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('stimulae_create'))
        self.assertRedirects(
            resp,
            '/accounts/login/?next=' +
            reverse('stimulae_create'))

    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='unprivileged', password='DAU12345')
        resp = self.client.get(reverse('stimulae_create'))
        self.assertRedirects(
            resp,
            '/accounts/login/?next=' +
            reverse('stimulae_create'))

    def test_logged_in_with_permission(self):
        login = self.client.login(username='scientist', password='DAU12345')
        resp = self.client.get(reverse('stimulae_create'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'lablog/stimulae_form.html')

    def test_redirects_to_detail_view_on_success(self):
        login = self.client.login(username='scientist', password='DAU12345')
        form_data = {
            'name': 'test_stimulae',
            'media1': 'somefile.mov',
            'media2': 'somefile.mp3',
        }
        resp = self.client.post(reverse('stimulae_create'), form_data)
        self.assertRedirects(resp, reverse('stimulae-detail', args=['1']))
