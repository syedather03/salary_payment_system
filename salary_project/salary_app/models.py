from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')

    def __str__(self):
        return self.name

class SalaryPayment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True)
    remaining_salary = models.DecimalField(max_digits=10, decimal_places=2)

class BonusDeduction(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=[("Bonus", "Bonus"), ("Deduction", "Deduction")])
    date = models.DateTimeField(auto_now_add=True)