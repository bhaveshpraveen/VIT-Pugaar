from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import ComplaintList, UserList, DepartmentList, EmployeeList, BlockList, FloorList

urlpatterns = [
    url(r'^complaints/$', ComplaintList.as_view()),
    url(r'^users/$', UserList.as_view()),
    url(r'^departments/$', DepartmentList.as_View()),
    url(r'employees/$', EmployeeList.as_view()),
    url(r'blocks', BlockList.as_view()),
    url(r'floors', FloorList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)