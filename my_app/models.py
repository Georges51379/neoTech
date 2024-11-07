from django.db import models


class Client(models.Model):
    client_id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    country = models.CharField(max_length=100)
    account_balance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10)
    transaction_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"
