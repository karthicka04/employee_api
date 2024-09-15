from django.urls import path
from .views import EmployeeListView, SignupView, LoginView, AddEmployeeView, DeleteEmployeeView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('employees/list/', EmployeeListView.as_view(), name='employee_list'),
    path('employees/add/', AddEmployeeView.as_view(), name='add_employee'),
    path('employees/delete/', DeleteEmployeeView.as_view(), name='delete_employee'),
    path('employees/delete/<int:pk>/', DeleteEmployeeView.as_view(), name='delete_employee_pk'),
]
