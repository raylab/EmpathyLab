from django.test import TestCase

# Create your tests here.


from lablog.models import Subject
from django.urls import reverse

class SubjectListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Create subjects for pagination tests
        number_of_subjects = 13
        for subject_num in range(number_of_subjects):
           Subject.objects.create(first_name='Christian %s' % subject_num, last_name = 'Surname %s' % subject_num,)
           
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
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['subject_list']) == 10)

    def test_lists_all_subjects(self):
        #Get second page and confirm it has (exactly) the remaining 3 items
        resp = self.client.get(reverse('subjects')+'?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['subject_list']) == 3)
        

import datetime
from django.utils import timezone
        
from lablog.models import Record, Experiment, Stimulae, Feedback
from django.contrib.auth.models import User #Required to assign User as a attendant

class LoanedRecordsByUserListViewTest(TestCase):

    def setUp(self):
        #Create two users
        test_user1 = User.objects.create_user(username='testuser1', password='DAU12345') 
        test_user1.save()
        test_user2 = User.objects.create_user(username='testuser2', password='DAU12345') 
        test_user2.save()
        
        #Create a experiment
        test_subject = Subject.objects.create(first_name='John', last_name='Smith')
        test_stimulae = Stimulae.objects.create(name='Fantasy')
        test_feedback = Feedback.objects.create(name='English')
        test_record = Experiment.objects.create(title='Experiment Title', summary = 'My experiment summary', isbn='ABCDEFG', subject=test_subject, feedback=test_feedback,)
        # Create stimulae as a post-step
        stimulae_objects_for_record = Stimulae.objects.all()
        #test_record.stimulae = stimulae_objects_for_record ## AB fixed many2many Direct assignment prohibition.
        test_record.stimulae.set(stimulae_objects_for_record)
        test_record.save()

        #Create 30 Record objects
        number_of_record_copies = 30
        for record_copy in range(number_of_record_copies):
            return_date= timezone.now() + datetime.timedelta(days=record_copy%5)
            if record_copy % 2:
                the_attendant=test_user1
            else:
                the_attendant=test_user2
            status='m'
            Record.objects.create(experiment=test_record,imprint='Unlikely Imprint, 2016', due_back=return_date, attendant=the_attendant, status=status)
        
    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('my-borrowed'))
        self.assertRedirects(resp, '/accounts/login/?next=/lablog/myexperiments/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='DAU12345')
        resp = self.client.get(reverse('my-borrowed'))
        
        #Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        #Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        #Check we used correct template
        self.assertTemplateUsed(resp, 'lablog/record_list_borrowed_user.html')

    def test_only_borrowed_experiments_in_list(self):
        login = self.client.login(username='testuser1', password='DAU12345')
        resp = self.client.get(reverse('my-borrowed'))
        
        #Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        #Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)
        
        #Check that initially we don't have any experiments in list (none on loan)
        self.assertTrue('record_list' in resp.context)
        self.assertEqual( len(resp.context['record_list']),0)
        
        #Now change all experiments to be on loan 
        get_ten_experiments = Record.objects.all()[:10]

        for copy in get_ten_experiments:
            copy.status='o'
            copy.save()
        
        #Check that now we have borrowed experiments in the list
        resp = self.client.get(reverse('my-borrowed'))
        #Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        #Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)
        
        self.assertTrue('record_list' in resp.context)
        
        #Confirm all experiments belong to testuser1 and are on loan
        for experimentitem in resp.context['record_list']:
            self.assertEqual(resp.context['user'], experimentitem.attendant)
            self.assertEqual('o', experimentitem.status)

    def test_pages_paginated_to_ten(self):
    
        #Change all experiments to be on loan.
        #This should make 15 test user ones.
        for copy in Record.objects.all():
            copy.status='o'
            copy.save()
            
        login = self.client.login(username='testuser1', password='DAU12345')
        resp = self.client.get(reverse('my-borrowed'))
        
        #Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        #Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)
                
        #Confirm that only 10 items are displayed due to pagination (if pagination not enabled, there would be 15 returned)
        self.assertEqual( len(resp.context['record_list']),10)

    def test_pages_ordered_by_due_date(self):
    
        #Change all experiments to be on loan
        for copy in Record.objects.all():
            copy.status='o'
            copy.save()
            
        login = self.client.login(username='testuser1', password='DAU12345')
        resp = self.client.get(reverse('my-borrowed'))
        
        #Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        #Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)
                
        #Confirm that of the items, only 10 are displayed due to pagination.
        self.assertEqual( len(resp.context['record_list']),10)
        
        last_date=0
        for copy in resp.context['record_list']:
            if last_date==0:
                last_date=copy.due_back
            else:
                self.assertTrue(last_date <= copy.due_back)
                

                
from django.contrib.auth.models import Permission # Required to grant the permission needed to set a experiment as returned.

class RenewRecordsViewTest(TestCase):

    def setUp(self):
        #Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='DAU12345') 
        test_user1.save()
        
        test_user2 = User.objects.create_user(username='testuser2', password='DAU12345') 
        test_user2.save()    
        permission = Permission.objects.get(name='Set record as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()
        
        #Create a experiment
        test_subject = Subject.objects.create(first_name='John', last_name='Smith')
        test_stimulae = Stimulae.objects.create(name='Fantasy')
        test_feedback = Feedback.objects.create(name='English')
        test_experiment = Experiment.objects.create(title='Experiment Title', summary = 'My experiment summary', isbn='ABCDEFG', subject=test_subject, feedback=test_feedback,)
        # Create stimulae as a post-step
        stimulae_objects_for_experiment = Stimulae.objects.all()
        test_experiment.stimulae.set(stimulae_objects_for_experiment)
        test_experiment.save()

        #Create a Record object for test_user1
        return_date= datetime.date.today() + datetime.timedelta(days=5)
        self.test_record1=Record.objects.create(experiment=test_experiment,imprint='Unlikely Imprint, 2016', due_back=return_date, attendant=test_user1, status='o')
        
        #Create a Record object for test_user2
        return_date= datetime.date.today() + datetime.timedelta(days=5)
        self.test_record2=Record.objects.create(experiment=test_experiment,imprint='Unlikely Imprint, 2016', due_back=return_date, attendant=test_user2, status='o')
        
    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('renew-record-librarian', kwargs={'pk':self.test_record1.pk,}) )
        #Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual( resp.status_code,302)
        self.assertTrue( resp.url.startswith('/accounts/login/') )
        
    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='DAU12345')
        resp = self.client.get(reverse('renew-record-librarian', kwargs={'pk':self.test_record1.pk,}) )
        
        #Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual( resp.status_code,302)
        self.assertTrue( resp.url.startswith('/accounts/login/') )

    def test_logged_in_with_permission_borrowed_experiment(self):
        login = self.client.login(username='testuser2', password='DAU12345')
        resp = self.client.get(reverse('renew-record-librarian', kwargs={'pk':self.test_record2.pk,}) )
        
        #Check that it lets us login - this is our experiment and we have the right permissions.
        self.assertEqual( resp.status_code,200)

    def test_logged_in_with_permission_another_users_borrowed_experiment(self):
        login = self.client.login(username='testuser2', password='DAU12345')
        resp = self.client.get(reverse('renew-record-librarian', kwargs={'pk':self.test_record1.pk,}) )
        
        #Check that it lets us login. We're a librarian, so we can view any users experiment
        self.assertEqual( resp.status_code,200)
        
    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='DAU12345')
        resp = self.client.get(reverse('renew-record-librarian', kwargs={'pk':self.test_record1.pk,}) )
        self.assertEqual( resp.status_code,200)

        #Check we used correct template
        self.assertTemplateUsed(resp, 'lablog/record_renew_librarian.html')
        
    def test_form_renewal_date_initially_has_date_three_weeks_in_future(self):
        login = self.client.login(username='testuser2', password='DAU12345')
        resp = self.client.get(reverse('renew-record-librarian', kwargs={'pk':self.test_record1.pk,}) )
        self.assertEqual( resp.status_code,200)
        
        date_3_weeks_in_future = datetime.date.today() + datetime.timedelta(weeks=3)
        self.assertEqual(resp.context['form'].initial['renewal_date'], date_3_weeks_in_future )
        
    def test_form_invalid_renewal_date_past(self):
        login = self.client.login(username='testuser2', password='DAU12345')
        
        date_in_past = datetime.date.today() - datetime.timedelta(weeks=1)
        resp = self.client.post(reverse('renew-record-librarian', kwargs={'pk':self.test_record1.pk,}), {'renewal_date':date_in_past} )
        self.assertEqual( resp.status_code,200)
        self.assertFormError(resp, 'form', 'renewal_date', 'Invalid date - renewal in past')
        
    def test_form_invalid_renewal_date_future(self):
        login = self.client.login(username='testuser2', password='DAU12345')
        
        invalid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=5)
        resp = self.client.post(reverse('renew-record-librarian', kwargs={'pk':self.test_record1.pk,}), {'renewal_date':invalid_date_in_future} )
        self.assertEqual( resp.status_code,200)
        self.assertFormError(resp, 'form', 'renewal_date', 'Invalid date - renewal more than 4 weeks ahead')
        
    def test_redirects_to_all_borrowed_record_list_on_success(self):
        login = self.client.login(username='testuser2', password='DAU12345')
        valid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=2)
        resp = self.client.post(reverse('renew-record-librarian', kwargs={'pk':self.test_record1.pk,}), {'renewal_date':valid_date_in_future} )
        self.assertRedirects(resp, reverse('all-borrowed') )

    def test_HTTP404_for_invalid_experiment_if_logged_in(self):
        import uuid 
        test_uid = uuid.uuid4() #unlikely UID to match our record!
        login = self.client.login(username='testuser2', password='DAU12345')
        resp = self.client.get(reverse('renew-record-librarian', kwargs={'pk':test_uid,}) )
        self.assertEqual( resp.status_code,404)


        

