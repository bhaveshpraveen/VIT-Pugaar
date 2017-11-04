from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import permissions

from api.views import ComplaintDetail, DepartmentDetail, EmployeeDetail, BlockDetail, FloorDetail, UserDetail, BlockOnlyDetail, FloorOnlyDetail
from .views import (
    ComplaintList,
    UserList,
    DepartmentList,
    EmployeeList,
    BlockList,
    FloorList,
    UserCreate,
    ComplaintCreate,
    BlockCreate,
    FloorCreate,
    EmployeeCreate,
    DepartmentCreate,
)

urlpatterns = [
    url(r'^complaints/$', ComplaintList.as_view()),
    url(r'complaints/create/$', ComplaintCreate.as_view()),
    url(r'^complaints/(?P<pk>[0-9a-zA-z\-]+)/$', ComplaintDetail.as_view()),

    url(r'^users/$', UserList.as_view()),
    url(r'^users/create/$', UserCreate.as_view()),
    url(r'^users/(?P<pk>[0-9a-zA-Z\-]+)/$', UserDetail.as_view()),

    url(r'^blockdetails/$', BlockOnlyDetail.as_view()),
    url(r'^floordetails/$', FloorOnlyDetail.as_view()),

    url(r'^departments/$', DepartmentList.as_view()),
    url(r'^departments/create/$', DepartmentCreate.as_view()),
    url(r'^departments/(?P<pk>[0-9a-zA-Z\-]+)/$', DepartmentDetail.as_view()),

    url(r'^employees/$', EmployeeList.as_view()),
    url(r'^employees/create/$', EmployeeCreate.as_view()),
    url(r'^employees/(?P<pk>[0-9a-zA-Z\-]+)/$', EmployeeDetail.as_view()),

    url(r'^blocks/$', BlockList.as_view()),
    url(r'^blocks/create/$', BlockCreate.as_view()),
    url(r'^blocks/(?P<pk>[0-9a-zA-Z\-]+)/$', BlockDetail.as_view()),

    url(r'^floors/$', FloorList.as_view()),
    url(r'^floors/create/$', FloorCreate.as_view()),
    url(r'^floors/(?P<pk>[0-9a-zA-Z\-]+)/$', FloorDetail.as_view()),


]

urlpatterns = format_suffix_patterns(urlpatterns)