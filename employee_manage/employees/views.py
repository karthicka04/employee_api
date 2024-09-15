from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from .models import Employee
from .serializers import EmployeeSerializer
from django.db import IntegrityError
from rest_framework.parsers import JSONParser

class SignupView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return render(request, 'employees/signup.html')

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            User.objects.create_user(username=username, password=password)
            return Response({'message': 'Sign up successful'}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'message': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return render(request, 'employees/login.html')

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class EmployeeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        employees = Employee.objects.all()
        context = {'employees': employees}
        return render(request, 'employees/employee_list.html', context)

class AddEmployeeView(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [JSONParser]

    def get(self, request, *args, **kwargs):
        return render(request, 'employees/add_employee.html')

    def post(self, request, *args, **kwargs):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Employee added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteEmployeeView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        # Render delete employee page
        employees = Employee.objects.all()
        context = {'employees': employees}
        return render(request, 'employees/delete_employee.html', context)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        employee = Employee.objects.get(pk=pk)
        employee.delete()
        return Response({'message': 'Employee deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        