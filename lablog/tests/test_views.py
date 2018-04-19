from django.test import TestCase

# Create your tests here.


from lablog.models import Subject, Analysis
from django.urls import reverse

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
        self.client.login(username='testuser1', password='DAU12345')
        resp = self.client.get(reverse('subject_create'))
        self.assertRedirects(
            resp,
            '/accounts/login/?next=' +
            reverse('subject_create'))

    def test_logged_in_with_permission(self):
        self.client.login(username='testuser2', password='DAU12345')
        resp = self.client.get(reverse('subject_create'))
        self.assertEqual(resp.status_code, 200)

    def test_uses_correct_template(self):
        self.client.login(username='testuser2', password='DAU12345')
        resp = self.client.get(reverse('subject_create'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'lablog/subject_form.html')

    def test_form_gender_initially_set_to_expected_date(self):
        self.client.login(username='testuser2', password='DAU12345')
        resp = self.client.get(reverse('subject_create'))
        self.assertEqual(resp.status_code, 200)

        # expected_initial_date = date(2016, 12, 10)
        # response_date=resp.context['form'].initial['gender']
        # response_date=datetime.datetime.strptime(response_date, "%m/%d/%Y").date()
        # self.assertEqual(response_date, expected_initial_date )

    def test_redirects_to_detail_view_on_success(self):
        self.client.login(username='testuser2', password='DAU12345')
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

    @classmethod
    def setUpTestData(cls):
        Analysis.objects.create(name='SomeAnalysis')

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
        self.client.login(username='unprivileged', password='DAU12345')
        resp = self.client.get(reverse('feedback_create'))
        self.assertRedirects(
            resp,
            '/accounts/login/?next=' +
            reverse('feedback_create'))

    def test_logged_in_with_permission(self):
        self.client.login(username='scientist', password='DAU12345')
        resp = self.client.get(reverse('feedback_create'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'lablog/feedback_form.html')

    def test_redirects_to_detail_view_on_success(self):
        self.client.login(username='scientist', password='DAU12345')
        form_data = {
            'electrode1': '1',
            'electrode2': '2',
            'electrode3': '3',
            'electrode4': '4',
            'analysis': '1',
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
        self.client.login(username='unprivileged', password='DAU12345')
        resp = self.client.get(reverse('stimulae_create'))
        self.assertRedirects(
            resp,
            '/accounts/login/?next=' +
            reverse('stimulae_create'))

    def test_logged_in_with_permission(self):
        self.client.login(username='scientist', password='DAU12345')
        resp = self.client.get(reverse('stimulae_create'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'lablog/stimulae_form.html')

    def test_redirects_to_detail_view_on_success(self):
        self.client.login(username='scientist', password='DAU12345')
        form_data = {
            'name': 'test_stimulae',
            'media1': 'somefile.mov',
            'media2': 'somefile.mp3',
        }
        resp = self.client.post(reverse('stimulae_create'), form_data)
        self.assertRedirects(resp, reverse('stimulae-detail', args=['1']))
