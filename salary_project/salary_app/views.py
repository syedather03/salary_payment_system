from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, SalaryPayment
from django.http import HttpResponse  
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'home.html')

def add_employee(request):
    if request.method == "POST":
        name = request.POST.get("name")
        salary = request.POST.get("salary")
        status = request.POST.get("status")

        Employee.objects.create(name=name, monthly_salary=salary, status=status)
        return redirect("dashboard")

    return render(request, "salary_app/add_employee.html")

def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return redirect("dashboard")

def payment_history(request):
    payments = SalaryPayment.objects.all().order_by("-date_paid")
    return render(request, "salary_app/payment_history.html", {"payments": payments})

@csrf_exempt
def make_payment(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == "POST":
        amount = int(request.POST.get("amount", 0))  

        # Ensure payment does not exceed salary
        total_paid = SalaryPayment.objects.filter(employee=employee).aggregate(total_paid=Sum('amount_paid'))['total_paid'] or 0
        remaining_salary = employee.monthly_salary - total_paid

        if amount > remaining_salary:
            return HttpResponse("Error: Payment exceeds remaining salary!", status=400) 

        # Save payment
        new_remaining_salary = remaining_salary - amount  
        SalaryPayment.objects.create(employee=employee, amount_paid=amount, remaining_salary=new_remaining_salary)

        return redirect("dashboard")

    # ✅ Handle GET request by displaying a payment form
    return render(request, "salary_app/make_payment.html", {"employee": employee})


def generate_report(request):
    employees = Employee.objects.all()
    report_data = []

    for employee in employees:
        total_paid = SalaryPayment.objects.filter(employee=employee).aggregate(Sum("amount_paid"))["amount_paid__sum"] or 0
        remaining_salary = employee.monthly_salary - total_paid
        report_data.append({"employee": employee, "total_paid": total_paid, "remaining_salary": remaining_salary})

    return render(request, "salary_app/report.html", {"report_data": report_data})


def add_bonus_deduction(request):
    if request.method == "POST":
        employee = get_object_or_404(Employee, id=request.POST.get("employee_id"))
        amount = float(request.POST.get("amount"))
        type = request.POST.get("type")

        BonusDeduction.objects.create(employee=employee, amount=amount, type=type)

        if type == "Bonus":
            employee.monthly_salary += amount
        else:
            employee.monthly_salary -= amount

        employee.save()
        return redirect("dashboard")

    return redirect("dashboard")

def dashboard(request):
    employees = Employee.objects.all()
    payments = SalaryPayment.objects.all()
    return render(request, "salary_app/dashboard.html", {"employees": employees, "payments": payments})




















########################### Last Working Code From here #########################################
# from django.shortcuts import render, get_object_or_404, redirect
# from django.db.models import Sum  # Import Sum
# from .models import Employee, SalaryPayment
# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponseRedirect
# from django.contrib import messages 

# def home(request):
#     return render(request, 'home.html')

# # def add_payment_form(request):
# #     employees = Employee.objects.all()  # Get all employees for dropdown
# #     return render(request, "salary_app/add_payment.html", {"employees": employees})
# def add_employee(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         salary = request.POST.get("salary")
#         status = request.POST.get("status", "Active")  # Default to Active

#         # Save Employee in Database
#         Employee.objects.create(name=name, monthly_salary=salary, status=status)

#         return HttpResponseRedirect("/api/")  # Redirect to Dashboard after adding

#     return render(request, "salary_app/add_employee.html")

# def dashboard(request):
#     employees = Employee.objects.all()
#     payments = SalaryPayment.objects.all()
#     return render(request, "salary_app/dashboard.html", {"employees": employees, "payments": payments})

# @csrf_exempt
# def make_payment(request, employee_id):
#     if request.method == "POST":
#         employee = get_object_or_404(Employee, id=employee_id)
#         amount = int(request.POST.get("amount"))

#         # Ensure payment does not exceed salary
#         total_paid = SalaryPayment.objects.filter(employee=employee).aggregate(total_paid=Sum('amount_paid'))['total_paid'] or 0
#         remaining_salary = employee.monthly_salary - total_paid

#         if amount > remaining_salary:
#             messages.warning(request, f"Payment exceeds remaining salary! Available: {remaining_salary}")  # ✅ Show Warning
#             return redirect("dashboard")  # ✅ Cancel Transaction and Redirect

#         # Calculate new remaining salary after payment
#         new_remaining_salary = remaining_salary - amount  

#         # Save payment with remaining_salary
#         SalaryPayment.objects.create(employee=employee, amount_paid=amount, remaining_salary=new_remaining_salary)

#         messages.success(request, "Payment successful!")  # ✅ Show Success Message
#         return redirect("dashboard")

#     return redirect("dashboard")
#################################################### Till Here ###########################################
# @csrf_exempt
# def make_payment(request, employee_id):
#     if request.method == "POST":
#         employee = get_object_or_404(Employee, id=employee_id)
#         amount = int(request.POST.get("amount"))

#         # Ensure payment does not exceed salary
#         total_paid = SalaryPayment.objects.filter(employee=employee).aggregate(total_paid=Sum('amount_paid'))['total_paid'] or 0
#         remaining_salary = employee.monthly_salary - total_paid

#         if amount > remaining_salary:
#             amount = remaining_salary  # Limit payment to remaining salary

#         # **Fix: Ensure remaining_salary is saved**
#         new_remaining_salary = remaining_salary - amount  # Calculate remaining salary after payment

#         # Save payment with remaining_salary
#         SalaryPayment.objects.create(employee=employee, amount_paid=amount, remaining_salary=new_remaining_salary)

#         return redirect("dashboard")

#     return redirect("dashboard")
























