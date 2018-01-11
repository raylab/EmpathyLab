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
    url(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    url(r'^borrowed/$', views.LoanedBooksAllListView.as_view(), name='all-borrowed'), #Added for challenge
]


# Add URLConf for librarian to renew a book.
urlpatterns += [   
    url(r'^record/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name='renew-book-librarian'),
]


# Add URLConf to create, update, and delete authors
urlpatterns += [  
    url(r'^subject/create/$', views.SubjectCreate.as_view(), name='author_create'),
    url(r'^subject/(?P<pk>\d+)/update/$', views.SubjectUpdate.as_view(), name='author_update'),
    url(r'^subject/(?P<pk>\d+)/delete/$', views.SubjectDelete.as_view(), name='author_delete'),
]

# Add URLConf to create, update, and delete books
urlpatterns += [  
    url(r'^book/create/$', views.BookCreate.as_view(), name='book_create'),
    url(r'^book/(?P<pk>\d+)/update/$', views.BookUpdate.as_view(), name='book_update'),
    url(r'^book/(?P<pk>\d+)/delete/$', views.BookDelete.as_view(), name='book_delete'),
]
