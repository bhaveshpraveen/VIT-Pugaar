from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import ComplaintDetail, DepartmentDetail, EmployeeDetail, BlockDetail, FloorDetail
from .views import ComplaintList, UserList, DepartmentList, EmployeeList, BlockList, FloorList

urlpatterns = [
    url(r'^complaints/$', ComplaintList.as_view()),
    url(r'^complaints/(?P<slug>[0-9a-zA-z\-]+)/$', ComplaintDetail.as_view()),

    url(r'^users/$', UserList.as_view()),

    url(r'^departments/$', DepartmentList.as_view()),
    url(r'^departments/(?P<slug>[0-9a-zA-Z\-]+)/$', DepartmentDetail.as_view()),

    url(r'^employees/$', EmployeeList.as_view()),
    url(r'^employees/(?P<slug>[0-9a-zA-Z\-]+)/$', EmployeeDetail.as_view()),

    url(r'^blocks/$', BlockList.as_view()),
    url(r'^blocks/(?P<slug>[0-9a-zA-Z\-]+)/$', BlockDetail.as_view()),

    url(r'^floors/$', FloorList.as_view()),
    url(r'^floors/(?P<slug>[0-9a-zA-Z\-]+)/$', FloorDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)