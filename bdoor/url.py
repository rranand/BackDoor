from django.conf.urls import url
from django.urls import path
from .views import home, scan, select, query, queryAll

urlpatterns = [
    path('', home, name='homepage'),
    path('scan', scan, name='scan'),
    path('select', select, name='select'),
    url(r'^query/(?P<ind>[\d]+)/$', query, name='query'),
    path('queryAll', queryAll, name='queryAll')
]
