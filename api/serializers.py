from django.contrib.auth import get_user_model
from rest_framework import serializers

from complaint.models import Complaint
from department.models import Department, Employee
from hostel.models import Block, Floor


class ComplaintSerializer(serializers.ModelSerializer):

    class Meta:
        model = Complaint
        fields = ('user', 'department', 'employee', 'user_block', 'user_floor', 'slug',  'issue', 'description', 'updated', 'timestamp', 'user_room', 'issue_count', 'issue', 'status')

    # todo add this to the view
    # def perform_create(self, serializer):
    #    serializer.save(user=self.request.user)


class EmployeeSerializer(serializers.ModelSerializer):
    complaints = ComplaintSerializer(many=True)

    class Meta:
        model = Employee
        fields = ('id', 'name', 'phone_number', 'department', 'block', 'floor', 'complaints')


class DepartmentSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True)
    complaints = ComplaintSerializer(many=True)

    class Meta:
        model = Department
        fields = ('user', 'name', 'slug', 'employees', 'complaints')


class UserSerializer(serializers.ModelSerializer):
    complaints = ComplaintSerializer(many=True)

# todo floor and block are fk
    class Meta:
        model = get_user_model()
        fields = (
            'complaints',
            'registration_number',
            'email',
            'first_name',
            'middle_name',
            'last_name',
            'phone_number',
            'room_no',
            'floor',
            'block'
        )


class FloorSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)
    employees = EmployeeSerializer(many=True)
    complaints = ComplaintSerializer(many=True)

    class Meta:
        model = Floor
        fields = ('users', 'employees', 'complaints', 'block', 'floor_number')


class BlockSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)
    floors = FloorSerializer(many=True)
    employees = EmployeeSerializer(many=True)
    complaints = ComplaintSerializer(many=True)

    class Meta:
        model = Block
        fields = ('users', 'floors', 'block_letter', 'name', 'slug', 'employees', 'complaints')


class BlockOnlySerializer(serializers.ModelSerializer):
    floors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Block
        fields = ('name', 'slug', 'floors')


class FloorOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = Floor
        fields = ('floor_number', 'slug', 'block')



'''
All of the fields which declare a Serializer class 
eg 
class BlockSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)
    floors = FloorSerializer(many=True)
    
Here 'users' is the related name in the User Model. We're supposed to make use of related_name here for serializing
Similarly, 'floors' is the related_name in the Floor model.
'''
