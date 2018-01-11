from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^experiments/$', views.ExperimentListView.as_view(), name='experiments'),
    url(r'^record/(?P<pk>\d+)$', views.RecordDetailView.as_view(), name='record-detail'),
    url(r'^subjects/$', views.SubjectListView.as_view(), name='subjects'),  
    url(r'^subject/(?P<pk>\d+)$', views.SubjectDetailView.as_view(), name='subject-detail'),
]


urlpatterns += [   
    url(r'^myexperiments/$', views.LoanedRecordsByUserListView.as_view(), name='my-borrowed'),
    url(r'^borrowed/$', views.LoanedRecordsAllListView.as_view(), name='all-borrowed'), #Added for challenge
]


# Add URLConf for librarian to renew a experiment.
urlpatterns += [   
    url(r'^record/(?P<pk>[-\w]+)/renew/$', views.renew_record_librarian, name='renew-record-librarian'),
]


# Add URLConf to create, update, and delete authors
urlpatterns += [  
    url(r'^subject/create/$', views.SubjectCreate.as_view(), name='subject_create'),
    url(r'^subject/(?P<pk>\d+)/update/$', views.SubjectUpdate.as_view(), name='subject_update'),
    url(r'^subject/(?P<pk>\d+)/delete/$', views.SubjectDelete.as_view(), name='subject_delete'),
]

# Add URLConf to create, update, and delete experiments
urlpatterns += [  
    url(r'^experiment/create/$', views.ExperimentCreate.as_view(), name='experiment_create'),
    url(r'^experiment/(?P<pk>\d+)/update/$', views.ExperimentUpdate.as_view(), name='experiment_update'),
    url(r'^experiment/(?P<pk>\d+)/delete/$', views.ExperimentDelete.as_view(), name='experiment_delete'),
]
