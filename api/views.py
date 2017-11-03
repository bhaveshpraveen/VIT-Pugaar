from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework.decorators import api_view
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

import json

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
    queryset = Block.objects.all()
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


# class UserCreate(APIView):
#
#
#     def POST(self, request, format=None):
#         print(request.data)
#         floor_number = request.data.get('floor_number', None)
#         block = request.data.get('block', None)
#         data = {
#             'block': None,
#             'floor': None,
#             'registration_number': None,
#             'email': None,
#             'first_name': None,
#             'middle_name': None,
#             'last_name': None,
#             'phone_number': None,
#             'is_active': False,
#             'admin': False,
#             'staff': False,
#             'room_no': None,
#         }
#         try:
#             data['block'] = Block.objects.get(block_letter=block)
#         except Exception as e:
#             data['block'] = None
#         try:
#             data['floor'] = data['block'].floors.get(floor_number=floor_number)
#         except Exception as e:
#             data['floor'] = None
#
#         data['registration_number'] = request.data.get('registration_number', None)
#         data['email'] = request.data.get('email', None)
#         data['first_name'] = request.data.get('first_name', None)
#         data['middle_name'] = request.data.get('middle_name', None)
#         data['last_name'] = request.data.get('last_name', None)
#         data['phone_number'] = request.data.get('phone_number', None)
#         data['room_no'] = request.data.get('Room_no', None)
#
#         print('Here')
#         try:
#             user = User.objects.create(**data)
#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#         serializer = UserSerializer(user)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
#     def put(self, request, format=None):
#
#         floor_number = request.data.get('floor_number', None)
#         block = request.data.get('block', None)
#         data = {
#             'block': None,
#             'floor': None,
#             'registration_number': None,
#             'email': None,
#             'first_name': None,
#             'middle_name': None,
#             'last_name': None,
#             'phone_number': None,
#             'is_active': True,
#             'admin': False,
#             'staff': False,
#             'room_no': None,
#         }
#
#         try:
#             data['block'] = Block.objects.get(block_letter=block)
#             data['floor'] = data['block'].floors.get(floor_number=floor_number)
#         except Department.DoesNotExist or Floor.DoesNotExist:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#         data['email'] = request.data.get('email', None)
#         data['first_name'] = request.data.get('first_name', None)
#         data['middle_name'] = request.data.get('middle_name', None)
#         data['last_name'] = request.data.get('last_name', None)
#         data['phone_number'] = request.data.get('phone_number', None)
#         data['room_no'] = request.data.get('Room_no', None)
#
#         try:
#             user = User.objects.get(registration_number=data['registration_number'])
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#         serializer = UserSerializer(user, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, format=None):
#         reg_no = request.data.get('registration_number')
#
#         try:
#             user = User.objects.get(registration_number=reg_no)
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#         user.is_active = False



@api_view(['POST'])
def user_create(request, *args, **kwargs):
    print(request.data)
    if request.method == 'POST':
        print(request.POST)
        floor_number = request.POST.get('floor_number', None)
        block = request.POST.get('block', None)
        data = {
            'block': None,
            'floor': None,
            'registration_number': None,
            'email': None,
            'first_name': None,
            'middle_name': None,
            'last_name': None,
            'phone_number': None,
            'is_active': False,
            'admin': False,
            'staff': False,
            'room_no': None,
        }
        try:
            data['block'] = Block.objects.get(block_letter=block)
        except Exception as e:
            data['block'] = None
        try:
            data['floor'] = data['block'].floors.get(floor_number=floor_number)
        except Exception as e:
            data['floor'] = None

        data['registration_number'] = request.POST.get('registration_number', None)
        data['email'] = request.POST.get('email', None)
        data['first_name'] = request.POST.get('first_name', None)
        data['middle_name'] = request.POST.get('middle_name', None)
        data['last_name'] = request.POST.get('last_name', None)
        data['phone_number'] = request.POST.get('phone_number', None)
        data['room_no'] = request.POST.get('Room_no', None)

        print(data)
        try:
            user = User.objects.create(**data)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        print('Second here')
        return Response(status=status.HTTP_201_CREATED)
