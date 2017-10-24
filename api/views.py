from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .serializers import (
    UserSerializer,
    EmployeeSerializer,
    ComplaintSerializer,
    FloorSerializer,
    BlockSerializer,
    DepartmentSerializer,
)
from complaint.models import Complaint
from department.models import (
    Department,
    Employee
)
from hostel.models import (
    Block,
    Floor,
)

User = get_user_model()


class ComplaintList(ListAPIView):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer


class ComplaintDetail(RetrieveAPIView):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer


class DepartmentList(ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentDetail(RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class EmployeeList(ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeDetail(RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class BlockList(ListAPIView):
    queryset =  Block.objects.all()
    serializer_class = BlockSerializer


class BlockDetail(RetrieveAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer


class FloorList(ListAPIView):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer


class FloorDetail(RetrieveAPIView):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


#todo Refactor UserDetail

