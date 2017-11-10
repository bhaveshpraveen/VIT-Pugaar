# todo To my future-self: This thing's a mess, try to put the repeated pieces of code in a separate function. Atleast Try!!

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import permissions
from spam_filter.asf import check

from .serializers import (
    UserSerializer,
    EmployeeSerializer,
    ComplaintSerializer,
    FloorSerializer,
    BlockSerializer,
    DepartmentSerializer,
    BlockOnlySerializer,
    FloorOnlySerializer,
)
from complaint.utils import (
    make_slug,
)
from complaint.models import Complaint
from department.models import (
    Department,
    Employee
)
from department.utils import floor_specific_departments
from hostel.models import (
    Block,
    Floor,
)


from rest_framework.authentication import SessionAuthentication, BasicAuthentication 


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


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


class BlockOnlyDetail(ListAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockOnlySerializer


class FloorOnlyDetail(ListAPIView):
    queryset = Floor.objects.all()
    serializer_class = FloorOnlySerializer


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



"""
all fields

registration_number:9bce0904
email:bhaveshpraveen10@gmail.com
first_name:Bhavesh
middle_name: ichigo
last_name:Praveen
phone_number:9789959296
password:12ab34cd
account_for:S
block : name-of-a-block
floor : name-of-a-block-2
room_no : 256

minimal

registration_number:16BCE0904
email:bhaveshpraveen10@gmail.com
first_name:Bhavesh
phone_number:9789959296
last_name:Praveen
password:12ab34cd
account_for:S

"""


# todo is_active is set to True, confirm email not set yet
# todo existing user registers another account, how to handle this case ? [UNIQUE constraint failed: users_user.registration_number]

# todo Permissions
class UserCreate(APIView):
    permission_classes = (permissions.AllowAny, )
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format=None):
        print('data', request.data)
        print('user:', request.user)

        data = {
            'registration_number': request.data.get('registration_number').lower() if request.data.get('registration_number', None) else None,
            'email': request.data.get('email', None),
            'first_name': request.data.get('first_name', None),
            'middle_name': request.data.get('middle_name', None),
            'last_name': request.data.get('last_name', None),
            'phone_number': request.data.get('phone_number'),
            'is_active': True,
            'admin': False,
            'staff': False,
            'room_no': request.data.get('room_no', None),
        }

        floor = request.data.get('floor', None)
        block = request.data.get('block', None)

        if floor:
            data['floor'] = Floor.objects.get(pk=floor)

        if block:
            data['block'] = Block.objects.get(pk=block)

        account_for = request.data.get('account_for', None)
        if not account_for:
            return Response(
                {'details': 'Send in the required Credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not request.data.get('password', None):
            return Response(
                {'details': 'Send in the required Credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.create(**data)

        except Exception as e:
            return Response(
                {'details': e.__str__()},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(request.data.get('password'))

        if account_for.lower() == 's':
            group = Group.objects.get(name='Students')

        elif account_for.lower() == 'cw':
            group = Group.objects.get(name='Chief Warden')
            user.admin = True
            user.staff = True

        elif account_for.lower() == 'bw':
            group = Group.objects.get(name='Block Warden')

        elif account_for.lower() == 'dh':
            group = Group.objects.get(name='Department Head')

        elif account_for.lower() == 'fw':
            group = Group.objects.get(name='Floor Warden')

        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.groups.add(group)
        user.save()
        print(user)

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk, format=None):
        try:
            obj = User.objects.get(pk=pk)

        except Exception as e:
            return Response(
                {'details': e.__str__()},
                status=status.HTTP_400_BAD_REQUEST
            )

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

'''
department:electrical
user_block:name-of-a-block
user_floor:name-of-a-block-2
user_room:235 -> if presen then room complaint
description:Fan and Light not working
'''


 #  todo: what to do if there are no employees satisfying the given criteria while assigning ?
# @method_decorator(csrf_exempt, name='dispatch')
class ComplaintCreate(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def assign_employee(self, data):
        q = Employee.objects.filter(
            department=data['department'],
            block=data['user_block']
        )

        if data['department'] in floor_specific_departments:
            q = q.filter(
                floor=data['user_floor']
            )

        if q.exists():
            # Assign the complaint to the employee who has minimum number of complaints allocated to him at the time

            minimum = 0
            for i in range(1, q.count()):
                if q[i].complaints.count() < q[minimum].complaints.count():
                    minimum = i

            data['employee'] = q[minimum]
            return data

        else:
            return data

    def spam(self, description):
        return not check(description)

    def post(self, request, format=None):
        user = request.user
        print('user', user)

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
        }

        description = request.data.get('description')
        print('Checking if spam')

        if self.spam(description):

            return Response(
                {
                    'details': 'Your complaint has been flagged as spam',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        print('Not spam')
        data['description'] = description

        data['slug'] = make_slug(data)
        data = self.assign_employee(data)

        try:
            obj = Complaint.objects.create(**data)

        except Exception as e:

            return Response(
                {
                    'details': e.__str__()
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        user_complaint_list = obj.user.complaints.all()
        print('list: ', user_complaint_list)

        serializer = ComplaintSerializer(user_complaint_list, many=True)
        print(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


"""
block_letter: e
"""


# todo Permissions
class BlockCreate(APIView):

    def post(self, request, format=None):
        print(request.data)
        block_letter = request.data.get('block_letter', None)

        if block_letter:
            obj = Block.objects.create(block_letter=block_letter)
            return Response(
                status=status.HTTP_201_CREATED
            )

        else:
            return Response(
                {
                    'details': 'Please Provide Valid details'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk, format=None):
        try:
            obj = Block.objects.get(pk=pk)

        except Exception as e:
            return Response(
                e.__str__(),
                status=status.HTTP_400_BAD_REQUEST
            )

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
block : name-of-f-block
floor : 3
"""


# todo Permissions
class FloorCreate(APIView):
    def post(self, request, format=None):
        block = request.data.get('block', None)
        floor = request.data.get('floor', None)

        if block and floor:

            try:
                block_obj = Block.objects.get(pk=block)

            except Exception as e:

                return Response(
                    {
                        'details': 'Make sure the given Block exists'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                obj = Floor.objects.create(
                    block=block_obj,
                    floor_number=int(floor)
                )

            except Exception as e:

                return Response(
                    e.__str__(),
                    status=status.HTTP_400_BAD_REQUEST
                )
            print('Success Return')
            return Response(status=status.HTTP_201_CREATED)

        else:

            return Response(
                {'details': 'Please Provide Valid details'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk, format=None):
        try:
            obj = Floor.objects.get(pk=pk)

        except Exception as e:
            return Response(
                {'details': e.__str__()},
                status=status.HTTP_400_BAD_REQUEST
            )

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



'''
user : 20BCE0904
name : Sample Department
'''

#todo permissions
class DepartmentCreate(APIView):
    def post(self, request, format=None):
        data = {
            'name': request.data.get('name')
        }

        user = request.data.get('user', None)

        if not user:
            return Response(
                {'details': 'Please provide a user as the head of the department'},
                status=status.HTTP_400_BAD_REQUEST
            )

        data['user'] = User.objects.get(pk=user)

        try:
            obj = Department.objects.create(**data)

        except Exception as e:
            return Response(
                e.__str__(),
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk, format=None):
        try:
            obj = Department.objects.get(pk=pk)

        except Exception as e:
            return Response(
                e.__str__(),
                status=status.HTTP_400_BAD_REQUEST
            )

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# todo permissions
class EmployeeCreate(APIView):
    def post(self, request, format=None):
        block = request.data.get('block')
        floor = request.data.get('floor')
        department = request.data.get('department')

        if department in floor_specific_departments and not floor:
            return Response(
                {'details': 'Floor has to be provided if you\'re adding an employee in this department'},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = {
            'name': request.data.get('name', None),
            'phone_number': request.data.get('phone_number', None),
        }
        # to check if the block object exists and to retrieve it
        try:
            block_obj = Block.objects.get(pk=block)
            data['block'] = block_obj

        except Exception as e:

            return Response(
                {
                    'details': 'Make sure the given Block exists'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # to check if department object exists and to retrieve it
        try:
            department_obj = Department.objects.get(pk=department)
            data['department'] = department_obj

        except Exception as e:

            return Response(
                dict(details='Make sure the given Floor exists'),
                status=status.HTTP_400_BAD_REQUEST
            )

        # only if a floor is given, floor is not necessary every time
        if floor:
            try:
                floor_obj = Floor.objects.get(pk=floor)
                data['floor'] = floor_obj

            except Exception as e:

                return Response(

                    dict(details='Make sure the given Floor exists'),
                    status=status.HTTP_400_BAD_REQUEST
                )
        try:
            employee_obj = Employee.objects.create(**data)

        except Exception as e:

            return Response(
                e.__str__(),
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, pk, format=None):
        try:
            obj = Employee.objects.get(pk=pk)

        except Exception as e:
            return Response(
                dict(details=e.__str__()),
                status=status.HTTP_400_BAD_REQUEST
            )

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ComplaintComplete(APIView):
    def patch(self, request, pk, format=None):
        try:
            obj = Complaint.objects.get(pk=pk)

        except Exception as e:
            return Response(
                dict(details=e.__str__()),
                status=status.HTTP_400_BAD_REQUEST
            )

        obj.status = True
        obj.save()

        return Response(
            dict(details='Successfully completed'),
            status=status.HTTP_202_ACCEPTED
        )

class ComplaintDelete(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def delete(self, request):
        print(request.data)
        user = request.user
        pk = request.data.get('pk', None)

        if not pk:

            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        print('Here')


        try:
            obj = user.complaints.get(pk=pk)

        except Exception as e:

            return Response(
                {
                    'details': 'Check the details'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            obj.delete()

        except Exception as e:

            return Response(
                {
                    'details': 'Something went wrong'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class UserChangePassword(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def patch(self, request):
        user = request.user
        new_pass = request.data.get('password')

        user.set_password(new_pass)
        user.save()

        return Response(status=status.HTTP_200_OK)