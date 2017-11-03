import json

from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import permissions

from .serializers import (
    UserSerializer,
    EmployeeSerializer,
    ComplaintSerializer,
    FloorSerializer,
    BlockSerializer,
    DepartmentSerializer,
)
from complaint.utils import (
    make_slug,
    assign_employee,
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

"""
Accepted data
{
"registration_number": "20BCE0904",
"email": "bhaveshpraveen10@gmail.com",
"first_name": "Yoda",
"phone_number": "9789959296",
"last_name": "Jedi"
}
"""


# todo is_active is set to True, confirm email not set yet
# todo existing user registers another account, how to handle this case ? [UNIQUE constraint failed: users_user.registration_number]

class UserCreate(APIView):
    def post(self, request, *args, **kwargs):
            floor_number = request.data.get('floor_number', None)
            block = request.data.get('block', None)
            data = {
                'block': None,
                'floor': None,
                'registration_number': None,
                'email': None,
                'first_name': None,
                'middle_name': None,
                'last_name': None,
                'phone_number': None,
                'is_active': True,
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

            data['registration_number'] = request.data.get('registration_number', None)
            data['email'] = request.data.get('email', None)
            data['first_name'] = request.data.get('first_name', None)
            data['middle_name'] = request.data.get('middle_name', None)
            data['last_name'] = request.data.get('last_name', None)
            data['phone_number'] = request.data.get('phone_number', None)
            data['room_no'] = request.data.get('Room_no', None)

            print(data)
            try:
                user = User.objects.create(**data)
            except Exception as e:
                res = {'detail': e.__str__()}
                print(res)
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_201_CREATED)


# assign the employee
class ComplaintCreate(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        user = request.user
        department = request.data.get('department', None)
        block = request.data.get('user_block', None)
        floor = request.data.get('user_floor', None)

        data = {
            'user': user,
            'user_room': request.data.get('user_room', None),
            'department': Department.objects.get(pk=department) if department else None,
            'user_block': Block.objects.get(pk=block) if block else None,
            'user_floor': Floor.objects.get(pk=floor) if floor else None,
            'status': False,
            'issue': False,
            'description': request.data.get('description', None)
        }

        data['slug'] = make_slug(data)
        data['employee'] = assign_employee(data)

        try:

            obj = Complaint.objects.create(**data)

        except Exception as e:

            res = {
                'details': e.__str__()
            }

            print(res)
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            ComplaintSerializer(data=obj),
            status=status.HTTP_201_CREATED
        )