class SubjectCreateViewTest(TestCase):
    """
    Test case for the SubjectCreate view (Created as Challenge!)
    """

    def setUp(self):
        #Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='DAU12345') 
        test_user1.save()
        
        test_user2 = User.objects.create_user(username='testuser2', password='DAU12345') 
        test_user2.save()    
        permission = Permission.objects.get(name='Set record as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()
        
        #Create a experiment
        test_subject = Subject.objects.create(first_name='John', last_name='Smith')

        
    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('subject_create') )
        self.assertRedirects(resp, '/accounts/login/?next=/lablog/subject/create/' )
        
    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='DAU12345')
        resp = self.client.get(reverse('subject_create') )
        self.assertRedirects(resp, '/accounts/login/?next=/lablog/subject/create/' )

    def test_logged_in_with_permission(self):
        login = self.client.login(username='testuser2', password='DAU12345')
        resp = self.client.get(reverse('subject_create') )
        self.assertEqual( resp.status_code,200)
        
    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='DAU12345')
        resp = self.client.get(reverse('subject_create') )
        self.assertEqual( resp.status_code,200)
        self.assertTemplateUsed(resp, 'lablog/subject_form.html')
         
    def test_form_gender_initially_set_to_expected_date(self):
        login = self.client.login(username='testuser2', password='DAU12345')
        resp = self.client.get(reverse('subject_create') )
        self.assertEqual( resp.status_code,200)
        
        expected_initial_date = datetime.date(2016, 12, 10)
        #response_date=resp.context['form'].initial['gender']
        #response_date=datetime.datetime.strptime(response_date, "%m/%d/%Y").date()
        #self.assertEqual(response_date, expected_initial_date )
        
    def test_redirects_to_detail_view_on_success(self):
        login = self.client.login(username='testuser2', password='DAU12345')
        resp = self.client.post(reverse('subject_create'),{'first_name':'Christian Name','last_name':'Surname',} )
        #Manually check redirect because we don't know what subject was created
        self.assertEqual( resp.status_code,302)
        self.assertTrue( resp.url.startswith('/lablog/subject/') )
