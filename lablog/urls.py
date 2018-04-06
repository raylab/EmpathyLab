from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('experiments/', views.ExperimentListView.as_view(), name='experiments'),
    path('experiment/<int:pk>', views.ExperimentDetailView.as_view(), name='experiment-detail'),
    path('experiment/create/', views.ExperimentCreate.as_view(), name='experiment_create'),
    path('experiment/<int:pk>/update/', views.ExperimentUpdate.as_view(), name='experiment_update'),
    path('experiment/<int:pk>/delete/', views.ExperimentDelete.as_view(), name='experiment_delete'),

    path('subjects/', views.SubjectListView.as_view(), name='subjects'),
    path('subject/<int:pk>', views.SubjectDetailView.as_view(), name='subject-detail'),
    path('subject/create/', views.SubjectCreate.as_view(), name='subject_create'),
    path('subject/<int:pk>/update/', views.SubjectUpdate.as_view(), name='subject_update'),
    path('subject/<int:pk>/delete/', views.SubjectDelete.as_view(), name='subject_delete'),

    path('records/', views.RecordListView.as_view(), name='records'),
    path('records/', views.RecordsAllListView.as_view(), name='all-records'),
    path('record/<uuid:pk>', views.RecordDetailView.as_view(), name='record-detail'),
    path('record/create/', views.RecordCreate.as_view(), name='record_create'),

    path('stimulaes/', views.StimulaeListView.as_view(), name='stimulaes'),
    path('stimulae/<int:pk>', views.StimulaeDetailView.as_view(), name='stimulae-detail'),
    path('stimulae/create/', views.StimulaeCreate.as_view(), name='stimulae_create'),
    path('stimulae/<int:pk>/update/', views.StimulaeUpdate.as_view(), name='stimulae_update'),
    path('stimulae/<int:pk>/delete/', views.StimulaeDelete.as_view(), name='stimulae_delete'),

    path('feedbacks/', views.FeedbackListView.as_view(), name='feedbacks'),
    path('feedback/<int:pk>', views.FeedbackDetailView.as_view(), name='feedback-detail'),
    path('feedback/create/', views.FeedbackCreate.as_view(), name='feedback_create'),
    path('feedback/<int:pk>/update/', views.FeedbackUpdate.as_view(), name='feedback_update'),
    path('feedback/<int:pk>/delete/', views.FeedbackDelete.as_view(), name='feedback_delete'),
]
