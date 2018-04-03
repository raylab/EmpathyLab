from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^experiments/$', views.ExperimentListView.as_view(), name='experiments'),
    url(r'^experiment/(?P<pk>\d+)$', views.ExperimentDetailView.as_view(), name='experiment-detail'),
    url(r'^experiment/create/$', views.ExperimentCreate.as_view(), name='experiment_create'),
    url(r'^experiment/(?P<pk>\d+)/update/$', views.ExperimentUpdate.as_view(), name='experiment_update'),
    url(r'^experiment/(?P<pk>\d+)/delete/$', views.ExperimentDelete.as_view(), name='experiment_delete'),

    url(r'^subjects/$', views.SubjectListView.as_view(), name='subjects'),
    url(r'^subject/(?P<pk>\d+)$', views.SubjectDetailView.as_view(), name='subject-detail'),
    url(r'^subject/create/$', views.SubjectCreate.as_view(), name='subject_create'),
    url(r'^subject/(?P<pk>\d+)/update/$', views.SubjectUpdate.as_view(), name='subject_update'),
    url(r'^subject/(?P<pk>\d+)/delete/$', views.SubjectDelete.as_view(), name='subject_delete'),

    url(r'^records/$', views.RecordListView.as_view(), name='records'),
    url(r'^records/$', views.RecordsAllListView.as_view(), name='all-records'),
    url(r'^record/(?P<pk>[-\w]+)$', views.RecordDetailView.as_view(), name='record-detail'),
    url(r'^record/create/$', views.RecordCreate.as_view(), name='record_create'),

    url(r'^stimulaes/$', views.StimulaeListView.as_view(), name='stimulaes'),
    url(r'^stimulae/(?P<pk>\d+)$', views.StimulaeDetailView.as_view(), name='stimulae-detail'),
    url(r'^stimulae/create/$', views.StimulaeCreate.as_view(), name='stimulae_create'),
    url(r'^stimulae/(?P<pk>\d+)/update/$', views.StimulaeUpdate.as_view(), name='stimulae_update'),
    url(r'^stimulae/(?P<pk>\d+)/delete/$', views.StimulaeDelete.as_view(), name='stimulae_delete'),

    url(r'^feedbacks/$', views.FeedbackListView.as_view(), name='feedbacks'),
    url(r'^feedback/(?P<pk>\d+)$', views.FeedbackDetailView.as_view(), name='feedback-detail'),
    url(r'^feedback/create/$', views.FeedbackCreate.as_view(), name='feedback_create'),
    url(r'^feedback/(?P<pk>\d+)/update/$', views.FeedbackUpdate.as_view(), name='feedback_update'),
    url(r'^feedback/(?P<pk>\d+)/delete/$', views.FeedbackDelete.as_view(), name='feedback_delete'),

    url(r'^myrecords/$', views.RecordsByUserListView.as_view(), name='my-records'),
]
