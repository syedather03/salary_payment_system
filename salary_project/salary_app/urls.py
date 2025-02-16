from django.urls import path
from .views import add_employee, delete_employee, make_payment, payment_history, generate_report, add_bonus_deduction, dashboard



urlpatterns = [
    path("add-employee/", add_employee, name="add_employee"),
    path("delete-employee/<int:employee_id>/", delete_employee, name="delete_employee"),
    path("pay/<int:employee_id>/", make_payment, name="make_payment"),
    path("payment-history/", payment_history, name="payment_history"),
    path("report/", generate_report, name="generate_report"),
    path("add-bonus-deduction/", add_bonus_deduction, name="add_bonus_deduction"),
    path('', dashboard, name="dashboard"),

]



########################### Last Running Code ##################
# from django.urls import path
# from .views import home,dashboard, make_payment, add_employee 

# urlpatterns = [
#     # path('', home, name='home'), 
#     path('', dashboard, name="dashboard"),
#     path("pay/<int:employee_id>/", make_payment, name="make_payment"),
#     path("add-employee/", add_employee, name="add_employee"),  
# ]




    
